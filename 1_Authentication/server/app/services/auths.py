from datetime import datetime
import asyncio
from .common.mail import send_email, render_email_template

from core.security import create_access_token, create_refresh_token, create_verify_code, get_password_hash, is_valid_password, create_state
from core.config import settings
from core.redis import get_redis_client

from repositories.users import user_repo
from repositories.tokens import token_repo

from schemas.tokens import TokenInDB, TokenLogin
from schemas.users import UserInDB, UserCreate, UserBase, UserUpdate
from schemas.auths import TokenRefresh, ChangePassword, Login
from schemas.utils import InfoEmailSend

from utils.errors.auth import (
    OAuthProviderNotSupportedError,
    OAuthClientError,
    OAuthStateMismatchError,
    InvalidCredentialsError,
    EmailSendFailureError,
    EmailSendFailureError
)

from utils.errors.user import UserAccountInactiveError
from utils.errors.token import RefreshTokenExpiredError

from authlib.integrations.starlette_client import OAuth

from logging import getLogger
logger = getLogger(__name__)

class AuthService():
    def __init__(self):
        self.oauth = OAuth()
        self.oauth.register(
            name='google',
            client_id=settings.GOOGLE_CLIENT_ID,
            client_secret=settings.GOOGLE_CLIENT_SECRET,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration', 
            client_kwargs={"scope": "openid email profile"},
            redirect_uri=f"{settings.server_host}/api/v1/auth/callback/google"
        )
        self.oauth.register(
            name='github',
            client_id=settings.GITHUB_CLIENT_ID,
            client_secret=settings.GITHUB_CLIENT_SECRET,
            authorize_url="https://github.com/login/oauth/authorize",
            access_token_url="https://github.com/login/oauth/access_token",
            redirect_uri=f"{settings.server_host}/auth/callback/github",
            userinfo_endpoint="https://api.github.com/user"
        )
        self.user_repo = user_repo
        self.token_repo = token_repo
        self.redis_client = asyncio.run(get_redis_client()) 
    async def oauth_login_service(self, request, provider: str):
        if provider not in ["google", "github"]:
            raise OAuthProviderNotSupportedError()  

        client = self.oauth.create_client(provider)
        if not client:
            raise OAuthClientError() 
    
        state = create_state()
        request.session['oauth_state'] = state

        redirect_uri = f"{settings.server_host}/api/v1/auth/callback/{provider}"

        return await client.authorize_redirect(request, redirect_uri, state=state)

    async def oauth_callback_service(self, request, provider: str, session) -> TokenLogin:
        state_in_request = request.query_params.get("state")
        state_in_session = request.session.get('oauth_state')
        if not state_in_request or state_in_request != state_in_session:
            raise OAuthStateMismatchError()  
        client = self.oauth.create_client(provider)
        if not client:
            raise OAuthClientError()  
        
        token = await client.authorize_access_token(request)
        user_info = await client.userinfo(token=token)
        email = user_info.get('email')
        user = await self.user_repo.get(session,filters={"email": email})
        if user is None:
            new_user = UserInDB(
                    email=email,
                    full_name=user_info.get('name'),
                    image=user_info.get('picture'),
                    account_type=provider,
                    is_active=True,
                    hashed_password="" 
                )
            user = await  self.user_repo.create(session=session, data=new_user.model_dump())
            
        existing_token = await  self.token_repo.get(session,filters={"user_id": user.id})
        access_token = create_access_token(user)

        if existing_token and existing_token.exp > datetime.now():
            refresh_token = existing_token.refresh_token
        else:
            refresh_token, expire = create_refresh_token()
            new_token = TokenInDB(refresh_token=refresh_token, user_id=user.id, exp=expire)
            if existing_token:
                await  self.token_repo.update(session,filters={"user_id": user.id},data=new_token.model_dump())
            else:
                await  self.token_repo.create(session, data=new_token.model_dump())

        return TokenLogin(token_type="bearer", refresh_token=refresh_token, access_token=access_token)
    
    async def login_service(self, session, data: Login) -> TokenLogin:
        user = await  self.user_repo.get(session, filters={"email": data.username})
       
        if not user or user.account_type != "local" or not is_valid_password(data.password, user.hashed_password):
            raise InvalidCredentialsError()  
        if not user.is_active:
            raise UserAccountInactiveError()  

        existing_token = await  self.token_repo.get(session, filters={"user_id": user.id})
        access_token = create_access_token(user)

        if existing_token and existing_token.exp > datetime.now():
            refresh_token = existing_token.refresh_token
        else:
            refresh_token, expire = create_refresh_token()
            if existing_token:
                await  self.token_repo.update(session, filters={"user_id": user.id}, data={ 'refresh_token': refresh_token, 'exp': expire })
            else:
                await  self.token_repo.create(session,  data={ 'refresh_token': refresh_token, 'exp': expire,'user_id':  user.id })

        return TokenLogin(token_type="bearer", refresh_token=refresh_token, access_token=access_token)    
    
    async def register_service(self, session, data: UserCreate):
        hashed_password = get_password_hash(data.password)

        new_user = UserInDB(
            email=data.email, 
            full_name=data.full_name, 
            hashed_password=hashed_password, 
            image=data.image, 
            role="user", 
            account_type="local", 
            is_active=False, 
        )
        user = await  self.user_repo.create(session, data=new_user.model_dump())
        code_active, exp_active = create_verify_code()
        
        await self.redis_client.setex(f"activate_code:{user.id}", exp_active, code_active) 

        info = InfoEmailSend(email=data.email, name=user.full_name, verification_code=code_active)
        html_content = await render_email_template("register_code.html", **info.model_dump())
        response = await send_email(
            email_to=data.email,
            subject="Your Verification Code",
            html_content=html_content
        )
        if not response:
            raise EmailSendFailureError()  

        return {"message": "Registration successful, verification code sent to your email"}
            

    async def refresh_token_service(self, session, token_data: TokenRefresh):
        result = await token_repo.get(session, filters={"refresh_token": token_data.refresh_token})
        if not result or result.exp < datetime.now() or result.user_id != token_data.user_id:
            raise RefreshTokenExpiredError()  

        user = await  self.user_repo.get(session, filters={"id": result.user_id})
        if  not user.is_active:
            raise UserAccountInactiveError() 

        access_token = create_access_token(user)
        refresh_token = token_data.refresh_token

        return TokenLogin(token_type="bearer", refresh_token=refresh_token, access_token=access_token)    

    async def change_password_service(self, session, data: ChangePassword, current_user: UserBase):
        if not is_valid_password(data.current_password, current_user.password):
            raise InvalidCredentialsError()  

        await  self.user_repo.update(session, filters={"id": current_user.id}, data={"hashed_password": get_password_hash(data.new_password)})

        return {"message": "Password changed successfully"} 

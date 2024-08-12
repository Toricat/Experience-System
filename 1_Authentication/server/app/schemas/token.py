from typing import Literal,Optional


from pydantic import BaseModel

class Token(BaseModel): 
    access_token: str
    token_type: Literal["bearer"]
    refresh_token: Optional[str]
class TokenPayload(BaseModel):
    user_id: Optional[str]
    scopes: list[str] = []
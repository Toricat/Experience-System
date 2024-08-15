from crud.base import CRUDBase
from models.token import Token
from schemas.tokens import TokenInDB, TokenUpdateDB

CRUDToken= CRUDBase[Token,TokenInDB, TokenUpdateDB]
crud_token = CRUDToken(Token)
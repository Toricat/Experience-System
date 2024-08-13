from typing import Literal,Optional
from pydantic import BaseModel

class Token(BaseModel): 
    token_type: Literal["bearer"]
    access_token: str
    refresh_token: Optional[str]
class TokenPayload(BaseModel):
    user_id: Optional[str]

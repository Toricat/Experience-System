from pydantic import BaseModel
class Detail(BaseModel):
    message: str
    code: int
class Message(BaseModel):
    detail: Detail
    class Config:
        from_attributes=True
class InfoEmailSend(BaseModel):
    email: str
    name:str
    verification_code: str        
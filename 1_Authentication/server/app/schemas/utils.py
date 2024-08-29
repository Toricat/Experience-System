from pydantic import BaseModel
class Detail(BaseModel):
    message: str
    code: int
class Message(BaseModel):
    detail: Detail
    class Config:
        from_attributes=True
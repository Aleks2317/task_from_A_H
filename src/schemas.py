from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Response schema for /message/{id}"""
    id: int
    text: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "text": "save user message text"
            }
        }


class ProcessRequest(BaseModel):
    """Request schema for /process"""
    data: str

    class Config:
        schema_extra = {
            "example": {
                "data": "example text"
            }
        }




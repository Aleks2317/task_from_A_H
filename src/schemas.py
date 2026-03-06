from pydantic import BaseModel


class MessageIDRequest(BaseModel):
    """Request schema for /message"""
    message_id: int

    class Config:
        json_encoders = {
            "example": {
                "message_id": 1
            }
        }


class MessageResponse(BaseModel):
    """Response schema for /message/{id}"""
    id: int
    text: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "save user message text"
            }
        }


class ProcessRequest(BaseModel):
    """Request schema for /process"""
    data: str

    class Config:
        json_schema_extra = {
            "example": {
                "data": "example text"
            }
        }




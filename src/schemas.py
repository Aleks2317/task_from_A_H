from pydantic import BaseModel


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


class ProcessResponse(BaseModel):
    """Схема ответа для /process"""
    input: str
    processed: str
    processing_time: str

    class Config:
        json_schema_extra = {
            "example": {
                "input": "test",
                "processed": "Processed: test",
                "processing_time": "0.50s"
            }
        }

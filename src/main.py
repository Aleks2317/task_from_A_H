from typing import AsyncGenerator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db_session import get_db_postgres
from src.models import Message
from src.schemas import MessageResponse, ProcessRequest
from src.logging_config import logger


app = FastAPI(title="API for monitoring", version="1.0")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_postgres():
        yield session



@app.get("/health", response_model=dict)
async def health_status() -> dict:
    """returns status"""
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.get("message/{message_id}", response_model=MessageResponse)
async def get_message_id(message_id: int, db: Session = Depends(get_db)) -> MessageResponse:
    """Get a message by ID from the database
    Arguments:
        message_id: Message ID
        db: Database session (automatically injected)
    Returns:
        MessageResponse: Message object"""

    logger.info(f"Get message {message_id} from database")

    stmt = select(Message).where(Message.id == message_id)
    message = db.scalars(stmt).first()

    if message is None:
        logger.warning("Message not found", message_id=id)
        raise HTTPException(
            status_code=404,
            detail=f"Message with ID {message_id} not found"
        )

    logger.info(
        "Message retrieved successfully",
        message_id=message_id,
        text_length=len(message.text)
    )

    return MessageResponse(id=message.id, text=message.text)


@app.post("/process")
async def process_data(data: str) -> dict:
    """processes data"""
    pass


@app.get("/metrics")
async def get_metrics() -> dict:
    """metrics with Prometheus"""
    pass


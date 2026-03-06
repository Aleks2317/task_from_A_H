import asyncio
import time

from fastapi import FastAPI, Depends, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from src.database.db import create_tables
from src.database.db_session import get_db_postgres
from src.models import Message
from src.schemas import MessageResponse, ProcessRequest, ProcessResponse
from src.seed_data import seed_messages
from src.logging_config import logger
from src.castom_prometeus_metric import measure_latency

app = FastAPI(title="API for monitoring", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untagged=True,
    should_respect_env_var=True,
    env_var_name="ENABLE_METRICS",
)
instrumentator.instrument(app).expose(
    app,
    endpoint="/metrics",
    include_in_schema=True,
)


@app.on_event("startup")
async def startup_event():
    """Initialization at application startup
    Creating tables in the database if they don't exist
    Filling the database with test data"""
    await create_tables()

    await seed_messages()

    logger.info(
        "Application started successfully",
        environment="development"
    )


@app.on_event("shutdown")
async def shutdown_event():
    """Cleaning when the application stops"""
    logger.info("Application shutting down")


@app.get("/health", response_model=dict)
async def health_status() -> dict:
    """returns status"""
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.get("/message/{message_id}", response_model=MessageResponse)
async def get_message_id(message_id: int, db: Session = Depends(get_db_postgres)) -> MessageResponse:
    """Get a message by ID from the database
    Arguments:
        message_id: Message ID
        db: Database session (automatically injected)
    Returns:
        MessageResponse: Message object"""

    logger.info(f"Get message {message_id} from database")

    stmt = select(Message).where(Message.id == message_id)
    result = await db.scalars(stmt)
    message = result.first()

    if message is None:
        logger.warning("Message not found", message_id=message_id)
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


@app.post("/process", response_model=ProcessResponse)
@measure_latency("process")
async def process_data(data: ProcessRequest) -> ProcessResponse:
    """Process data with delay simulation
    Args:
        data: Input data to be processed
    Returns:
        ProcessResponse: Processing result"""
    start_time = time.time()
    logger.info("Processing started", input_length=len(data.data))

    await asyncio.sleep(0.5)

    processing_time = time.time() - start_time

    result = {
        "input": data.data,
        "processed": f"Processed: {data.data}",
        "processing_time": f"{processing_time:.2f}s"
    }

    logger.info(
        "Processing completed",
        input_length=len(data.data),
        processing_time=f"{processing_time:.2f}s",
        status="success"
    )

    return ProcessResponse(**result)

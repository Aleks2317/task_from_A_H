from sqlalchemy import delete

from .database.db_session import async_session_maker
from .models import Message
from .logging_config import logger


async def seed_messages():
    db = async_session_maker()
    try:
        await db.execute(delete(Message))

        test_message = [
            f"Text message#{i}: This is a test message." for i in range(1, 21)
        ]

        for id_, text in enumerate(test_message, start=1):
            message = Message(id=id_, text=text)
            db.add(message)

        await db.commit()
        logger.info(" OK # Seed data inserted successfully (20 messages)")

    except Exception as e:
        logger.error(f" NO # Error inserting seed data: {e}")
        await db.rollback()
    finally:
        await db.close()

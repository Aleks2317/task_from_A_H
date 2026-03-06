from src.database.db_session import async_session_maker
from src.models import Message


async def seed_messages():
    db = await async_session_maker()
    try:
        await db.select(Message).delete()

        test_message = [
            f"Text message#{i}: This is a test message." for i in range(1, 21)
        ]

        for id_, text in enumerate(test_message, start=1):
            message = Message(id=id_, text=text)
            await db.add(message)

        await db.commit()
        print(" OK # Seed data inserted successfully (20 messages)")
    except Exception as e:
        print(f" NO # Error inserting seed data: {e}")
        await db.rollback()


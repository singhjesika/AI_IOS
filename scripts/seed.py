"""
Seed the database with sample data.

Usage:
    cd backend
    python ../scripts/seed.py
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from database import AsyncSessionLocal, init_db
from app.models.user import User
from app.models.task import Task
from app.config.security import hash_password


SAMPLE_USERS = [
    {"name": "Alice Demo",   "email": "alice@demo.com",   "password": "AlicePass1"},
    {"name": "Bob Demo",     "email": "bob@demo.com",     "password": "BobPass12"},
]

SAMPLE_TASKS = [
    {"title": "Review monthly budget",  "priority": "high"},
    {"title": "30-minute workout",      "priority": "medium"},
    {"title": "Read 20 pages",          "priority": "low"},
    {"title": "Prepare weekly plan",    "priority": "high"},
]


async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        user_ids = []
        for u in SAMPLE_USERS:
            user_obj = User(
                name=u["name"],
                email=u["email"],
                hashed_password=hash_password(u["password"]),
            )
            db.add(user_obj)
            await db.flush()
            user_ids.append(user_obj.id)
            print(f"  ✅ User: {u['email']}")

        for uid in user_ids:
            for t in SAMPLE_TASKS:
                db.add(Task(user_id=uid, **t))
            print(f"  ✅ Tasks seeded for user {uid}")

        await db.commit()
    print("\n✅ Seeding complete.")


asyncio.run(seed())
"""
Initialize the database and create all tables.

Usage:
    cd backend
    python ../scripts/init_db.py
"""
import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from database import init_db, engine
from app.models import user, task, memory, subscription   # noqa – registers models


async def main():
    print("Initialising database...")
    await init_db()
    print("✅ All tables created.")
    await engine.dispose()


asyncio.run(main())
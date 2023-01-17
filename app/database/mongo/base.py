from motor.motor_asyncio import AsyncIOMotorClient

from app.database.mongo.client import MongoClient

mc = MongoClient()


async def get_db() -> AsyncIOMotorClient:
    return mc.client

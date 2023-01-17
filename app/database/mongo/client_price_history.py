import datetime
import os

os.environ['TZ'] = 'UTC'

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class MongoClientPriceHistory:

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_CONNSTRING)

    async def insert_price_history(self, crypto, time_frame, limit, info):
        db = self.client[settings.CRYPTO_DB_NAME]
        insert_time = datetime.datetime.now()
        info.update({"insert_time": insert_time})
        await db[crypto][time_frame][limit].insert_one(info)

    async def clear_old_price_history(self, crypto, time_frame, limit='100'):
        db = self.client[settings.CRYPTO_DB_NAME]
        time_to_remove = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        await db[crypto][time_frame][limit].delete_many({"insert_time": {"$lte": time_to_remove}})

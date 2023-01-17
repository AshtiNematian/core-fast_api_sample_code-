import datetime
import os
from app.database.model.algorithms import AlgorithmModel
os.environ['TZ'] = 'UTC'
from motor.motor_asyncio import AsyncIOMotorClient
from app.checker.signal_timeframe_validation import latest_signal_time_frame_verify
from app.core.config import settings


class MongoClient:

    def __init__(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_CONNSTRING)

    async def get_client(self):
        return self.client

    # FIXME convert me to init_db api for first time
    def not_in_db(self, symbol="btcusdt", time_frame="1day"):
        collection = f'{symbol}.{AlgorithmModel.RSI_SMI}.{time_frame}'
        db = self.client
        db_name = db['crypto_db']
        coll = db_name[collection]
        count_documents = coll.count_documents({})
        if count_documents == 0:
            return 1
        else:
            return 0

    async def insert(self, crypto, time_frame, algorithm, info):
        db = self.client[settings.CRYPTO_DB_NAME]
        insert_time = datetime.datetime.now()
        validate = latest_signal_time_frame_verify(info, time_frame)

        if validate or self.not_in_db:
            print(f"signal time frame validated. inserted to db insert_time : {insert_time}")
            info.update({"insert_time": insert_time})
            await db[crypto][algorithm][time_frame].insert_one(info)
        else:
            print(f"signal time not validated for this time frame:")

    async def get_two_latest_actions(self, symbol, time_frame, algorithm):
        db = self.client[settings.CRYPTO_DB_NAME]
        rs = db[symbol][algorithm][time_frame].find().sort("insert_time", -1).limit(2)
        objects = []
        async for row in rs:
            objects.append(row)
        return objects

    async def clear_old_data(self, symbol, time_frame, algorithm):
        db = self.client[settings.CRYPTO_DB_NAME]
        time_to_remove = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        await db[symbol][algorithm][time_frame].delete_many({"insert_time": {"$lte": time_to_remove}})

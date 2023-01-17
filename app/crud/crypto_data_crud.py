from app.core.config import settings


async def get_actions_from_db(symbol, algorithm, time_frame, db):
    rs = db[settings.CRYPTO_DB_NAME][symbol][algorithm][time_frame].find().sort("insert_time", -1).limit(1)
    objects = []
    async for row in rs:
        objects.append(row)
    return objects[0]


async def get_price_history_from_db(symbol, time_frame, limit, db):
    rs = db[settings.CRYPTO_DB_NAME][symbol][time_frame][limit].find().sort("insert_time", -1).limit(1)
    objects = []
    async for row in rs:
        objects.append(row)
    return objects[0]

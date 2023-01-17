from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette import status
from starlette.responses import JSONResponse

from app.crud.crypto_data_crud import get_price_history_from_db
from app.database.mongo.base import get_db

import secrets

from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()
router = APIRouter()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "lpm")
    correct_password = secrets.compare_digest(credentials.password, "123")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/all_data")
async def get_all_data(symbol: str = "adausdt", time_frame="4hour", limit="100",
                       db: AsyncIOMotorClient = Depends(get_db)):
    # username: str = Depends(get_current_username)):
    collection = f'{symbol}.{time_frame}.{limit}'
    db_name = db['crypto_db']
    coll = db_name[collection]
    count_documents = await coll.count_documents({})

    if count_documents != 0:

        data = await get_price_history_from_db(symbol, time_frame, limit, db)

        i = 0
        price_history = []
        while i < 100:
            price_list = [{"date_time": data['info'][i]['Time_'].strftime('%Y-%m-%d %H:%M:%S'),
                           "price_history": data['info'][i]['Close'],
                           "volume": data['info'][i]['Volume'],
                           "Amount": data['info'][i]['Amount']
                           }]
            price_history.append(price_list)
            i += 1

    else:

        price_history = {'price_history': ' There is no such crypto currency'}

    collection_latest_data = f'{symbol}.{time_frame}.1'
    db_name = db['crypto_db']
    coll_latest_data = db_name[collection_latest_data]
    count_documents_latest_data = await coll_latest_data.count_documents({})

    if count_documents_latest_data != 0:
        data_latest_data = await get_price_history_from_db(symbol, time_frame, limit='1', db=db)

        market_cap = float(data_latest_data['info'][0]['Close']) * float(data_latest_data['info'][0]['Volume'])
        latest_data = {
            "latest_price": data_latest_data['info'][0]['Close'],
            "volume": data_latest_data['info'][0]['Volume'],
            "amount": data_latest_data['info'][0]['Amount'],
            "market_cap": market_cap}

    else:

        latest_data = {'latest_data': ' There is no such crypto currency'}

    return JSONResponse(status_code=status.HTTP_200_OK, content=
    {
        "symbol": symbol,
        "time_frame": time_frame,
        "latest_data": latest_data,
        "price_history": price_history

    })

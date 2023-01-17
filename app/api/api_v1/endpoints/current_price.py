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


@router.get("/current_price")
async def get_current_price(symbol: str = "adausdt", time_frame="4hour", limit="100",
                            db: AsyncIOMotorClient = Depends(get_db)):
    # username: str = Depends(get_current_username)):
    collection = f'{symbol}.{time_frame}.{limit}'
    db_name = db['crypto_db']
    coll = db_name[collection]
    count_documents = await coll.count_documents({})

    if count_documents != 0:

        data = await get_price_history_from_db(symbol, time_frame, limit, db)
        result = {"date_time": data['info'][99]['Time_'].strftime('%Y-%m-%d %H:%M:%S'),
                  "current_price": data['info'][99]['Close'],
                  "volume": data['info'][99]['Volume'],
                  "amount": data['info'][99]['Amount']
                  }



    else:

        result = {'result': ' There is no such crypto currency'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=
    {
        "symbol": symbol,
        "time_frame": time_frame,
        "body": result

    })

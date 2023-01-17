from fastapi import APIRouter, Depends, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse
from app.analysis.rsi_smi import RSISMI
from app.coinex.fetch_kline_data import FetchKLineData
from app.crud.crypto_data_crud import get_actions_from_db
from app.database.model.algorithms import AlgorithmModel
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


@router.get("/fresh")
async def calculate_rsi_smi_algorithm(symbol: str = "adausdt", time_frame="1hour", limit=100,
                                      # username: str = Depends(get_current_username)
                                      ):
    data = FetchKLineData(symbol=symbol, type=time_frame, limit=limit).get()
    rsi_smi = RSISMI(data)
    result = rsi_smi.calculate()
    return JSONResponse(status_code=status.HTTP_200_OK, content=
    {
        "message": f"return rsi smi strategy for {symbol} in {time_frame} limited by : {limit}",
        "symbol": symbol,
        "time_frame": time_frame,
        "limit": limit,
        "body": result
    })


@router.get("/db")
async def get_rsi_smi_algorithm(symbol: str = "adausdt", time_frame="1hour", db: AsyncIOMotorClient = Depends(get_db),
                                # username: str = Depends(get_current_username)
                                ):
    collection = f'{symbol}.{AlgorithmModel.RSI_SMI}.{time_frame}'
    db_name = db['crypto_db']
    coll = db_name[collection]

    count_documents = await coll.count_documents({})

    if count_documents != 0:

        data = await get_actions_from_db(symbol, AlgorithmModel.RSI_SMI, time_frame, db)
        result = {
            'actions': data['action_df'],
            'back_test': data['back_test'],
            'insert_time': str(data['insert_time'])
        }

    else:

        result = {'result': ' There is no such crypto currency'}
    return JSONResponse(status_code=status.HTTP_200_OK, content=
    {
        "message": f"return RSI SMI strategy for {symbol} in {time_frame}",
        "symbol": symbol,
        "time_frame": time_frame,
        "body": result
    })

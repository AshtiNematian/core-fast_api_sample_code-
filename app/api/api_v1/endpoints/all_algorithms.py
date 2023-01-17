from fastapi import APIRouter, Depends, Path, status, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse

from app.crud.crypto_data_crud import get_actions_from_db
from app.database.model.algorithms import AlgorithmModel
from app.database.mongo.base import get_db
import secrets

from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter()
security = HTTPBasic()


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


@router.get("/db")
async def get_all_algorithms(symbol: str = "btcusdt", time_frame="1day", db: AsyncIOMotorClient = Depends(get_db), ):
    # username: str = Depends(get_current_username)):
    """ MACD """

    db_name = db['crypto_db']
    collection_macd = f'{symbol}.{AlgorithmModel.MACD}.{time_frame}'
    coll_macd = db_name[collection_macd]

    count_documents_macd = await coll_macd.count_documents({})

    if count_documents_macd != 0:

        data_macd = await get_actions_from_db(symbol, AlgorithmModel.MACD, time_frame, db)
        result_macd = {"message": f"return MACD strategy for {symbol} in {time_frame}",
                       'actions': data_macd['action_df'],
                       'back_test': data_macd['back_test'],
                       'insert_time': str(data_macd['insert_time'])}
    else:

        result_macd = {"message": f"return MACD strategy for {symbol} in {time_frame}",
                       'result_macd': ' There is no such crypto currency'}

    """ RSI """

    collection_rsi = f'{symbol}.{AlgorithmModel.RSI}.{time_frame}'
    coll_rsi = db_name[collection_rsi]

    count_documents_rsi = await coll_rsi.count_documents({})

    if count_documents_rsi != 0:

        data_rsi = await get_actions_from_db(symbol, AlgorithmModel.RSI, time_frame, db)
        result_rsi = {"message": f"return RSI strategy for {symbol} in {time_frame}",
                      'actions': data_rsi['action_df'],
                      'back_test': data_rsi['back_test'],
                      'insert_time': str(data_rsi['insert_time'])
                      }

    else:

        result_rsi = {"message": f"return RSI strategy for {symbol} in {time_frame}",
                      'result_rsi': ' There is no such crypto currency'}

    """ RSI_SMI """
    collection_rsi_smi = f'{symbol}.{AlgorithmModel.RSI_SMI}.{time_frame}'
    coll_rsi_smi = db_name[collection_rsi_smi]

    count_documents_rsi_smi = await coll_rsi_smi.count_documents({})

    if count_documents_rsi_smi != 0:

        data_rsi_smi = await get_actions_from_db(symbol, AlgorithmModel.RSI_SMI, time_frame, db)
        result_rsi_smi = {
            "message": f"return RSI SMI strategy for {symbol} in {time_frame}",
            'actions': data_rsi_smi['action_df'],
            'back_test': data_rsi_smi['back_test'],
            'insert_time': str(data_rsi_smi['insert_time'])
        }

    else:

        result_rsi_smi = {"message": f"return RSI SMI strategy for {symbol} in {time_frame}",
                          'result': ' There is no such crypto currency'}

    """ STOCH_RSI """

    collection_stoch_rsi = f'{symbol}.{AlgorithmModel.STOCH_RSI}.{time_frame}'
    coll_stoch_rsi = db_name[collection_stoch_rsi]

    count_documents_stoch_rsi = await coll_stoch_rsi.count_documents({})

    if count_documents_stoch_rsi != 0:

        data_stoch_rsi = await get_actions_from_db(symbol, AlgorithmModel.STOCH_RSI, time_frame, db)
        result_stoch_rsi = {
            "message": f"return STOCH_RSI strategy for {symbol} in {time_frame}",
            'actions': data_stoch_rsi['action_df'],
            'back_test': data_stoch_rsi['back_test'],
            'insert_time': str(data_stoch_rsi['insert_time'])
        }

    else:

        result_stoch_rsi = {"message": f"return STOCH_RSI strategy for {symbol} in {time_frame}",
                            'result': ' There is no such crypto currency'}

    return JSONResponse(status_code=status.HTTP_200_OK, content=
    {

        "symbol": symbol,
        "time_frame": time_frame,
        "result_MACD": result_macd,
        "result_RSI": result_rsi,
        "result_RSI_SMI": result_rsi_smi,
        "result_STOCH_RSI": result_stoch_rsi
    })

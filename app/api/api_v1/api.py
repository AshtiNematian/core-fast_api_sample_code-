from fastapi import APIRouter

from app.api.api_v1.endpoints import rsi, rsi_sma, macd, stoch_rsi, atr, all_algorithms, price_history, \
    market_list, all_data, current_price, xical

api_router = APIRouter()
api_router.include_router(rsi.router, prefix="/rsi", tags=["rsi"])
api_router.include_router(macd.router, prefix="/macd", tags=["macd"])
api_router.include_router(stoch_rsi.router, prefix="/stoch_rsi", tags=["stoch_rsi"])
api_router.include_router(rsi_sma.router, prefix="/rsi_smi", tags=["rsi_smi"])
api_router.include_router(atr.router, prefix="/atr", tags=["atr"])
api_router.include_router(all_algorithms.router, prefix="/all_algorithms", tags=["all_algorithms"])
api_router.include_router(price_history.router, prefix="/price_history", tags=["price_history"])
api_router.include_router(market_list.router, prefix="/market_list", tags=["market_list"])
api_router.include_router(all_data.router, prefix="/all_data", tags=["all_data"])
api_router.include_router(current_price.router, prefix="/current_price", tags=["current_price"])
api_router.include_router(xical.router, prefix="/xical", tags=["xical"])

from fastapi import APIRouter, Depends, Path, status
from starlette.responses import JSONResponse

from app.analysis.atr import ATR
from app.coinex.fetch_kline_data import FetchKLineData


router = APIRouter()



@router.get("/fresh")
async def calculate_atr_algorithm(symbol: str = "btcusdt", time_frame="1day", limit=100):
    data = FetchKLineData(symbol=symbol, type=time_frame, limit=limit).get()
    atr = ATR(data)
    result = atr.calculate()
    return JSONResponse(status_code=status.HTTP_200_OK, content=
    {
        "message": f"return macd strategy for {symbol} in {time_frame} limited by : {limit}",
        "symbol": symbol,
        "time_frame": time_frame,
        "limit": limit,
        "body": result
    })



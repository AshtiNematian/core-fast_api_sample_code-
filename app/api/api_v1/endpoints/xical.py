from fastapi import APIRouter, status
from starlette.responses import JSONResponse
from app.xical.fetchers import fetch_price_history, fetch_technical_table, fetch_price_history_symbol, \
    fetch_meta_data_symbol, fetch_all_tick_distinct

router = APIRouter()


@router.get("/xical_price_history/")
async def xical_price_history():
    print('salam')
    data = fetch_price_history().fetch()
    # price_history_ins = fetch_price_history()
    print(data)
    return JSONResponse(status_code=status.HTTP_200_OK, content=
    {
        "xical_price_history": data['data']
    })


@router.get("/xical_technical_table/")
async def xical_technical_table():
    technical_table_ins = fetch_technical_table()
    print(technical_table_ins)
    return JSONResponse(technical_table_ins, status_code=status.HTTP_200_OK)


@router.get("/xical_price_history_symbol/")
async def xical_price_history_symbol():
    price_history_symbol_ins = fetch_price_history_symbol()
    print(price_history_symbol_ins)
    return JSONResponse(price_history_symbol_ins, status_code=status.HTTP_200_OK)


@router.get("/xixal_meta_data_symbol/")
async def xixal_meta_data_symbol():
    meta_data_symbol_ins = fetch_meta_data_symbol()
    print(meta_data_symbol_ins)
    return JSONResponse(meta_data_symbol_ins, status_code=status.HTTP_200_OK)


@router.get("/all_tick_distinct/")
async def all_tick_distinct():
    all_tick_distinct_ins = fetch_all_tick_distinct()
    print(all_tick_distinct_ins)
    return JSONResponse(all_tick_distinct_ins, status_code=status.HTTP_200_OK)



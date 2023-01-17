import asyncio

from app.coinex.fetch_kline_data import FetchKLineData

from app.database.mongo.client_price_history import MongoClientPriceHistory

mc = MongoClientPriceHistory()


async def save_hour_1(args):
    symbol = args.split(",")[0]
    time_frame = args.split(",")[1]
    while True:
        info = FetchKLineData(symbol=symbol, type=time_frame, limit='100').get()

        info['Time_'] = info.index
        info_dataframe = {'info': info[['Time_', 'Close', 'Volume', 'Amount']].to_dict(orient='records')}
        await mc.insert_price_history(crypto=symbol, time_frame=time_frame, limit='100', info=info_dataframe)
        await mc.clear_old_price_history(crypto=symbol, time_frame=time_frame, limit='100')
        await asyncio.sleep(6)


async def repeat(func, *args, **kwargs):
    while True:
        await asyncio.gather(
            func(*args),
        )


async def main():
    t1 = asyncio.ensure_future(repeat(save_hour_1, "adausdt,4hour"))
    t2 = asyncio.ensure_future(repeat(save_hour_1, "adausdt,1day"))

    t3 = asyncio.ensure_future(repeat(save_hour_1, "btcusdt,4hour"))
    t4 = asyncio.ensure_future(repeat(save_hour_1, "btcusdt,1day"))

    t5 = asyncio.ensure_future(repeat(save_hour_1, "ethusdt,4hour"))
    t6 = asyncio.ensure_future(repeat(save_hour_1, "ethusdt,1day"))

    t7 = asyncio.ensure_future(repeat(save_hour_1, "xrpusdt,4hour"))
    t8 = asyncio.ensure_future(repeat(save_hour_1, "xrpusdt,1day"))

    t9 = asyncio.ensure_future(repeat(save_hour_1, "dogeusdt,4hour"))
    t10 = asyncio.ensure_future(repeat(save_hour_1, "dogeusdt,1day"))

    t11 = asyncio.ensure_future(repeat(save_hour_1, "shibausdt,4hour"))
    t12 = asyncio.ensure_future(repeat(save_hour_1, "shibausdt,1day"))

    await t1
    await t2
    await t3
    await t4
    await t5
    await t6
    await t7
    await t8
    await t9
    await t10
    await t11
    await t12



loop = asyncio.get_event_loop()
loop.run_until_complete(main())


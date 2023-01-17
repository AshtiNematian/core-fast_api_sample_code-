from app.analysis.macd import MACD
from app.database.model.algorithms import AlgorithmModel

print("start btc")
import asyncio
import datetime

import time

from app.checker.change_signal import check_signal_changed
from app.coinex.fetch_kline_data import FetchKLineData
from app.database.mongo.client import MongoClient
from app.telegram.send_message import send_message_on_telegram, send_monitor_message

# symbol = "btcusdt"
mc = MongoClient()


async def save_hour_1(args):
    symbol = args.split(",")[0]
    time_frame = args.split(",")[1]
    while True:
        price_history = FetchKLineData(symbol=symbol, type=time_frame, limit=100).get()
        indicator = MACD(price_history)
        info = indicator.calculate()
        await mc.insert(crypto=symbol, time_frame=time_frame, algorithm=AlgorithmModel.MACD, info=info)
        await mc.clear_old_data(symbol=symbol, algorithm=AlgorithmModel.MACD, time_frame=time_frame)
        await change_checker(symbol, time_frame)
        await asyncio.sleep(6)


async def change_checker(symbol, time_frame):
    two_latest_actions = await mc.get_two_latest_actions(symbol=symbol, algorithm=AlgorithmModel.MACD,
                                                         time_frame=time_frame)
    check = check_signal_changed(two_latest_actions)
    if check != 0:
        message = f"New signal for %23MACD : %23{symbol} in %23{time_frame},\n" \
                  f"side : {check['action']}, close : {check['close']}, \n time : {check['date']}"
        # send_message_on_telegram(message)

    else:
        message = f"latest check in {datetime.datetime.now()} for %23MACD : %23{symbol} in %23{time_frame} "
        # send_monitor_message(message)
        print("no new signal")


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

import datetime
import os
import time

from pytz import timezone

from app.coinex.fetch_kline_data import FetchKLineData

os.environ['TZ'] = 'UTC'


def is_time_format(input, format):
    try:
        time.strptime(input, format)
        return True
    except ValueError:
        return False


def latest_signal_time_frame_verify(info, time_frame):
    if len(info['action_df']) < 1:
        return 0
    signal_date = info['action_df'][-1]['date']

    if is_time_format(signal_date, '%Y-%m-%d %H:%M:%S.%f'):
        signal_date = signal_date
    elif is_time_format(signal_date, '%Y-%m-%d %H:%M:%S'):
        signal_date = signal_date + '.00'
    elif is_time_format(signal_date, '%Y-%m-%d %H:%M'):
        signal_date = signal_date + ':00.00'
    elif is_time_format(signal_date, '%Y-%m-%d %H'):
        signal_date = signal_date + ':00:00.00'
    else:
        signal_date = signal_date + ' ' + '00:00:00.00'

    signal_date = datetime.datetime.strptime(signal_date, '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.datetime.now(timezone("UTC"))
    time_delta = now - signal_date.astimezone()
    if time_frame == "1min":
        if time_delta.seconds > 60:
            return 1  # validated
        else:
            return 0  # invalidated
    elif time_frame == "3min":
        if time_delta.seconds > 3 * 60:
            return 1  # validated
        else:
            return 0  # invalidated
    elif time_frame == "30min":
        if time_delta.seconds > 30 * 60:
            return 1  # validated
        else:
            return 0  # invalidated
    elif time_frame == "1hour":
        if time_delta.seconds > 60 * 60:
            return 1  # validated
        else:
            return 0  # invalidated
    elif time_frame == "4hour":
        if time_delta.seconds > 4 * 60 * 60:
            return 1  # validated
        else:
            return 0  # invalidated
    elif time_frame == "1day":
        if time_delta.seconds > 24 * 60 * 60:
            return 1  # validated
        else:
            return 0  # invalidated




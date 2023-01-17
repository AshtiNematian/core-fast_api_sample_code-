import requests
from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Tehran')

raw_TS = datetime.now(IST)
curr_date = raw_TS.strftime("%d-%m-%Y")
curr_time = raw_TS.strftime("%H-%M-%S")

telegram_auth_token = "5010992215:AAHBD2iY7rZF9be7YI2pqLpHgb1JP3QF8_Q"
telegram_group_id = "xical123"


# msg = f"Message received on {curr_date} at {curr_time}"
# 1023027474:AAE1AQq-0jE32e3TgDe4riSvBR7eY5SuviY -> actor_manager_bot

def send_message_on_telegram(message, telegram_group_id="xical123"):

    telegram_auth_token = "5010992215:AAHBD2iY7rZF9be7YI2pqLpHgb1JP3QF8_Q"
    telegram_group_id = "xical123"
    telegram_api_url = f"https://api.telegram.org/bot{telegram_auth_token}/sendMessage?chat_id=@{telegram_group_id}&text={message}"

    tel_resp = requests.get(telegram_api_url)

    if tel_resp.status_code == 200:
        print("horaaaaaaa:", datetime.now())

    else:
        print(f" {tel_resp} don't send:", datetime.now())


def send_monitor_message(message):
    telegram_auth_token = "1023027474:AAE1AQq-0jE32e3TgDe4riSvBR7eY5SuviY"
    telegram_group_id = "xical_monitor"
    telegram_api_url = f"https://api.telegram.org/bot{telegram_auth_token}/sendMessage?chat_id=@{telegram_group_id}&text={message}"
    tel_resp = requests.get(telegram_api_url)
    if tel_resp.status_code != 200:
        print(f"error in send msg tlg {tel_resp}")
    else:
        print(f"send msg to tlg {message}")



#!/usr/bin/env python
import requests
from config.cfg import TG_TOKEN  # ,TG_API

TG_API = "https://api.telegram.org/bot"


def main(msg, chat_id, msg_type=""):
    TOKEN = TG_TOKEN
    API_URL = TG_API

    emoji = {
        'critical': "\U0001F198",
        'ok': "\U00002705"
    }
    if msg_type == 'HARD':
        MESSAGE = emoji['critical'] + msg
    elif msg_type == 'OK':
        MESSAGE = emoji['ok'] + msg
    else:
        MESSAGE = msg
    r = requests.get('%s%s/sendMessage?chat_id=%d&text=%s' % (API_URL, TOKEN, int(chat_id), MESSAGE))
    return r.text

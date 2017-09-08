#!/usr/bin/env python
import requests
import json

CLIENT_ID = 'SKYPE_CLIENT_ID'
CLIENT_SECRET = 'SKYPE_CLIENT_SECRET'


def get_access_token(client_id, client_secret):
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }
    r = requests.post("https://login.microsoftonline.com/common/oauth2/v2.0/token", data=payload)
    try:
        response = json.loads(r.text)
        return response['access_token']
    except:
        return False


def send_message(token, skype_id, message, type):
    if type == 'direct':
        URL = "https://apis.skype.com/v2/conversations/8:{}/activities".format(skype_id)
    if type == 'chat':
        URL = "https://apis.skype.com/v2/conversations/19:{}/activities".format(skype_id)
    headers = dict(Authorization='Bearer ' + token)
    data = json.dumps(dict(message=dict(content=message))).encode()
    r = requests.post(URL, data=data, headers=headers)
    return r.text, r.status_code


def main(message, skype_id):
    TOKEN = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if TOKEN:
        conversation_type = 'chat' if 'thread.skype' in skype_id else 'direct'
        return send_message(TOKEN, skype_id, message, conversation_type)

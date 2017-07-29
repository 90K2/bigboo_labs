import hashlib
import json
from gevent import monkey
monkey.patch_all()
from bottle import Bottle, run, request

from transfer_validation import validation
app = Bottle()

secret = 'your yandex secret'

@app.route('/webhook', method='POST')
def web_payload():
    payload_str = dict(request.forms)
    # print(payload_str)
    if validation(payload_str, secret):
        return {'received': 'true'}


if __name__ == '__main__':
    run(app=app, host='0.0.0.0', port=8044, debug=True, server='gevent')

import json
from websocket import create_connection
import ssl
import time
import requests

from connect import*


send_request({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "requestAccess",
    "params": {
        "clientId": "NZjtUNCOiaPP7gMkNSucchM7jATzNY386Aq2hMI7",
        "clientSecret": "526x2Afu46XG6eMMfkJ7Him3QKszzys9Bs4ABKcAVhLa6xfIfSbTs1ZmziBqYcOHWvup3N9XqBo9GbhMAqh2sWSGKQgj5k30PQUwocFaq1haP4eb3oUKMlUp70ZmoOG9"
    }
}))

result = ws.recv()
result_dic = json.loads(result)

ws.send(json.dumps({
    "id": 4,
    "jsonrpc": "2.0",
    "method": "authorize",
    "params": {
        "clientId": "NZjtUNCOiaPP7gMkNSucchM7jATzNY386Aq2hMI7",
        "clientSecret": "526x2Afu46XG6eMMfkJ7Him3QKszzys9Bs4ABKcAVhLa6xfIfSbTs1ZmziBqYcOHWvup3N9XqBo9GbhMAqh2sWSGKQgj5k30PQUwocFaq1haP4eb3oUKMlUp70ZmoOG9",
        "debit": 500
    }
}))

result = ws.recv()
result_dic = json.loads(result)
auth = result_dic['result']['cortexToken']

ws.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "createSession",
    "params": {
        "cortexToken": auth,
        "headset": "INSIGHT-A1D2007D",
        "status": "active"
    }
}))

result = ws.recv()
result_dic = json.loads(result)
print('create session result ', json.dumps(result_dic, indent=4))
session_id = result_dic['result']['id']

ws.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "setupProfile",
    "params": {
        "cortexToken": auth,
        "headset": "INSIGHT-A1D2007D",
        "profile": "Asad",
        "status": "load"
    }
}))

print(ws.recv())

input_signals = ["com", "mot"]  #TODO: Change this to data we need to use
ws.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "subscribe",
    "params": {
        "cortexToken": auth,
        "session": session_id,
        "streams": input_signals
    }
}))

print('\n')
print(ws.recv())

while True:
    mental_command = json.loads(ws.recv())
    for input in input_signals:
        try:
            print(mental_command[input])
        except KeyError:
            continue

import json
from websocket import create_connection
import ssl
import time
import requests

ws = create_connection("wss://localhost:6868", sslopt={"cert_reqs": ssl.CERT_NONE})

ws.send(json.dumps({
    "id": 1,
    "jsonrpc": "2.0",
    "method": "queryHeadsets"
}))

connection = json.loads(ws.recv())
headset_id = connection["result"][0]["id"]

print(connection, end = '\n\n')
print(headset_id)
# if connection["result"]["id"]

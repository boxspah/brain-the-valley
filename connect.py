import json
from websocket import create_connection
import ssl
import time
import requests

ws = create_connection("wss://localhost:6868", sslopt={"cert_reqs": ssl.CERT_NONE})


def recieve_packet():
    """
    Gets a packet form the headset, a json packet should probably be sent first
    @returns the packet recieved
    """
    return json.loads(ws.recv())


def send_request(json_block, recieve_print_result=False):
    """
    Sends a json packet to the headset and prints the recieved result
    @param json_block The json packet to send
    @param recieve_print_result wether the result should be recieved and printed
    """
    ws.send(json.dumps(json_block))
    if recieve_print_result:
        print(recieve_packet())


send_request(
    {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "queryHeadsets"
    }
)

connection = recieve_packet()

if not len(connection["result"]):
    print("Headset not found")
    exit(0)

headset_id = connection["result"][0]["id"]

print(connection, end='\n\n')
print(headset_id)

send_request(
    {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "controlDevice",
        "params": {
            "command": "connect",
            "headset": headset_id
        }
    }
)

connection = json.loads(ws.recv())
print(connection)

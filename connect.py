import json
from websocket import create_connection
import ssl
import time
import requests
import warnings

ws = create_connection("wss://localhost:6868", sslopt={"cert_reqs": ssl.CERT_NONE})


def recieve_packet():
    """
    Gets a packet form the headset, a json packet should probably be sent first
    @returns the packet recieved
    """
    return json.loads(ws.recv())


def send_request(json_block, recieve_result=False):
    """
    Sends a json packet to the headset and prints the recieved result
    @param json_block The json packet to send
    @param recieve_result wether the result should be recieved
    """
    ws.send(json.dumps(json_block))
    if recieve_result:
        return recieve_packet()


def connect_to_headset():
    """
    Connects to headset
    @returns the connection result if successful, error 400 if failed
    """

    connect_tries = 0
    while True:
        try:
            send_request(
                {
                    "id": 1,
                    "jsonrpc": "2.0",
                    "method": "queryHeadsets"
                }
            )
            connect = recieve_packet()
            connect_tries += 1
            time.sleep(0.5)
            if connect_tries > 10:
                raise TimeoutError
            if not len(connect["result"]):
                raise ConnectionError
            return connect
        except ConnectionError:
            print("Headset not found")
            continue
        except TimeoutError:
            print("Too many failed Attempts")
            return 400
        except Exception(e):
            print(e)
            return e


connection = connect_to_headset()

if connection == Exception or connection == 400:  # checks whether to continue with the program
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

connection = recieve_packet()
print(connection)

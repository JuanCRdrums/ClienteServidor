import zmq
import json
import os

ctx = zmq.Context()
client = ctx.socket(zmq.REP)
client.bind("tcp://*:5555")

while True:
    m = client.recv_string()
    list = m.split(".")
    name = list[0]
    nameToFind = name + "1.mp3"
    data = json.load("Proxy/partes.json")
    print(data)
    client.send_string(nameToFind)

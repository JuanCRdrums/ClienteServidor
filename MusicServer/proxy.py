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
    with open("Proxy/partes.json") as fjson:
        data = json.load(fjson)
        try:
            server = data[m][0]
            parts = data[m][1]
        except:
            server = 0
            parts = 0 #esto es en caso de que el archivo no exista

    if server == 0:
        client.send_string("El archivo no existe")
    else:
        client.send_string(str(server))

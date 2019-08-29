#!usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import json
import os

ctx = zmq.Context()
client = ctx.socket(zmq.REP)
client.bind("tcp://*:5555")

server1 = ctx.socket(zmq.REQ)
server1.connect("tcp://localhost:5556")

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
    elif server == 1:
        client.send_string(str(parts))
        for i in range(1,parts):
            nameFile = name + str(i) + ".mp3"
            server1.send_string(nameFile)
            file = server1.recv()
            ok = client.recv_string()
            client.send(file)

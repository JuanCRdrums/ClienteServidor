#!usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import os


ctx = zmq.Context()
s = ctx.socket(zmq.REP)
s.bind("tcp://*:5557")

while True:
    nameFile = s.recv_string()
    path = "Server2/" + nameFile
    with open(path,"rb") as f:
        contents = f.read()
        s.send(contents)

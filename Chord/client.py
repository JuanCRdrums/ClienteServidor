#!usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import os
import subprocess
import uuid
import string
import random
import hashlib
import sys

if len(sys.argv) != 4:
    print("ERROR: You have to pass 3 console arguments: Node ip, node port and name of file")
    sys.exit()

ip = sys.argv[1]
port = sys.argv[2]
file = sys.argv[3]
address = "tcp://" + ip + ":" + port

ctx = zmq.Context()
toNode = ctx.socket(zmq.REQ)
toNode.connect(address)

toNode.send_string(file)
answer = toNode.recv_json()
toNode.send(b'')
contents = toNode.recv()
print(answer['name'], " recieved")

with open("Downloads/" + answer['name'],'wb') as f:
    f.write(contents)

print("File ", answer['name'], " stored in Downloads directory")

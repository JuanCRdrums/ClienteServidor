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

def hashFile(name):
    hash = hashlib.sha1(name.encode('utf-8'))
    hex = hash.hexdigest()
    value = int(hex,16) % 160
    return value

def inInterval(interval,value):
    list = []
    if interval[0] < interval[1]:
        for i in range(interval[0],interval[1]):
            list.append(i)
    else:
        for i in range(interval[0],256):
            list.append(i)
        for i in range(0,interval[1]):
            list.append(i)

    if value in list:
        return True
    else:
        return False



def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
#
# print(sys.argv)
if len(sys.argv) != 8:
    print("ERROR: You have to pass 7 console arguments: Port to listen predeccesor, ip address of succesor, port to succesor, port to listen succesot, ip of predeccesor, port to predeccesor and port to listen clients")
    sys.exit()

portPred = sys.argv[1]
ipSucc = sys.argv[2]
portSucc = sys.argv[3]
ipPred = sys.argv[4]
portRPred = sys.argv[5]
portRSucc = sys.argv[6]
portClient = sys.argv[7]

addPred = "tcp://*:" + portPred
addSucc = "tcp://" + ipSucc + ":" + portSucc

addRPred = "tcp://" + ipPred + ":" + portRPred
addRSucc = "tcp://*:" + portRSucc


ctx = zmq.Context()
succ = ctx.socket(zmq.REQ)
succ.connect(addSucc)

pred = ctx.socket(zmq.REP)
pred.bind(addPred)

Rpred = ctx.socket(zmq.REQ)
Rpred.connect(addRPred)

Rsucc = ctx.socket(zmq.REP)
Rsucc.bind(addRSucc)

toClient = ctx.socket(zmq.REP)
addClient = "tcp://*:" + portClient
toClient.bind(addClient)




mac = str(hex(uuid.getnode()))
rand = randomString(10)
hash = hashlib.sha1((mac+rand).encode('utf-8'))
hex = hash.hexdigest()
value = int(hex,16) % 160


valPred = "0"
succ.send_string(str(value))
valPred = pred.recv_string()
pred.send(b'')
succ.recv()
intPred = int(valPred)
interval = [intPred,value]

print("Value: " + str(value))
print("Predeccesor value: " + str(intPred))
print("Interval: [" + str(interval[0]) + " - " + str(interval[1]) + ")")

poller = zmq.Poller()
poller.register(toClient,zmq.POLLIN)
poller.register(pred,zmq.POLLIN)
poller.register(Rsucc,zmq.POLLIN)



while True:
    socks = dict(poller.poll())
    if toClient in socks:
        nameFile = toClient.recv_string()
        toSend = {}
        toSend[value] = nameFile
        print("Value to find: ",nameFile)
        succ.send_json(toSend)
        succ.recv()

    if pred in socks:
        recv = pred.recv_json()
        src = []
        s = []
        items = recv.items()
        for item in items:
            src.append(item[0]),s.append(item[1])
        print("Forwarded value: ",s[0])
        pred.send(b'')
        if(inInterval(interval,hashFile(s[0]))):
            print("Eureka from ",src[0])
            answer = {}
            answer['src'] = value
            answer['dest'] = src[0]
            answer['value'] = s[0]
            with open(s[0],"rb") as f:
                contents = f.read()
            Rpred.send_json(answer)
            Rpred.recv()
            Rpred.send(contents)
            Rpred.recv()
            continue
        succ.send_json(recv)
        succ.recv()

    if Rsucc in socks:
        recv = Rsucc.recv_json()
        Rsucc.send(b'')
        contents = Rsucc.recv()
        Rsucc.send(b'')
        if(int(recv['dest']) == value):
            print(recv['value']," recieved by ",recv['src'])
            sentClient = {}
            sentClient['name'] = recv['value']
            toClient.send_json(sentClient)
            toClient.recv()
            toClient.send(contents)
            continue
        Rpred.send_json(recv)
        Rpred.recv()
        Rpred.send(contents)
        Rpred.recv()
# fingerTable = {}
# proxy = ctx.socket(zmq.REQ)
# #proxy.connect("tcp://localhost:6060")
#
# fingerTable = makeFingerTable(pred,succ,proxy,value)
# print(fingerTable)
# print(req)
# if inInterval(interval,int(req[req.keys()[0]])):
#     print(req[req.keys()[0]])

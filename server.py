import zmq
import json

ctx = zmq.Context()
s = ctx.socket(zmq.REP)
s.bind("tcp://*:5555")

while True:
    d = s.recv_json()
    print("Operación {} operando {} operando {}".format(d["operacion"], d["op1"], d["op2"]))
    resp = 0
    if d["operacion"] == "suma":
        resp = str(d["op1"] + d["op2"])
    elif op == d["operacion"] == "resta":
        resp = str(d["op1"] + d["op2"])
    else:
        resp = "0"
    s.send_string(resp)

print("Esto no deberia aparecer")

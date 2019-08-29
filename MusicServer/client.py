import zmq
import os


ctx = zmq.Context()
s = ctx.socket(zmq.REQ)
s.connect("tcp://localhost:5555")
file = "Amoroso (bajo).mp3"
s.send_string(file)
m = s.recv_string()
print(m)

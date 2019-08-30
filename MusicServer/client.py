#!usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import os
import subprocess


ctx = zmq.Context()
s = ctx.socket(zmq.REQ)
s.connect("tcp://localhost:5555")
file = "Fix you.mp3"
with open("Client/" + file,"ab") as f:
    s.send_string(file)
    m = s.recv_string()
    if m == "El archivo no existe":
        print(m)
        os.remove("Client/" + file)
    else:
        parts = int(m)
        s.send_string("ok")
        for i in range(parts):
            contents = s.recv()
            f.write(contents)
            s.send_string("ok")
        subprocess.call(["xdg-open","Client/" + file])

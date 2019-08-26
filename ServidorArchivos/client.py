import zmq
import os


ctx = zmq.Context()
s = ctx.socket(zmq.REQ)
s.connect("tcp://localhost:5555")
filename = "Ensamble.pdf"
with open(filename,"rb") as f:
    size = os.path.getsize(filename)
    for i in range(0,size,500000):
        f.seek(i)
        contents = f.read(500000)
        s.send_multipart([filename.encode("utf-8"), contents])
        m = s.recv_string()



""" Pendiente
Transmisión por partes y almacenamiento de archivos por shal
"""

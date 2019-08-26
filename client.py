import zmq
import json

ctx = zmq.Context()
s = ctx.socket(zmq.REQ)
s.connect("tcp://localhost:5555")

d = {"operacion": "suma", "op1": 100, "op2": 455}
s.send_json(d)
m = s.recv_string()
print("Recibi: {}".format(m))

"""
Tarea:
Hacer un servidor de archivos. Debe soportar subir y descargar archivos de cualquier
tipo
"""

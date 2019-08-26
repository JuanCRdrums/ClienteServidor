import zmq


ctx = zmq.Context()
s = ctx.socket(zmq.REP)
s.bind("tcp://*:5555")

def store(message, filename):
    with open(filename,"ab") as f:
        f.write(message)

while True:
    name, b = s.recv_multipart()
    store(b,"Servidor/" + str(name))
    s.send_string("ok")

print("Esto no deberia aparecer")

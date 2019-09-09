import sys
import time
import zmq

context = zmq.Context()

work = context.socket(zmq.PULL)
work.connect("tcp://localhost:5557")

# Socket to send messages to
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

dot = 0
# Process tasks forever
while True:
    s = work.recv_json()
    print(s)
    X = s["x"]
    Y = s["y"]
    dot = 0
    for (i,j) in zip(X,Y):
        dot += i*j

    # Send results to sink
    sink.send_json({"result":dot,"i":s["i"],"j":s["j"]})

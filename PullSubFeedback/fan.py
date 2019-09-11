import zmq
import random
import time

context = zmq.Context()

# socket with workers
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")

# socket with sink
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

pullSink = context.socket(zmq.PULL)
pullSink.bind("tcp://*:5559")


print("Press enter when workers are ready...")
_ = input()
print("sending tasks to workers")

sink.send(b'0')

while True:
    for task in range(10):
        workers.send_string("hola")
    s = pullSink.recv_string()
    print("sigo")

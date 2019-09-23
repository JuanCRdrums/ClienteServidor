import sys
import time
import zmq

context = zmq.Context()

work = context.socket(zmq.PULL)
work.connect("tcp://localhost:5557")

# Socket to send messages to
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

# Process tasks forever
while True:
    s = work.recv_string()

    print(s)

    # Send results to sink
    sink.send(b'')

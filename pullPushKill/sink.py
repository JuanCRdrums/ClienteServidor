import sys
import time
import zmq

context = zmq.Context()

fan = context.socket(zmq.PULL)
fan.bind("tcp://*:5558")

signals = context.socket(zmq.PUB)
signals.bind("tcp://*:9999")

# Wait for start of batch
s = fan.recv()

# Start our clock now
tstart = time.time()
a = fan.recv_string()
print(a)
signals.send_string("stop")

# Calculate and report duration of batch
tend = time.time()
print("Total elapsed time: %d msec" % ((tend-tstart)*1000))

while True:
    pass

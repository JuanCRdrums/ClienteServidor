import sys
import time
import zmq

context = zmq.Context()

fan = context.socket(zmq.PULL)
fan.bind("tcp://*:5558")

toFan = context.socket(zmq.PUSH)
toFan.connect("tcp://localhost:5559")

# Wait for start of batch
s = fan.recv()

# Start our clock now
tstart = time.time()

while True:
    # Process 100 confirmations
    for task in range(10):
        print(task)
        s = fan.recv()
    print("Grupo de 10 recibido")
    toFan.send_string("1") #se confirma al fan

# Calculate and report duration of batch
tend = time.time()
print("Total elapsed time: %d msec" % ((tend-tstart)*1000))

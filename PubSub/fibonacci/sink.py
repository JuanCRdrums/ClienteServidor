import sys
import time
import zmq

context = zmq.Context()

fan = context.socket(zmq.PULL)
fan.bind("tcp://*:5558")

# Wait for start of batch
# Espera al inicio del lote
s = fan.recv()

# Start our clock now
tstart = time.time()
sol = 0
# Procesar 100 confirmaciones
for task in range(40):
    #print(task)
    s = fan.recv_string()
    t = int(s)
    sol += t
    #if task % 10 == 0:
    #    sys.stdout.write(':')
    #else:
    #    sys.stdout.write('.')
    #sys.stdout.flush()
    #print("-")

# Calculdar e informar la duración del lote
tend = time.time()
print("Total elapsed time: %d msec" % ((tend-tstart)*1000))
print("Answer: %d " % sol)

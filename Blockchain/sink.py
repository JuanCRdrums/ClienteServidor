import sys
import time
import zmq

context = zmq.Context()

fan = context.socket(zmq.PULL)
fan.bind("tcp://*:5558")


# Wait for start of batch
#Espere al inicio del lote
s = {}
s = fan.recv_json()

print(s)

#fan.send_string(s["answer"])


# Calculate and report duration of batch
# Calcular e informar la duración del lote
#print("Tiempo total transcurrido: %d msec" % ((tend-tstart)*1000))

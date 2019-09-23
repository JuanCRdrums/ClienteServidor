import zmq
import random
import time

context = zmq.Context()

# socket para workers
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")

# socket para sink (Resumidero, Sifón)
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")


print("Presione enter cuando los workers estén listos...")
_ = input()
print("Enviando tareas a los workers")

sink.send(b'0')

random.seed()

totalTime = 0

debug = 0 #Contador de Tareas

for task in range(40):
    #workload = random.randint(1,40)
    #totalTime += workload
    workers.send_string(u'%i' % task)
    
    debug += 1 
    print("Repartiendo tareas: %i" % debug)
    


print("Hecho!!!")
#print("Total expected cost: %s msec" % totalTime)
while True:
    pass

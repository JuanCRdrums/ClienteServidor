import zmq
import random
import time
import string
import hashlib
import itertools #Se importa para utilizar rangos infinitos

context = zmq.Context()

# socket para trabajadores (Work)
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")

# Socket para SINK (Resumidero,Sifón) Donde todo se recoge
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")


print("Presione enter cuando los workers estén listos...")
_ = input()
print("Enviando tareas a los workers")

################################
#Convierte una Cadena de Texto en una Cadena de hash
def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()

found = False
b = 0

while True:
    if b == 0:
        challenge = hashString("CS-rocks!")
        print("Hash: CS-rocks! \n {}".format(challenge))

    b += 1
    workers.send_string(u'%s' % challenge) #Envio challenge a los workers para empezar

#print("Hash: Nuevo Reto \n {}".format(challenge))



#sink.send_string(u'%s' % challenge) #Envio challenge para empezar
###############################

while True:
    pass

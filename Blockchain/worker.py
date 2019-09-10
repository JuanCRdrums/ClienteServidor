import sys
import time
import zmq
import string
import random
import hashlib

context = zmq.Context()

work = context.socket(zmq.PULL)
work.connect("tcp://localhost:5557")

# Socket para enviar mensajes a
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")


#Recibe el hash para sumarlo
challenge = work.recv_string()
print("\tSe ha recibido el CS-rocks! -> hashString: \n %s" % challenge)
print("\t\nGenerando...\n")

#######################################
#Convierte una Cadena de Texto en una Cadena de hash
def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()

#Genearacion de hash
def generation(challenge, size = 25):
    answer = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                      for x in range(size))
    attempt = challenge + answer
    #Se suman en attempt(intento) el reto (challenge) y responder(answer) -> "Que es el hash aleatorio"
    return attempt, answer
#######################################

#######################################
#Prueba de palabra
def proofOfWork(challenge): #Recibe el reto (challenge)
    found = False #Encontrar = False si no encuentra el reto
    attempts = 0 #(intentos inicializo en cero)
    while not found:
        attempt, answer = generation(challenge, 64)
        print(attempt)
        hash = hashString(attempt)
        if hash.startswith('00000'):
            found = True
            print(hash)
            print("\t\n Reto Encontrado!!!")
            return answer,attempts
        attempts += 1

    #print(attempts) #Numero de intentos que se demoro en hallar la respuesta
#######################################

answer,attempts = proofOfWork(challenge)

print("%s" % answer)
print("%i" % attempts)

result = {"answer": answer,"attempts": attempts}

sink.send_json(result)
'''
#Procesar tareas para siempre
while True:
    s = work.recv()

    # Indicador de progreso simple para el espectador
    sys.stdout.write('.')
    sys.stdout.flush()

    # Hacer el trabajo
    time.sleep(int(s)*0.001)

    # Enviar los resultados para sink
    sink.send(b'')
'''

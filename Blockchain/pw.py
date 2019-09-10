import string
import random
import hashlib

#Convierte una Cadena de Texto en una Cadena de hash
def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()


def generation(challenge, size = 25):
    answer = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                      for x in range(size))
    attempt = challenge + answer
    #Se suman en attempt(intento) el reto (challenge) y responder(answer) -> "Que es el hash aleatorio"
    return attempt, answer

#Prueba de palabra
def proofOfWork(challenge): #Recibe el reto (challenge)
    found = False #Encontrar = False si no encuentra el reto
    attempts = 0 #(intentos inicializo en cero)
    while not found:
        attempt, answer = generation(challenge, 64)
        print(attempt)
        hash = hashString(attempt)
        if hash.startswith('00'):
            found = True
            print(hash)
        attempts += 1
    print(attempts) #Numero de intentos que se demoro en hallar la respuesta
    return answer

challenge = hashString("CS-rocks!")
print("\tCS-rocks! -> hashString: \n %s" % challenge)
print("\t\nCalculando...\n")
answer = proofOfWork(challenge)
print(answer)

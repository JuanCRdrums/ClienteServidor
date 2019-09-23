import zmq
import random
import time
import string
import hashlib

random.seed()

def randomString(n):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                          for x in range(n))

context = zmq.Context()

# socket with workers
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")

# socket with sink
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

print("Press enter when workers are ready...")
_ = input()
print("sending tasks to workers")

sink.send(b'0')

challenge = randomString(20)

for task in range(2):
    workers.send_string(challenge)

while True:
    pass

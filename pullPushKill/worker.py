import sys
import time
import zmq
import random
import hashlib
import string

context = zmq.Context()

work = context.socket(zmq.PULL)
work.connect("tcp://localhost:5557")

# Socket to send messages to
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

signals = context.socket(zmq.SUB)
signals.connect("tcp://localhost:9999")
signals.setsockopt_string(zmq.SUBSCRIBE, "stop")

def hashString(s):
    sha = hashlib.sha256()
    sha.update(s.encode('ascii'))
    return sha.hexdigest()

def generation(challenge, size = 25):
    answer = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits)
                      for x in range(size))
    attempt = challenge + answer
    return attempt, answer

def signal(poller, s):
    socks = dict(poller.poll(1))
    return s in socks


def proofOfWork(challenge, poller, s):
    found = False
    attempts = 0
    answer = ""
    while not found and not signal(poller, s):
        attempt, answer = generation(challenge, 64)
        hash = hashString(attempt)
        if hash.startswith('0000'):
            found = True
            print(hash)
        attempts += 1
    print(attempts)
    return answer

poller = zmq.Poller()
poller.register(work, zmq.POLLIN)
poller.register(signals, zmq.POLLIN)

# Process tasks forever
while True:
    print("hola")
    socks = dict(poller.poll())
    if work in socks:
        print("Work to do....")
        challenge = work.recv_string()
        a = proofOfWork(challenge, poller, signals)
        sink.send_string(a)

    if signals in socks:
        print("Signal to exit....")
        m = signals.recv_string()
        print(m)

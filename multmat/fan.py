import zmq
import random
import time
import json

context = zmq.Context()

# socket with workers
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")

# socket with sink
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")


X = [[12,7,3],
    [4,5,9],
    [7,8,9]]

Y = [[5,8,1],
    [6,7,3],
    [4,5,9]]

print("Press enter when workers are ready...")
_ = input()
print("sending tasks to workers")
numtasks = len(X) * len(Y[0])

sink.send_string(u'%i' % numtasks)





print("Tasks to be sended {}", format(numtasks))



for i in range(len(X[0])):
    for j in range(len(Y)):
        w = json.dumps({"x":X[i], "y":Y[j], "i":i, "j":j})
        workers.send_string(w)

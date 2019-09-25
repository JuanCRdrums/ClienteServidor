import zmq
import random
import time
import string
import hashlib


context = zmq.Context()

board = {}

board["board"] = [
    [1,0,0,0,0,0,0,9,0],
    [8,4,0,0,0,2,0,0,0],
    [0,0,0,3,8,0,2,0,0],
    [0,0,0,9,0,0,8,5,3],
    [0,0,0,0,0,0,0,0,0],
    [5,3,8,0,0,6,0,0,0],
    [0,0,1,0,7,9,0,0,0],
    [0,0,0,5,0,0,0,6,7],
    [0,2,0,0,0,0,0,0,9]
]

def find_empty(bo):
    for i in range(len(bo["board"])):
        for j in range(len(bo["board"][0])):
            if bo["board"][i][j] == 0:
                return (i, j)  # row, col
    return None


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


row, col = find_empty(board) #se encuentra la primer celda vacia

for task in range(1,10):
    board["board"][row][col] = task
    workers.send_json(board)

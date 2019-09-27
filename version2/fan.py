import zmq
import random
import time
import string
import hashlib


context = zmq.Context()

board = {}

board["board"] = [
    [3,5,0,6,0,0,0,0,0],
    [0,0,4,0,0,0,0,0,0],
    [0,2,0,0,7,0,8,9,0],
    [0,0,0,0,0,5,0,0,0],
    [0,7,0,0,1,0,0,2,0],
    [0,0,0,4,0,0,0,0,0],
    [0,3,6,0,9,0,0,1,0],
    [0,0,0,0,0,0,5,0,0],
    [0,0,0,0,0,7,0,8,2]
]

def find_empty(bo):
    for i in range(len(bo["board"])):
        for j in range(len(bo["board"][0])):
            if bo["board"][i][j] == 0:
                return (i, j)  # row, col
    return None

def possibles(bo,pos):

    # Check row
    candidatos = [1,2,3,4,5,6,7,8,9]
    for num in candidatos:
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                if num in candidatos:
                    candidatos.remove(num)

        # Check column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                if num in candidatos:
                    candidatos.remove(num)

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if bo[i][j] == num and (i,j) != pos:
                    if num in candidatos:
                        candidatos.remove(num)

    return candidatos


# socket with workers
workers = context.socket(zmq.PUSH)
workers.bind("tcp://*:5557")

# socket with sink
sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

toSink = context.socket(zmq.PULL)
toSink.bind("tcp://*:5559")




print("Press enter when workers are ready...")
_ = input()
print("sending tasks to workers")

sink.send(b'0')




cont = 0
while True:
    if cont != 0:
        board = toSink.recv_json()
    row, col = find_empty(board) #se encuentra la primer celda vacia
    candidatos = possibles(board["board"],(row,col))
    for task in candidatos:
        board["board"][row][col] = task
        workers.send_json(board)
    cont += 1

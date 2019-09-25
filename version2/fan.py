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

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        for task in range(1,4):
            board["board"][row][col] = task
            board["i"] = i
            board["row"] = row
            board["col"] = col
            if(task == 1):
                board["f"] = 1
            if(task == 2):
                board["f"] = 2
            if(task == 3):
                board["f"] = 3
            workers.send_json(board)
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            #print_board(bo)
            #print("-=-=--=-=--=-=--=-=--=-=--=-=- ")
            if solve(bo):
                return True

            bo[row][col] = 0
    return False


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

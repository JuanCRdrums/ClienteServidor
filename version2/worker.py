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


def signal(poller, s):
    socks = dict(poller.poll(1))
    return s in socks



poller = zmq.Poller()
poller.register(work, zmq.POLLIN)
poller.register(signals, zmq.POLLIN)


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


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None


def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1,10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            #print_board(bo)
            #print("-=-=--=-=--=-=--=-=--=-=--=-=- ")
            if solve(bo):
                return True

            bo[row][col] = 0
    return False

def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i,j) != pos:
                return False

    return True






# Process tasks forever
while True:
    socks = dict(poller.poll())
    if work in socks:
        board = work.recv_json()
        find = find_empty(bo)
        if not find:
            return True
        else:
            row, col = find
        candidatos = possibles(board["board"],(row,col))
        for candidato in candidatos:
            board["board"][row][col] = candidato
            sink.send_json(board)

    if signals in socks:
        print("Signal to exit....")
        m = signals.recv_string()
        print(m)

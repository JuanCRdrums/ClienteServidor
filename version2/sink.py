import sys
import time
import zmq

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None


context = zmq.Context()

fan = context.socket(zmq.PULL)
fan.bind("tcp://*:5558")

toFan = context.socket(zmq.PUSH)
toFan.connect("tcp://localhost:5559")

signals = context.socket(zmq.PUB)
signals.bind("tcp://*:9999")

# Wait for start of batch
s = fan.recv()

# Start our clock now
tstart = time.time()

boards = [] #pila de tableros
cont = 0
while True:
    board = fan.recv_json()
    if board["board"] != 0:
        boards.append(board["board"])
        find = find_empty(board["board"])
        if not find:
            signals.send_string("stop")
            tend = time.time()
            print("Sudoku solved: ")
            print_board(board["board"])
            print("\nTotal elapsed time: %d msec" % ((tend-tstart)*1000))

        else:
            print("voy a enviar " + str(cont))
            """print_board(board["board"])
            print()
            print("----------------------")"""
            toFan.send_json(board)
            print("envio")

    else:
        print("pop")
        boards.pop()
        board["board"] = boards.pop()
        toFan.send_json(board)
    cont += 1

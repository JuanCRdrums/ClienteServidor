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


def possibles(bo,pos):

    # Check row
    candidatos = [1,2,3,4,5,6,7,8,9]
    for num in range(1,10):
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


def valid(bo, row):
    for i in range(len(bo[0])):
        if bo[row][i] == 0:
            if not possibles(bo,(row,i)):
                return False

    return True



context = zmq.Context()

fan = context.socket(zmq.PULL)
fan.bind("tcp://*:5558")

toFan = context.socket(zmq.PUSH)
toFan.connect("tcp://localhost:5559")

signals = context.socket(zmq.PUB)
signals.bind("tcp://*:9999")

# Wait for start of batch
s = fan.recv()



cont = 0
# Start our clock now
tstart = time.time()
while True:
    board = fan.recv_json()
    find = find_empty(board["board"])
    if not find:
        signals.send_string("stop")
        tend = time.time()
        print("Sudoku solved: ")
        print_board(board["board"])
        print("\nTotal elapsed time: %d msec" % ((tend-tstart)*1000))
        print("\nTotal iterations; %d" % cont)

    else:
        #print("voy a enviar " + str(cont))
        #print_board(board["board"])
        #print()
        #print("----------------------")
        row = find[0]
        if valid(board["board"],row):
            toFan.send_json(board)
        #print("envio")

    cont += 1

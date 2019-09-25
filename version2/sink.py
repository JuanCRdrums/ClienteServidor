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


context = zmq.Context()

fan = context.socket(zmq.PULL)
fan.bind("tcp://*:5558")

signals = context.socket(zmq.PUB)
signals.bind("tcp://*:9999")

# Wait for start of batch
s = fan.recv()

# Start our clock now
tstart = time.time()
finished = 
a = fan.recv_json()

signals.send_string("stop")


# Calculate and report duration of batch
tend = time.time()
print("Sudoku solved: ")
print_board(a["board"])
print("\nTotal elapsed time: %d msec" % ((tend-tstart)*1000))

while True:
    pass

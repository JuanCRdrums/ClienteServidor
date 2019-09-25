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





def valid(bo, num, pos, f):
    # Check row
    if f == 1:
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False

    # Check column
    if f == 2:
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0] != i:
                return False

    # Check box
    if f == 3:
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
        if(valid(board["board"]),board["i"],(board["row"],board["col"]),board["f"]):
            sink.send_string("1")
        else:
            sink.send_string("0")

    if signals in socks:
        print("Signal to exit....")
        m = signals.recv_string()
        print(m)

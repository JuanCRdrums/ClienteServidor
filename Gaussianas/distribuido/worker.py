import zmq

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



# Process tasks forever
while True:
    socks = dict(poller.poll())
    if work in socks:
        message = work.recv_json()
        print(message)


    if signals in socks:
        print("Signal to exit....")
        m = signals.recv_string()
        print(m)

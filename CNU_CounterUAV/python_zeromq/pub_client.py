import sys
import zmq

port = "8889"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://10.42.0.150:%s" % port)

# Subscribe to zipcode, default is NYC, 10001
socket.setsockopt(zmq.SUBSCRIBE, b"")

# Process 5 updates
total_value = 0
for update_nbr in range (5):
    string = socket.recv()
    print("receive")

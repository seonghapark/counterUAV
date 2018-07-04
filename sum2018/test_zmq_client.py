import sys
import zmq

port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting data...")
socket.connect("tcp://localhost:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, b'')

# Process 5 updates
total_value = 0
for update_nbr in range (5):
    string = socket.recv()
    print(string)

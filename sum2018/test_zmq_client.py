import sys
import zmq

port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://192.168.43.244:%s" % port)

# Subscribe to zipcode, default is NYC, 10001
socket.setsockopt(zmq.SUBSCRIBE, "")

# Process 5 updates
total_value = 0
for update_nbr in range (5):
    string = socket.recv()
    print string

import numpy as np
import threading
import zmq

fs = 44100
flag = 0

class Node:
    def __init__(self, count=None, fsif=None, time=None, next=None, prev=None):
        self.count = count
        self.fsif = fsif
        self.time = time
        self.next = next
        self.prev = prev

    def setting(self, tail):
        self.next = tail
        tail.prev = self

    def add_prev(self, count, fsif, time):
        temp = Node(count, fsif, time)
        temp.prev = self.prev
        temp.prev.next = temp
        temp.next = self
        self.prev = temp

    def add_list(self, head, tail):
        tail.next = self
        head.prev = self.prev
        self.prev.next = head
        self.prev = tail

    def remove_next(self):
        global flag
        head_next = self.next
        count = head_next.count
        fsif = head_next.fsif
        time = head_next.time
        if head_next.fsif is None:
            print("Queue is empty")
            flag = 2
            return None, None, None
        self.next = head_next.next
        head_next.next.prev = self
        del head_next
        return count, fsif, time


class zeroMQ(threading.Thread):
    def __init__(self, head, tail):
        threading.Thread.__init__(self)
        self.count = 0
        self.head = head
        self.tail = tail
        self.temp_head = Node()
        self.temp_tail = Node()
        self.temp_head.setting(self.temp_tail)
        port = 8887

        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://127.0.0.1:%s" % port)  # raspberry pi ip address

        topicfilter = b""
        self.socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

    def run(self):
        global flag
        while True:
            string = self.socket.recv()

            print(string)
            temp = np.fromstring(string, dtype=np.float)
            c = int(len(temp) / 883) #c 전체 데이터를 883으로 나누면 됨(c * 883 배열이므로)
            f = np.empty((c, 882)) #지금 1차원배열로 받으므로 나중에 처리해줘야함
            f = temp[:, :c]
            f = f.T
            t = temp[882:883, :c]

            print(c)
            print(f)
            print(t)

            if flag is not 0:
                self.temp_tail.add_prev(c, f, t)
                self.count += 1
            else:
                flag = -1
                if self.count is not 0:
                    self.tail.add_list(self.temp_head.next, self.temp_tail.prev)
                    self.count = 0
                self.tail.add_prev(c, f, t)
                flag = 0
            print("recevie")


class fft_handler:
    def __init__(self):
        self.opp = 0
        self.fs = fs
        self.Tp = 0.020
        self.n = int(self.Tp * self.fs);
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:8889")  # tcp data transfer

    def dbv(self, input):   #transform to decibel
        return 20 * np.log10(abs(input))

    def data_process(self, count, time, fsif):
        self.opp += 1
        self.time = np.array(time)  # change the format of time from list to to np.array
        sif = fsif[:count, :]  # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count
        sif = sif - np.tile(sif.mean(0), [sif.shape[0], 1]);
        zpad = int(8 * self.n / 2)  # create the number_of_ifft_entities --> which is the number of vales that has to be created from fft calculation
        v = self.dbv(np.fft.ifft(sif, zpad, 1))  # Do fft calculation, and convert results to decibel through dbv function
        s = v[:, 0:int(v.shape[1] / 2)]
        m = s.max()
        self.s = s - m
        self.time = self.time[:50]
        self.s = self.s[:50]

    def send(self):
        data = np.array([self.time, self.s])
        self.socket.send(data)


def main():
    global flag

    head = Node()
    tail = Node()
    fft = fft_handler()
    head.setting(tail)
    zeromq = zeroMQ(head, tail)
    zeromq.start()

    # while True:
    #     flag = 1
    #     c, f, t = head.remove_next()
    #     if flag is 2:
    #         time.sleep(0.1)
    #         continue
    #     flag = 0
    #     fft.data_process(c, f, t)
    #     fft.send

main()
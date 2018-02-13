import zmq
from scipy.io import wavfile
import numpy as np
from pykalman import KalmanFilter

fs = 44100


class wav_handler:
    def __init__(self, file_name):
        self.fs, self.data = wavfile.read(file_name)
        self.data = self.data.T
        self.count = 0

    def get_chunk(self):
        if self.count + fs < self.data.shape[1]:
            data = self.data[:, self.count: self.count + fs]
            self.count += fs
            return data
        else:
            return None


class zmq_handler:
    def __init__(self):
        # zmq send context
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:8887")

    def send(self, s, time):
        data = np.concatenate((s, time), 0)
        self.socket.send(data)


class fft_handler:
    def __init__(self):
        self.opp = 0
        self.fs = fs
        self.Tp = 0.020
        self.n = int(self.Tp * self.fs);
        self.fsif = np.zeros([50, self.n], dtype=np.float)

    def dbv(self, input):
        return 20 * np.log10(abs(input))

    def get_line(self, raw):
        self.leftarray = raw[0]
        self.rightarray = raw[1]
        self.start = (self.leftarray > 0) #주파수값이 증가하고 있는 지 판단함(양수면 증가)

    def data_process(self):
        count = 0
        time = []  # time is a list

        for ii in range(11, int((self.start.shape[0] - self.n))):
            if (self.start[ii] == True) & (self.start[ii - 11:ii - 1].mean() == 0):  # if start[ii] is true and the mean of from start[ii-11] to start[ii-1] is zero
                self.fsif[count, :] = self.rightarray[ii:ii + self.n]  # then copy rightarray from ii to ii+n and paste them to sif[count] --> sif[count] is a list
                time.append((ii + int(self.start.shape[0]) * self.opp) * 1. / self.fs)  # append time, the time is ii/fs --> few micro seconds (0.0001 sec or so)
                count = count + 1

        self.opp += 1
        data_time = np.array(time)  # change the format of time from list to to np.array
        sif = self.fsif[:count, :]   # truncate sif --> remove all redundant array lists in sif, just in case if sif is longer then count
        sif = sif - np.tile(sif.mean(0), [sif.shape[0], 1]);
        zpad = int(8 * self.n / 2)  # create the number_of_ifft_entities --> which is the number of vales that has to be created from fft calculation
        v = self.dbv(np.fft.ifft(sif, zpad, 1))  # Do fft calculation, and convert results to decibel through dbv function
        s = v[:, 0:int(v.shape[1] / 2)]
        m = s.max()
        data_val = s - m
        data_time = data_time[:50]
        data_val = data_val[:50]

        return data_val, data_time


class max_handler:
    def __init__(self):
        self.n = 882
        self.lfm = [2260E6, 2590E6]  # e6 = * 10^6
        self.max_detect = 3E8 / (2 * (self.lfm[1] - self.lfm[0])) * self.n / 2
        self.y_len = 1764

        self.ignore_distance = 2.5
        self.ignore_index = int(self.ignore_distance * self.y_len / self.max_detect)

        self.data_time = []
        self.data_val = []
        self.data_tlen = 0
        self.data_vallen = 0

        self.initial_time = -1
        self.initial_distance = -1
        self.min_initial_distance = 10
        self.front_val = []
        self.front_t = []

    def get_data(self, val, time):
        self.data_time = np.insert(time, len(time), 1.0)
        self.data_val = val
        self.data_tlen = len(self.data_time)
        self.data_vallen = len(self.data_val)

    def print_max(self):
        time = []
        max_distance = []
        for i in range(0, self.data_tlen - 1):
            time.append((self.data_time[i] + self.data_time[i + 1]) / 2)
            max_index = np.argmax(self.data_val[i][self.ignore_index:])
            max_distance.append(self.ignore_distance + max_index * self.max_detect / self.y_len)
        if (self.initial_time == -1 and self.initial_distance == -1):
            self.set_initial(time, max_distance)

        return time, max_distance

    def set_initial(self, time, max_distance):
        t = []
        val = []

        for i in range(0, self.data_tlen - 1):
            if (max_distance[i] > self.min_initial_distance):
                t.append(time[i])
                val.append(max_distance[i])
        long_val = np.array(self.front_val + val)

        if (len(long_val) > 10 and np.var(long_val) < 100):
            minimum = 100
            mean = np.mean(long_val)
            for i in range(0, len(long_val)):
                if abs(long_val[i] - mean) < minimum:
                    self.initial_time = (self.front_t + t)[i]
                    self.initial_distance = long_val[i]
                    minimum = abs(long_val[i] - mean)

        self.front_val = val
        self.front_t = t


class kmf_handler:
    def __init__(self, time, distance, initial_time=-1, initial_distance=-1, wav_time=1, max_speed=3):
        self.data_maxrange = distance
        self.initial_time = initial_time
        self.initial_distance = initial_distance
        self.wav_time = wav_time
        self.max_speed = max_speed
        self.time_ragne = np.linspace(0, wav_time, 50 * wav_time)
        self.time_range = self.time_range + 1

        # check start point
        for i in range(0, len(time)):
            if time[i] == initial_time:
                self.initial_range = i
                print(i)
                break

    def data_process(self):
        # cut before first point
        self.time_range = self.time_range[self.initial_range:]
        data_maxrange_afterinitial = self.data_maxrange[self.initial_range:]
        temp = np.concatenate((data_maxrange_afterinitial, ([0] * (50 - len(data_maxrange_afterinitial) % 50))), axis=0)

        # seperate by time (1 second)
        afterinitial_sep = np.zeros((int(len(temp) / 50), 50))
        for i in range(0, int(len(temp) / 50)):
            for j in range(0, 50):
                afterinitial_sep[i][j] = temp[i * 50 + j]

        # cut lower and upper value
        avg = self.initial_distance
        for i in range(0, afterinitial_sep.shape[0]):
            hap = 0
            hapcnt = 0
            for j in range(0, 50):
                if ((avg - self.max_speed < afterinitial_sep[i][j]) and (afterinitial_sep[i][j] < avg + self.max_speed)):
                    hap += afterinitial_sep[i][j]
                    hapcnt += 1
                else:
                    afterinitial_sep[i][j] = -1
            avg = hap / float(hapcnt)

        afterinitial_hap = []
        for i in range(0, afterinitial_sep.shape[0]):
            for j in range(0, afterinitial_sep.shape[1]):
                afterinitial_hap.append(afterinitial_sep[i][j])
        afterinitial_hap = np.array(afterinitial_hap[:-1 * (50 - len(data_maxrange_afterinitial) % 50)])

        # fill -1 values
        front_val = 0
        last_val = 0
        after_noise_cancel = np.zeros((len(afterinitial_hap)))
        for i in range(0, len(afterinitial_hap)):
            after_noise_cancel[i] = afterinitial_hap[i]
        for i in range(1, len(after_noise_cancel)):
            if (after_noise_cancel[i] != -1):
                first_val = last_val
                last_val = i
                for i in range(1, last_val - first_val):
                    after_noise_cancel[first_val + i] = after_noise_cancel[first_val] + (after_noise_cancel[last_val] - after_noise_cancel[first_val]) / (last_val - first_val) * i
        
        self.getkmf(after_noise_cancel)

    def get_kmf(self, after_noise_cancel):
        kf = KalmanFilter(transition_matrices=np.array([[1, 1], [0, 1]]), transition_covariance=([[0.25, 0], [0, 0]]), initial_state_mean=[29, -1.5])
        self.after_kf = kf.em(after_noise_cancel).smooth(after_noise_cancel)[0]

def main():
    file_name = './wav/range_test2.wav'
    wav = wav_handler(file_name)
    zmq = zmq_handler()
    fft = fft_handler()
    max = max_handler()

    while (1):
        raw = wav.get_chunk()
        if raw is None:
            break

        fft.get_line(raw)
        val, time = fft.data_process()
        max.get_data(val, time)
        time, distance = max.print_max()

        kmf = kmf_handler(time, distance, max.initial_t, max.initial_distance)
        kmf.data_process()

        print(kmf.time_ragne)
        print(kmf.after_kf)


main()
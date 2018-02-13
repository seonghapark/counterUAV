import numpy as np
import pylab as pl

in_t = open("time_from_maxindex.txt","r")
in_distance = open("distance_from_maxindex.txt","r")

data_t = []
data_maxrange = []
wav_time = 24
initial_t = 7.081337868480725
initial_distance = 24.09090909090909
max_speed = 3.0


# read files
in_t.readline()
in_distance.readline() #ignore first second

j = 0
for i in range(0, wav_time):
	split_line = in_t.readline().split()
	split_line = [float (j) for j in split_line]  # string to float
	data_t = np.append(data_t, split_line)
	data_t = np.array(data_t)

	split_line = in_distance.readline().split()
	split_line = [float(k) for k in split_line]  # string to float
	data_maxrange = np.append(data_maxrange, split_line)
	data_maxrange = np.array(data_maxrange)

time_range = np.linspace(0, wav_time, 50*wav_time)  # 1초를 50개로 나눠 배열을 만듬, 1초면 인덱스가 50개, 0.02초 단위로 측정하므로
time_range = time_range + 1  # 배열 전체에 1을 더함

# check start point
for i in range(0, len(data_t)):
	if data_t[i] == initial_t:
		initial_range = i
		print(i)
		break

#cut before first point
time_range = time_range[initial_range:]
data_maxrange_afterinitial = data_maxrange[initial_range:]
temp = np.concatenate((data_maxrange_afterinitial, ([0] * (50-len(data_maxrange_afterinitial)%50))), axis = 0)
print(temp.shape)

# seperate by time (1 second)
afterinitial_sep = np.zeros((int(len(temp)/50), 50))
for i in range(0, int(len(temp)/50)):
	for j in range(0, 50):
		afterinitial_sep[i][j] = temp[i*50 + j]
print(afterinitial_sep.shape)

#cut lower and upper value
avg = initial_distance
for i in range(0, afterinitial_sep.shape[0]):
	hap = 0
	hapcnt = 0
	for j in range(0, 50):
		if((avg - max_speed < afterinitial_sep[i][j]) and (afterinitial_sep[i][j] < avg + max_speed)):
			hap += afterinitial_sep[i][j]
			hapcnt += 1
		else:
			afterinitial_sep[i][j] = -1
	avg = hap / float(hapcnt)

afterinitial_hap = []
for i in range(0, afterinitial_sep.shape[0]):
	for j in range(0, afterinitial_sep.shape[1]):
		afterinitial_hap.append(afterinitial_sep[i][j])
afterinitial_hap = np.array(afterinitial_hap[:-1*(50-len(data_maxrange_afterinitial)%50)])
print(afterinitial_hap.shape)

#fill -1 values
front_val = 0
last_val = 0
after_noise_cancel = np.zeros((len(afterinitial_hap)))
for i in range(0, len(afterinitial_hap)):
	after_noise_cancel[i] = afterinitial_hap[i]
for i in range(1, len(after_noise_cancel)):
	if(after_noise_cancel[i] != -1):
		first_val = last_val
		last_val = i
		for i in range(1, last_val-first_val):
			after_noise_cancel[first_val+i] = after_noise_cancel[first_val] + (after_noise_cancel[last_val] - after_noise_cancel[first_val])/(last_val-first_val)*i


print(data_t.shape, data_maxrange.shape)
print(time_range.shape, data_maxrange_afterinitial.shape)
print(time_range.shape, afterinitial_hap.shape)

pl.scatter(data_t, data_maxrange, marker = 'x', label = 'original data', color = 'g')
pl.scatter(time_range, data_maxrange_afterinitial, marker = 'x', color = 'r', label = 'cut before first point')
#pl.scatter(time_range, afterinitial_hap, marker = 'x', color = 'b', label = 'cut lower and upper value')
pl.plot(time_range, after_noise_cancel, label = 'cut lower and upper value')


#time_range, data_maxrange_afterinitial
from pykalman import KalmanFilter

kf = KalmanFilter(transition_matrices = np.array([[1,1],[0,1]]),
				  transition_covariance = ([[0.25,0],[0,0]]),
				  initial_state_mean = [29, -1.5])
after_kf = kf.em(after_noise_cancel).smooth(after_noise_cancel)[0]

pl.plot(time_range, after_kf[:,0], label = 'after kalman filter')

pl.xlim (0,30)
pl.ylim(-10, 70)
pl.legend(loc = 'upper right')

pl.show()

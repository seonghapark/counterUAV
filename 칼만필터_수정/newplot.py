import numpy as np
import sys
import pylab as pl

in_t = open("time_from_maxindex.txt","r")
in_distance = open("distance_from_maxindex.txt","r")

data_t = []
data_maxrange = []
first_time = 7.08133786849
first_value = 24.0909090909
max_speed = 5.0

wav_time = int(sys.argv[1])-1


# read files
in_t.readline()
in_distance.readline()

j=0
for i in range(0, wav_time):
	split_line = in_t.readline().split()
	split_line = [float (j) for j in split_line]
	data_t = np.append(data_t, split_line)
	data_t = np.array(data_t)

	split_line = in_distance.readline().split()
	split_line = [float(k) for k in split_line]
	data_maxrange = np.append(data_maxrange, split_line)
	data_maxrange = np.array(data_maxrange)

time_range = np.linspace(0, wav_time, 50*wav_time)
time_range =time_range +1

# check start point
for i in range(0, len(data_t)):
	if data_t[i] == 7.08133786849:
		print(i,data_t[i], data_maxrange[i])
		start_range =i

#cut before first point
time_range = time_range[start_range:]
new_data_maxrange = data_maxrange[start_range:]
temp = np.concatenate((new_data_maxrange, ([0] * (50-len(new_data_maxrange)%50))), axis = 0) 
print(temp.shape)

# seperate by time (1 second)
new_data_timesep = np.zeros((int(len(temp)/50), 50))
for i in range(0, int(len(temp)/50)):
	for j in range(0, 50):
		new_data_timesep[i][j] = temp[i*50 + j]
print(new_data_timesep.shape)

#cut lower and upper value
avg = first_value
for i in range(0, new_data_timesep.shape[0]):
	hap = 0
	hapcnt = 0
	for j in range(0, 50):
		if((avg - max_speed < new_data_timesep[i][j]) and (new_data_timesep[i][j] < avg + max_speed)):
			hap += new_data_timesep[i][j]
			hapcnt += 1
		else:
			new_data_timesep[i][j] = -1
	avg = hap / float(hapcnt)

new_data_timehap = []
for i in range(0, new_data_timesep.shape[0]):
	for j in range(0, new_data_timesep.shape[1]):
		new_data_timehap.append(new_data_timesep[i][j])
new_data_timehap = np.array(new_data_timehap[:-3])
print(new_data_timehap.shape)

#fill -1 values
front_val = 0
last_val = 0
before_kf = np.zeros((len(new_data_timehap)))
for i in range(0, len(new_data_timehap)):
	before_kf[i] = new_data_timehap[i]
for i in range(1, len(before_kf)):
	if(before_kf[i] != -1):
		first_val = last_val
		last_val = i
		for i in range(1, last_val-first_val):
			before_kf[first_val+i] = before_kf[first_val] + (before_kf[last_val] - before_kf[first_val])/(last_val-first_val)*i




print(data_t.shape, data_maxrange.shape)
print(time_range.shape, new_data_maxrange.shape)
print(time_range.shape, new_data_timehap.shape)

pl.scatter(data_t, data_maxrange, marker = 'x', label = 'original data', color = 'g')
pl.scatter(time_range, new_data_maxrange, marker = 'x', color = 'r', label = 'cut before first point')
pl.scatter(time_range, new_data_timehap, marker = 'x', color = 'b', label = 'cut lower and upper value')
pl.scatter(time_range, before_kf, marker = 'x', color = 'r', label = 'before kf')







#time_range, new_data_maxrange
from pykalman import KalmanFilter

kf = KalmanFilter(transition_matrices = np.array([[1,1],[0,1]]),
				  transition_covariance = ([[0.25,0],[0,0]]),
				  initial_state_mean = [29, -1.5])
states_pred = kf.em(before_kf).smooth(before_kf)[0]

pl.plot(time_range, states_pred[:,0], label = 'after kalman filter')

pl.xlim (0,30)
pl.ylim(-10, 70)
pl.legend(loc = 'upper right')

pl.show()

import sys

fs = 44100  # Sampling rate
Tp = 0.020  # Ramp up-time
lfm = [2260E6, 2590E6] 

if (len(sys.argv) > 1):
    fs = float(sys.argv[1])
    Tp = float(sys.argv[2])
    lfm = [float(sys.argv[3]), float(sys.argv[4])]  # Radar frequency sweep range

n = fs/(1/Tp)  # Samples per a ramp up-time
max_detect = 3E8/(2*(lfm[1]-lfm[0]))*n/2 # Max detection distance according to the radar frequency

print("Max detection range:", round(max_detect, 2), " m")

range_resolution = 3E8/(2*(lfm[1]-lfm[0]))  # Tau_r = c/2B (bandwidth)

print("Range resolution:", round(range_resolution, 2), " m")
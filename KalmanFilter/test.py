from pykalman import KalmanFilter

kf = KalmanFilter(initial_state_mean=0, n_dim_obs=2)

measurements = [[1,0],[0,0],[0,1]]
print (kf.em(measurements).smooth([[2,0],[2,1],[2,2]])[0])

import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

from pykalman import KalmanFilter

rnd = np.random.RandomState(0)

n_timesteps = 50 # num of blue dot(observation)

x = np.linspace(0, 100, n_timesteps) # num of timesteps values from 0 to 100 value
observations = 5 * (x + 5*rnd.randn(n_timesteps)) # y with noise 
						# randn : Return a samples from the “standard normal” distribution.
observations = observations[::-1] # reverse



kf = KalmanFilter(
	transition_matrices = np.array([[1,1],[0,1]])
	,transition_covariance = ([[0,0],[0,0]])
	,initial_state_mean = [500, 0]
	#,initial_state_covariance = [0, 0]
	,em_vars=[
      'transition_matrices', 'transition_covariance',
      'initial_state_mean'
      #,'initial_state_covariance'
    ]
)



loglikelihoods = np.zeros(10)
for i in range(len(loglikelihoods)):
    kf = kf.em(X=observations, n_iter=1)
    loglikelihoods[i] = kf.loglikelihood(observations)
    # X : [n_timesteps, n_dim_obs] array


'''
# Estimate the state without using any observations. 
#This will let us see how
# good we could do if we ran blind.
n_dim_state = data.transition_matrix.shape[0]
n_timesteps = data.observations.shape[0]
blind_state_estimates = np.zeros((n_timesteps, n_dim_state))
for t in range(n_timesteps - 1):
    if t == 0:
        blind_state_estimates[t] = kf.initial_state_mean
    blind_state_estimates[t + 1] = (
      np.dot(kf.transition_matrices, blind_state_estimates[t])
      + kf.transition_offsets[t]
    )
'''

#filtered_state_estimates = kf.filter(observations)[0]
#smoothed_state_estimates = kf.smooth(observations)[0]

states_pred = kf.em(observations).smooth(observations)[0]


observation_plot = pl.scatter(x, observations, marker = 'x', color = 'b', label = 'observations')
position_plot = pl.plot(x, states_pred[:, 0], linestyle = '-', color = 'r', label = 'position est.')
answer_plot = pl.plot(x, 5*x[::-1], linestyle = '-', color = 'g', label = 'answer')

#lines_filt = pl.plot(filtered_state_estimates, linestyle='--', color='g')
#lines_smooth = pl.plot(smoothed_state_estimates, linestyle='-.', color='r')



pl.legend(loc = 'upper right')
pl.show()

'''
pl.figure()
pl.plot(loglikelihoods)
pl.show()
'''
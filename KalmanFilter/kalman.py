import numpy as np
import pylab as pl
import matplotlib.pyplot as plt

from pykalman import KalmanFilter

rnd = np.random.RandomState(0)

n_timesteps = 100
x = np.linspace(0, 100, n_timesteps)
observations = 5 * (x + 5*rnd.randn(n_timesteps)) # y with noise
observations = observations[::-1]



kf = KalmanFilter(transition_matrices = np.array([[1,1],[0,1]]),
				  transition_covariance = ([[0,0],[0,0]]),
				  initial_state_mean = [500, -5])

states_pred = kf.em(observations).smooth(observations)[0]


observation_plot = pl.scatter(x, observations, marker = 'x', color = 'b', label = 'observations')
position_plot = pl.plot(x, states_pred[:, 0], linestyle = '-', color = 'r', label = 'position est.')
answer_plot = pl.plot(x, 5*x[::-1], linestyle = '-', color = 'g', label = 'answer')
pl.legend(loc = 'upper right')
pl.show()


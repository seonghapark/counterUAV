import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 8)

# intial parameters
n_iter = 300
sz = (n_iter,) # size of array
x = 0

added = np.random.normal(x,0.1,size=sz)
xi = np.linspace(0, 5, n_iter) 
z = xi + added

Q = 1e-5 # process variance

# allocate space for arrays
xhat=np.zeros(sz)      # a posteri estimate of x
P=np.zeros(sz)         # a posteri error estimate
xhatminus=np.zeros(sz) # a priori estimate of x
Pminus=np.zeros(sz)    # a priori error estimate
K=np.zeros(sz)         # gain or blending factor

# estimate of measurement variance
R = 0.02**2 # change ... see the effect

# intial guesses
xhat[0] = 0.0
P[0] = 10.0

for k in range(1,n_iter):
    # time update
    xhatminus[k] = xhat[k-1]
    Pminus[k] = P[k-1]+Q

    # measurement update
    K[k] = Pminus[k]/( Pminus[k]+R )
    xhat[k] = xhatminus[k]+K[k]*(z[k]-xhatminus[k])
    P[k] = (1-K[k])*Pminus[k]

plt.figure()
plt.plot(z,'k+',label='noisy observations')
plt.plot(xhat,'b-',label='estimation')
#plt.plot(xi, color = 'g', label='truth value')
plt.legend()
plt.xlabel('time')
plt.ylabel('position')

plt.show()

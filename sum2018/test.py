import random
import time

from matplotlib import pyplot as plt
from matplotlib import animation


class RegrMagic(object):
    """Mock for function Regr_magic()
    """
    def __init__(self):
        self.x = 0
    def __call__(self):
        time.sleep(random.random())
        self.x += 1
        return self.x, random.random()

regr_magic = RegrMagic()

def frames():
    while True:
        yield regr_magic()

fig = plt.figure()

x = []
y = []
def animate(args):
    x.append(args[0])
    y.append(args[1])
    return plt.plot(x, y, color='g')


anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000)
plt.show()

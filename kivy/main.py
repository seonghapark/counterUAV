from kivy.app import App
from kivy.uix.button import Button

#import matplotlib
#matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
#from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas
import matplotlib.pyplot as plt
#import matplotlib.patches as patches
#import matplotlib.colors as colors 
#import numpy as np
#import math

def hi():
    infile = open("dummy.txt",'r')
    color_file = open("color.txt",'r')
    color=[]
    for i in range(0,80):
	    color.append(int(color_file.readline()))
    time = 10
    distance = 10
    calculate = 100/10
    plt.figure()

    for t in range(0,time):
	    s=infile.readline()
	    w = s.split()
	    for dis in range(0,distance):
		    sharp = '#'+str(hex(color[int(w[dis])+79]))[2:].zfill(6)
		    plt.scatter(t,dis,c=sharp)
    plt.show()


class Hello(App):
      def build(self):
	   btn = Button(text="hello")
	   hi()
	   return btn

if __name__ == "__main__":
	Hello().run()

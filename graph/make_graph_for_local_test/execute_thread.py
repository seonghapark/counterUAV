import sys
import threading

from subprocess import call
# from queue import Queue

filename = sys.argv[1]
# filetime = sys.argv[2]

th_handler = threading.Thread(target)

threads = []
for_process = threading.Thread(target = data_processing)
threads.append(for_process)
for_plot = threading.Thread(target = plot_graph)
threads.append(for_plot)

for_process.start()
time.sleep(1)
for_plot.start()

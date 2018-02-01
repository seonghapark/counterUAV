
import argparse

from datetime import timedelta
import datetime
import sys
import os

import subprocess
import shlex

from read_data import read_data
from plot_data import plot_data


def collect_data(nodeNAME):
	nodeLoc = []
	nodeDescr = []

	for i in range(len(nodeNAME)):
		subprocess.call(['./reports/getdatasets', nodeNAME[i], datefrom, dateto])
		with open("./node_name") as f:
			for line in f:
				# print('\n', "** description: ", line.strip(), ', node ID: ', nodeNAME[i])
				nodeDescr.append(line.strip())
		with open("./node_loc") as f:
			for line in f:
				# print("** location: ", line, '\n')
				nodeLoc.append(line.strip())
				os.rename("./sensor_data_set.csv", "./sensor_data_set_"+nodeNAME[i]+".csv")

	return nodeLoc, nodeDescr




if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--n', dest='node_name', nargs='*', help='Target node IDs')
	parser.add_argument('--ds', dest='start_day', nargs='*', help='Start date from today, 0 means start from today')
	parser.add_argument('--de', dest='end_day', nargs='*', help='End date from today, 1 means yesterday')
	parser.add_argument('--t', dest='plot_temperature', action='store_true', help='Plot temperature sensor data')
	parser.add_argument('--h', dest='plot_humidity', action='store_true', help='Plot humidity sensor data')
	parser.add_argument('--p', dest='plot_pressure', action='store_true', help='Plot pressure sensor data')

	args = parser.parse_args()
	nodeNAME = args.node_name
	datefrom = args.start_day[0]
	dateto = args.end_day[0]

	args_plot = []
	args_plot.append(args.plot_temperature)
	args_plot.append(args.plot_humidity)
	args_plot.append(args.plot_pressure)

	nodeLoc, nodeDescr = collect_data(nodeNAME)
	print('\n' "** the number of the nodes: ", len(nodeNAME))
	print("** node ID: ", nodeNAME)
	print("** date from: ", datetime.date.today()-timedelta(int(datefrom)))
	print("** date to: ", datetime.date.today()-timedelta(int(dateto)))
	print("** location of the nodes: ", nodeLoc)
	print("** Descrptions of the nodes: ", nodeDescr, '\n')

	data_dict = read_data(nodeNAME)
	plot_data(nodeNAME, nodeLoc, data_dict, args_plot)

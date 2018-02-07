
# # ############################################################# PLOT data

import os

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


	#************************************************************************************Pressure1
def plot_pressrue(nodeNAME, nodeLoc, data_dict):
	for i in range(len(nodeNAME)):
		pressure1 = plt.figure(figsize=(100, 100))
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["pressbmp180"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["pressbmp180"],label='met_pressure: bmp180', linewidth=1)
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["presslps25h"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["presslps25h"],label='chem_pressure: lps25h', linewidth=1)

		##****Legend

		legpressurewhole = plt.legend()
		# get the lines and texts inside legend box
		legpressurewhole_lines = legpressurewhole.get_lines()
		legpressurewhole_texts = legpressurewhole.get_texts()
		# bulk-set the properties of all lines and texts
		plt.setp(legpressurewhole_lines, linewidth=1)
		plt.setp(legpressurewhole_texts, fontsize='x-large')
		##****Legend

		plt.xlabel('Time (EST)', fontsize=15)
		plt.ylabel('Pressure (hPa)', fontsize=15)
		plt.title('node ID: '+nodeNAME[i]+', Loc: '+nodeLoc[i], fontsize=20)

		### y axis minor tick
		plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1000))
		plt.subplot().tick_params(direction='in', width=1., length=10)
		plt.subplot().tick_params(direction='in', length=6,  which='minor')

		# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

		majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
		plt.subplot().xaxis.set_major_formatter(majorFormatter)
		plt.gcf().autofmt_xdate()
		pressure1.show()
		plt.savefig('./pressure_'+nodeNAME[i]+'.png',bbox_inches='tight')

	# #*********************************************************************************************Pressrue2

	if len(nodeNAME) > 1:
		pressureCMP = plt.figure(figsize=(100, 100))

		title = ''

		for i in range(len(nodeLoc)):
			title = title+'node ID: '+nodeNAME[i]+', Loc: '+nodeLoc[i]+'\n'
			if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["pressbmp180"]):
				plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["pressbmp180"],label='met_pressure: bmp180, '+nodeNAME[i], linewidth=1)
			if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["presslps25h"]):
				plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["presslps25h"],label='chem_pressure: lps25h, '+nodeNAME[i], linewidth=1)

		##****Legend
		legpressurewhole = plt.legend()
		# get the lines and texts inside legend box
		legpressurewhole_lines = legpressurewhole.get_lines()
		legpressurewhole_texts = legpressurewhole.get_texts()
		# bulk-set the properties of all lines and texts
		plt.setp(legpressurewhole_lines, linewidth=1)
		plt.setp(legpressurewhole_texts, fontsize='x-large')
		##****Legend

		plt.xlabel('Time (EST)', fontsize=15)
		plt.ylabel('Pressure (hPa)', fontsize=15)
		plt.title(title, fontsize=20)

		### y axis minor tick
		plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1000))
		plt.subplot().tick_params(direction='in', width=1., length=10)
		plt.subplot().tick_params(direction='in', length=6,  which='minor')

		# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

		majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
		plt.subplot().xaxis.set_major_formatter(majorFormatter)
		plt.gcf().autofmt_xdate()
		pressureCMP.show()
		plt.savefig('./pressure_all.png',bbox_inches='tight')


	#************************************************************************************************************Humidity1
def plot_humidity(nodeNAME, nodeLoc, data_dict):
	for i in range(len(nodeNAME)):
		humid1 = plt.figure(figsize=(100, 100))
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["huhih6130"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["huhih6130"],label='light_humidity: hih6130', linewidth=1, color="aqua")
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["huhtu21d"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["huhtu21d"],label='met_humidity: htu21d', linewidth=1, color="greenyellow")
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["husht25"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["husht25"],label='chem_humidity: sht25', linewidth=1, color="yellow")
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["huhih4030"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["huhih4030"],label='met_humidity: hih4030', linewidth=1)

		##****Legend
		leghumid = plt.legend()
		# get the lines and texts inside legend box
		leghumid_lines = leghumid.get_lines()
		leghumid_texts = leghumid.get_texts()
		# bulk-set the properties of all lines and texts
		plt.setp(leghumid_lines, linewidth=1)
		plt.setp(leghumid_texts, fontsize=10)
		##****Legend

		plt.xlabel('Time (EST)', fontsize=15)
		plt.ylabel('Relative Humidity (%RH)', fontsize=15)
		plt.title('node ID: '+nodeNAME[i]+', Loc: '+nodeLoc[i], fontsize=20)

		### y axis minor tick
		plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1))
		plt.subplot().tick_params(direction='in', width=1., length=10)
		plt.subplot().tick_params(direction='in', length=6,  which='minor')

		# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

		majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
		plt.subplot().xaxis.set_major_formatter(majorFormatter)
		plt.gcf().autofmt_xdate()
		humid1.show()
		plt.savefig('humidity_'+nodeNAME[i]+'.png',bbox_inches='tight')

	#************************************************************************************************************Humidity2
	if len(nodeNAME) > 1:
		humidCMP = plt.figure(figsize=(100, 100))

		title = ''

		for i in range(len(nodeLoc)):
			title = title+'node ID: '+nodeNAME[i]+', Loc: '+nodeLoc[i]+'\n'
			if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["huhih6130"]):
				plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["huhih6130"],label='light_humidity: hih6130, '+nodeNAME[i], linewidth=1)
			if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["huhtu21d"]):
				plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["huhtu21d"],label='met_humidity: htu21d, '+nodeNAME[i], linewidth=1)
			if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["husht25"]):
				plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["husht25"],label='chem_humidity: sht25, '+nodeNAME[i], linewidth=1)

		##****Legend
		leghumid = plt.legend()
		# get the lines and texts inside legend box
		leghumid_lines = leghumid.get_lines()
		leghumid_texts = leghumid.get_texts()
		# bulk-set the properties of all lines and texts
		plt.setp(leghumid_lines, linewidth=1)
		plt.setp(leghumid_texts, fontsize=10)
		##****Legend

		plt.xlabel('Time (EST)', fontsize=15)
		plt.ylabel('Relative Humidity (%RH)', fontsize=15)
		plt.title(title, fontsize=20)

		### y axis minor tick
		plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1))
		plt.subplot().tick_params(direction='in', width=1., length=10)
		plt.subplot().tick_params(direction='in', length=6,  which='minor')

		# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

		majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
		plt.subplot().xaxis.set_major_formatter(majorFormatter)
		plt.gcf().autofmt_xdate()
		humidCMP.show()
		plt.savefig('./humidity_all.png',bbox_inches='tight')


	#********************************************************************************************************Temperature1
def plot_temperature(nodeNAME, nodeLoc, data_dict):
	for i in range(len(nodeNAME)):
		temper1 = plt.figure(figsize=(100, 100))

		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["hih6130"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["hih6130"], label='light_temp: hih6130', linewidth=1, color="aqua")
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["tmp421"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["tmp421"], label='light_temp: tmp421', linewidth=1)


		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["htu21d"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["htu21d"],label='met_temp: htu21d', linewidth=1, color="greenyellow")
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["tmp112"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["tmp112"], label='met_temp: tmp112', linewidth=1)
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["bmp180"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["bmp180"], label='met_temp: bmp180', linewidth=1)
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["tsys01"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["tsys01"], label='met_temp: tsys01', linewidth=1)
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["pr103j2"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["pr103j2"], label='met_temp: pr103j2', linewidth=1)


		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["sht25"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["sht25"],label='chem_temp: sht25', linewidth=1, color="yellow")
		if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["lps25h"]):
			plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["lps25h"], label='chem_temp: lps25h', linewidth=1)

		##****Legend
		legtemper = plt.legend()
		# get the lines and texts inside legend box
		legtemper_lines = legtemper.get_lines()
		legtemper_texts = legtemper.get_texts()
		# bulk-set the properties of all lines and texts
		plt.setp(legtemper_lines, linewidth=1)
		plt.setp(legtemper_texts, fontsize=10)
		##****Legend

		plt.xlabel('Time (EST)', fontsize=15)
		plt.ylabel('Temperature (°C)', fontsize=15)
		plt.title('node ID: '+nodeNAME[i]+', Loc: '+nodeLoc[i],fontsize=20)

		### y axis minor tick
		plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1))
		plt.subplot().tick_params(direction='in', width=1., length=10)
		plt.subplot().tick_params(direction='in', length=6,  which='minor')

		# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

		majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
		plt.subplot().xaxis.set_major_formatter(majorFormatter)
		plt.gcf().autofmt_xdate()
		temper1.show()
		plt.savefig('temperature_'+nodeNAME[i]+'.png',bbox_inches='tight')

	#********************************************************************************************************Temperature2
	if len(nodeNAME) > 1:
		temperCMP = plt.figure(figsize=(100, 100))

		title = ''

		for i in range(len(nodeLoc)):
			title = title+'node ID: '+nodeNAME[i]+', Loc: '+nodeLoc[i]+'\n'
			if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["hih6130"]):
				plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["hih6130"], label='light_temp: hih6130, '+nodeNAME[i], linewidth=1)
			if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["htu21d"]):
				plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["htu21d"],label='met_temp: htu21d, '+nodeNAME[i], linewidth=1)
			if len(data_dict[nodeNAME[i]]["time"]) == len(data_dict[nodeNAME[i]]["sht25"]):
				plt.plot(data_dict[nodeNAME[i]]["time"],data_dict[nodeNAME[i]]["sht25"],label='chem_temp: sht25, '+nodeNAME[i], linewidth=1)

		##****Legend
		legtemper = plt.legend()
		# get the lines and texts inside legend box
		legtemper_lines = legtemper.get_lines()
		legtemper_texts = legtemper.get_texts()
		# bulk-set the properties of all lines and texts
		plt.setp(legtemper_lines, linewidth=1)
		plt.setp(legtemper_texts, fontsize=10)
		##****Legend

		plt.xlabel('Time (EST)', fontsize=15)
		plt.ylabel('Temperature (°C)', fontsize=15)
		plt.title(title, fontsize=20)

		### y axis minor tick
		plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1))
		plt.subplot().tick_params(direction='in', width=1., length=10)
		plt.subplot().tick_params(direction='in', length=6,  which='minor')

		# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

		majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
		plt.subplot().xaxis.set_major_formatter(majorFormatter)
		plt.gcf().autofmt_xdate()
		temperCMP.show()
		plt.savefig('./temperature_all.png',bbox_inches='tight')

	### to keep the images alive
	# input()

def plot_data(nodeNAME, nodeLoc, data_dict, args_plot):
	# from datetime import datetime

	# REMOVE ALL PNG FILES
	directory = './'
	test = os.listdir(directory)
	for item in test:
		# print (item)
		if item.endswith('.png') or item.endswith('.csv'):
			# print("endswith: ", item)
			os.remove('./'+item)

	if args_plot[0] == False and args_plot[1] == False and args_plot[2] == False:
		plot_temperature(nodeNAME, nodeLoc, data_dict)
		plot_humidity(nodeNAME, nodeLoc, data_dict)
		plot_pressrue(nodeNAME, nodeLoc, data_dict)
	else:
		if args_plot[0] == True:
			plot_temperature(nodeNAME, nodeLoc, data_dict)
		if args_plot[1] == True:
			plot_humidity(nodeNAME, nodeLoc, data_dict)
		if args_plot[2] == True:
			plot_pressrue(nodeNAME, nodeLoc, data_dict)

	input()

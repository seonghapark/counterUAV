
from RTlist import getRT
# import datetime

from datetime import datetime, timedelta
import sys

import subprocess
import shlex
import os

if len(sys.argv) < 2:
	print("add node name, the number of start day from today, end day from today, as arguments")
	print("for example: python3 simpler_plot.py EEF0 0 2")
	print("which means collect data of node name EEF0 from today to 2 days ahead")
	subprocess.call(['./livenode'])
	exit(1)

print(sys.argv)

# nodeNUM = int(sys.argv[1])

nodeNUM = sys.argv[1:-2]
datefrom = sys.argv[-2]
dateto = sys.argv[-1]

inputnodecount = len(nodeNUM)
print(inputnodecount)

print("node ID: ", nodeNUM, type(nodeNUM))
print("date from: ", datefrom, " date to: ", dateto)

nodeName = []
nodeLoc = []
data_dict = {}
for i in range(inputnodecount):
	# if os.path.exists('./sensor_data_set_'+nodeNUM[i]+'.csv') == False:
	# 	print("False")
	subprocess.call(['./reports/getdatasets', nodeNUM[i], datefrom, dateto])
	with open("./node_name") as f:
		for line in f:
			print("python: ", line)
			nodeName.append(line.strip())
			os.rename("./sensor_data_set.csv", "./sensor_data_set_"+nodeNUM[i]+".csv")
			# os.remove("./sensor_data_set.csv")
	with open("./node_loc") as f:
		for line in f:
			print("python: ", line)
			nodeLoc.append(line.strip())

	# nodeNUM = 0 # 0-3, 0 is 1st deployed or whatever node

	################################ Raw data from beehive1
	## including time

	data_dict[nodeNUM[i]] = {}

	### temperature
	data_dict[nodeNUM[i]]["tmp112"] = []
	data_dict[nodeNUM[i]]["bmp180"] = []
	data_dict[nodeNUM[i]]["tsys01"] = []
	data_dict[nodeNUM[i]]["pr103j2"] = []
	data_dict[nodeNUM[i]]["tmp421"] = []
	data_dict[nodeNUM[i]]["hih6130"] = []
	data_dict[nodeNUM[i]]["htu21d"] = []

	data_dict[nodeNUM[i]]["lps25h"] = []
	data_dict[nodeNUM[i]]["sht25"] = []

	data_dict[nodeNUM[i]]["co_adc_tmp"] = []
	data_dict[nodeNUM[i]]["co_lmp_tmp"] = []
	data_dict[nodeNUM[i]]["so2_adc_tmp"] = []
	data_dict[nodeNUM[i]]["o3_tmp"] = []
	data_dict[nodeNUM[i]]["irr_tmp"] = []

	### pressure
	data_dict[nodeNUM[i]]["pressbmp180"] = []
	data_dict[nodeNUM[i]]["presslps25h"] = []

	### humidity
	data_dict[nodeNUM[i]]["huhih4030"] = []
	data_dict[nodeNUM[i]]["huhih6130"] = []
	data_dict[nodeNUM[i]]["huhtu21d"] = []
	data_dict[nodeNUM[i]]["husht25"] = []

	### light
	data_dict[nodeNUM[i]]["apds"] = []
	data_dict[nodeNUM[i]]["ml8511"] = []
	data_dict[nodeNUM[i]]["mlx"] = []
	data_dict[nodeNUM[i]]["tsl260"] = []
	data_dict[nodeNUM[i]]["tsl250as"] = []
	data_dict[nodeNUM[i]]["tsl250ls"] = []

	data_dict[nodeNUM[i]]["rawapds"] = []
	data_dict[nodeNUM[i]]["rawml8511"] = []
	data_dict[nodeNUM[i]]["rawmlx"] = []
	data_dict[nodeNUM[i]]["rawtsl260"] = []
	data_dict[nodeNUM[i]]["rawtsl250as"] = []
	data_dict[nodeNUM[i]]["rawtsl250ls"] = []

	### time
	data_dict[nodeNUM[i]]["nytime"] = []
	time = 0

	# no data from 20eny and 20dny on 2017-08-17
	# nyinput = ['./nynode/209ny_2017-08-17.csv', './nynode/202ny_2017-08-17.csv', './nynode/20eny_2017-08-17.csv', './nynode/20dny_2017-08-17.csv']
	inputcsv = './sensor_data_set_'+nodeNUM[i]+'.csv'
	with open(inputcsv) as f:
		for line in f:

			newtime = line.strip().split(';')[1]
			if time != newtime:
				time = newtime
				# convtime = datetime.datetime.fromtimestamp(time)
				datetime_object = datetime.strptime(time, "%Y_%m_%d_%H:%M:%S")
				convtime = datetime_object - timedelta(hours=4)
				data_dict[nodeNUM[i]]["nytime"].append(convtime)

			if "temperature" in line:
				if "TMP112" in line:
					temperature = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["tmp112"].append(temperature)
				elif "BMP180" in line:
					temperature = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["bmp180"].append(temperature)
				elif "TSYS01" in line:
					temperature = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["tsys01"].append(temperature)
				elif "PR103J2" in line:
					pre_temperature = float(line.strip().split(';')[-1])
					temperature = round(getRT(pre_temperature), 2)
					data_dict[nodeNUM[i]]["pr103j2"].append(temperature)
				elif "TMP421" in line:
					temperature = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["tmp421"].append(temperature)
				elif "HIH6130" in line:
					temperature = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["hih6130"].append(temperature)
				elif "HTU21D" in line:
					temperature = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["htu21d"].append(temperature)
				elif "LPS25H" in line:
					temperature = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["lps25h"].append(temperature)
				elif "SHT25" in line:
					temperature = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["sht25"].append(temperature)
				elif "CO LMP Temp" in line:
					temperature = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["co_lmp_tmp"].append(temperature)
				elif "CO ADC Temp" in line:
					temperature = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["co_adc_tmp"].append(temperature)
				elif "SO2/H2S Temp" in line:
					temperature = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["so2_adc_tmp"].append(temperature)
				elif "O3/NO2 Temp" in line:
					temperature = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["o3_tmp"].append(temperature)
				elif "IAQ/IRR Temp" in line:
					temperature = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["irr_tmp"].append(temperature)

			elif "pressure" in line:
				if "BMP180" in line:
					pressure = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["pressbmp180"].append(pressure)
				elif "LPS25H" in line:
					pressure = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["presslps25h"].append(pressure)

			elif "humidity" in line:
				if "HIH6130" in line:
					humidity = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["huhih6130"].append(humidity)
				elif "SHT25" in line:
					pressure = float(line.strip().split(';')[-1])/100
					data_dict[nodeNUM[i]]["husht25"].append(pressure)
				elif "HTU21D" in line:
					humidity = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["huhtu21d"].append(humidity)
				elif "HIH4030" in line:
					humidity = float(line.strip().split(';')[-1]) * 5 / 1023 - 0.85
					humidity = humidity * 100 / 3
					data_dict[nodeNUM[i]]["huhih4030"].append(humidity)


			elif "intensity" in line:
				if "APDS-9006-020" in line:
					intensity = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["rawapds"].append(intensity)

					irrad = (intensity / 0.001944) / 405.1   # 405.1 unit: mA/lux
					data_dict[nodeNUM[i]]["apds"].append(irrad)
				elif "ML8511" in line:
					intensity = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["rawml8511"].append(intensity)
					intensity = intensity  * 0.0000625 * 2.50
					irrad = (intensity - 1) * 14.9916 / 0.12# - 18.71

					if 2.5 <= irrad <= 3.0:
						irrad = irrad - 0.3
					elif 3.0 <= irrad <= 4.0:
						irrad = irrad - 0.6
					elif 4.0 <= irrad <= 4.2:
						irrad = irrad - 0.4
					elif 4.5 < irrad:
						irrad = irrad + 0.25

					data_dict[nodeNUM[i]]["ml8511"].append(irrad)
				elif "MLX75305" in line:
					intensity = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["rawmlx"].append(intensity)
					irrad = (intensity  * 0.0000625 * 2.50 - 0.09234) / 0.007   #with gain 1, the factor is 7mA/(uW/cm^2)
					data_dict[nodeNUM[i]]["mlx"].append(irrad)
				elif "TSL260RD" in line:
					intensity = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["rawtsl260"].append(intensity)
					irrad = (intensity  * 0.0000625 * 2.50 - 0.006250) / 0.058
					data_dict[nodeNUM[i]]["tsl260"].append(irrad)
				elif "TSL250RD-AS" in line:
					intensity = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["rawtsl250as"].append(intensity)
					irrad = intensity  * 0.0000625 * 2.5 / 0.064
					data_dict[nodeNUM[i]]["tsl250as"].append(irrad)
				elif "TSL250RD-LS" in line:
					intensity = float(line.strip().split(';')[-1])
					data_dict[nodeNUM[i]]["rawtsl250ls"].append(intensity)
					irrad = (intensity * 0.0000625 * 2.5 - 0.005781) / 0.064
					data_dict[nodeNUM[i]]["tsl250ls"].append(irrad)

print(nodeName, nodeLoc, nodeNUM)

# # ############################################################# PLOT data
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
# from datetime import datetime

# REMOVE ALL PNG FILES
directory = './'
test = os.listdir(directory)
for item in test:
	print (item)
	if item.endswith('.png') or item.endswith('.csv'):
		print("endswith: ", item)
		os.remove('./'+item)

#************************************************************************************Pressure1

for i in range(len(nodeName)):
	pressure1 = plt.figure(figsize=(100, 100))
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["pressbmp180"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["pressbmp180"],label='met_pressure: bmp180', linewidth=3)
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["presslps25h"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["presslps25h"],label='chem_pressure: lps25h', linewidth=3)

	##****Legend

	legpressurewhole = plt.legend()
	# get the lines and texts inside legend box
	legpressurewhole_lines = legpressurewhole.get_lines()
	legpressurewhole_texts = legpressurewhole.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(legpressurewhole_lines, linewidth=4)
	plt.setp(legpressurewhole_texts, fontsize='x-large')
	##****Legend

	plt.xlabel('Time (EST)', fontsize=25)
	plt.ylabel('Pressure (hPa)', fontsize=25)
	plt.title(nodeName[i]+', Loc: '+nodeLoc[i], fontsize= 30)

	### y axis minor tick
	plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1000))
	plt.subplot().tick_params(direction='in', width=1., length=10)
	plt.subplot().tick_params(direction='in', length=6,  which='minor')

	# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

	majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
	plt.subplot().xaxis.set_major_formatter(majorFormatter)
	plt.gcf().autofmt_xdate()
	pressure1.show()
	# plt.savefig('pressure'+nodeName[i]+nodeLoc[i]+'.png',bbox_inches='tight')

# #*********************************************************************************************Pressrue2

if len(nodeName) > 1:
	pressureCMP = plt.figure(figsize=(100, 100))

	title = ''

	for i in range(len(nodeLoc)):
		if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["pressbmp180"]):
			plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["pressbmp180"],label='met_pressure: bmp180, '+nodeLoc[i], linewidth=3)
			title = title+nodeName[i]+', '+nodeLoc[i]+' & '
		# if len(data_dict[nodeNUM[1]]["nytime"]) == len(data_dict[nodeNUM[1]]["pressbmp180"]):
		# 	plt.plot(data_dict[nodeNUM[1]]["nytime"],data_dict[nodeNUM[1]]["pressbmp180"],label='met_pressure: bmp180, '+nodeLoc[1], linewidth=3)

	##****Legend
	legpressurewhole = plt.legend()
	# get the lines and texts inside legend box
	legpressurewhole_lines = legpressurewhole.get_lines()
	legpressurewhole_texts = legpressurewhole.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(legpressurewhole_lines, linewidth=4)
	plt.setp(legpressurewhole_texts, fontsize='x-large')
	##****Legend

	plt.xlabel('Time (EST)', fontsize=25)
	plt.ylabel('Pressure (hPa)', fontsize=25)
	plt.title(title, fontsize= 30)

	### y axis minor tick
	plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1000))
	plt.subplot().tick_params(direction='in', width=1., length=10)
	plt.subplot().tick_params(direction='in', length=6,  which='minor')

	# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

	majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
	plt.subplot().xaxis.set_major_formatter(majorFormatter)
	plt.gcf().autofmt_xdate()
	pressureCMP.show()
	# plt.savefig('pressure_CMP.png',bbox_inches='tight')

# #************************************************************************************************************Humidity1
for i in range(len(nodeName)):
	humid1 = plt.figure(figsize=(100, 100))
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["huhih6130"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["huhih6130"],label='light_humidity: hih6130', linewidth=3, color="aqua")
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["huhtu21d"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["huhtu21d"],label='met_humidity: htu21d', linewidth=3, color="greenyellow")
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["husht25"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["husht25"],label='chem_humidity: sht25', linewidth=3, color="yellow")
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["huhih4030"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["huhih4030"],label='met_humidity: hih4030', linewidth=3)

	##****Legend
	leghumid = plt.legend()
	# get the lines and texts inside legend box
	leghumid_lines = leghumid.get_lines()
	leghumid_texts = leghumid.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(leghumid_lines, linewidth=4)
	plt.setp(leghumid_texts, fontsize=20)
	##****Legend

	plt.xlabel('Time (EST)', fontsize=25)
	plt.ylabel('Relative Humidity (%RH)', fontsize=25)
	plt.title(nodeName[i]+', '+nodeLoc[i], fontsize= 30)

	### y axis minor tick
	plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1))
	plt.subplot().tick_params(direction='in', width=1., length=10)
	plt.subplot().tick_params(direction='in', length=6,  which='minor')

	# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

	majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
	plt.subplot().xaxis.set_major_formatter(majorFormatter)
	plt.gcf().autofmt_xdate()
	humid1.show()
	# plt.savefig('humidity'+nodeName[i]+nodeLoc[i]+'.png',bbox_inches='tight')

#************************************************************************************************************Humidity2
if len(nodeName) > 1:
	humidCMP = plt.figure(figsize=(100, 100))

	title = ''

	for i in range(len(nodeLoc)):
		title = title+nodeName[i]+', '+nodeLoc[i]+' & '
		if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["huhih6130"]):
			plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["huhih6130"],label='light_humidity: hih6130, '+nodeLoc[i], linewidth=3)
		if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["huhtu21d"]):
			plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["huhtu21d"],label='met_humidity: htu21d, '+nodeLoc[i], linewidth=3)
		if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["husht25"]):
			plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["husht25"],label='chem_humidity: sht25, '+nodeLoc[i], linewidth=3)

	##****Legend
	leghumid = plt.legend()
	# get the lines and texts inside legend box
	leghumid_lines = leghumid.get_lines()
	leghumid_texts = leghumid.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(leghumid_lines, linewidth=4)
	plt.setp(leghumid_texts, fontsize=20)
	##****Legend

	plt.xlabel('Time (EST)', fontsize=25)
	plt.ylabel('Relative Humidity (%RH)', fontsize=25)
	plt.title(title, fontsize= 30)

	### y axis minor tick
	plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1))
	plt.subplot().tick_params(direction='in', width=1., length=10)
	plt.subplot().tick_params(direction='in', length=6,  which='minor')

	# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

	majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
	plt.subplot().xaxis.set_major_formatter(majorFormatter)
	plt.gcf().autofmt_xdate()
	humidCMP.show()
	# plt.savefig('humidity_CMP.png',bbox_inches='tight')


#********************************************************************************************************Temperature1
for i in range(len(nodeName)):
	temper1 = plt.figure(figsize=(100, 100))

	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["hih6130"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["hih6130"], label='light_temp: hih6130', linewidth=3, color="aqua")
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["tmp421"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["tmp421"], label='light_temp: tmp421', linewidth=3)


	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["htu21d"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["htu21d"],label='met_temp: htu21d', linewidth=3, color="greenyellow")
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["tmp112"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["tmp112"], label='met_temp: tmp112', linewidth=3)
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["bmp180"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["bmp180"], label='met_temp: bmp180', linewidth=3)
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["tsys01"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["tsys01"], label='met_temp: tsys01', linewidth=3)
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["pr103j2"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["pr103j2"], label='met_temp: pr103j2', linewidth=3)


	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["sht25"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["sht25"],label='chem_temp: sht25', linewidth=3, color="yellow")
	if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["lps25h"]):
		plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["lps25h"], label='chem_temp: lps25h', linewidth=3)

	##****Legend
	legtemper = plt.legend()
	# get the lines and texts inside legend box
	legtemper_lines = legtemper.get_lines()
	legtemper_texts = legtemper.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(legtemper_lines, linewidth=4)
	plt.setp(legtemper_texts, fontsize=20)
	##****Legend

	plt.xlabel('Time (EST)', fontsize=25)
	plt.ylabel('Temperature (°C)', fontsize=25)
	plt.title(nodeName[0]+', '+nodeLoc[0],fontsize= 30)

	### y axis minor tick
	plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1))
	plt.subplot().tick_params(direction='in', width=1., length=10)
	plt.subplot().tick_params(direction='in', length=6,  which='minor')

	# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

	majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
	plt.subplot().xaxis.set_major_formatter(majorFormatter)
	plt.gcf().autofmt_xdate()
	temper1.show()
	# plt.savefig('temperature'+nodeName[i]+', '+nodeLoc[i]+'.png',bbox_inches='tight')

#********************************************************************************************************Temperature2
if len(nodeName) > 1:
	temperCMP = plt.figure(figsize=(100, 100))

	title = ''

	for i in range(len(nodeLoc)):
		title = title+nodeName[i]+', '+nodeLoc[i]+' & '
		if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["hih6130"]):
			plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["hih6130"], label='light_temp: hih6130, '+nodeLoc[i], linewidth=3)
		if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["htu21d"]):
			plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["htu21d"],label='met_temp: htu21d, '+nodeLoc[i], linewidth=3)
		if len(data_dict[nodeNUM[i]]["nytime"]) == len(data_dict[nodeNUM[i]]["sht25"]):
			plt.plot(data_dict[nodeNUM[i]]["nytime"],data_dict[nodeNUM[i]]["sht25"],label='chem_temp: sht25, '+nodeLoc[i], linewidth=3)

	##****Legend
	legtemper = plt.legend()
	# get the lines and texts inside legend box
	legtemper_lines = legtemper.get_lines()
	legtemper_texts = legtemper.get_texts()
	# bulk-set the properties of all lines and texts
	plt.setp(legtemper_lines, linewidth=4)
	plt.setp(legtemper_texts, fontsize=20)
	##****Legend

	plt.xlabel('Time (EST)', fontsize=25)
	plt.ylabel('Temperature (°C)', fontsize=25)
	plt.title(title,fontsize= 30)

	### y axis minor tick
	plt.subplot().yaxis.set_minor_locator(ticker.MultipleLocator(1))
	plt.subplot().tick_params(direction='in', width=1., length=10)
	plt.subplot().tick_params(direction='in', length=6,  which='minor')

	# majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')

	majorFormatter = matplotlib.dates.DateFormatter('%m-%d %H:%M')
	plt.subplot().xaxis.set_major_formatter(majorFormatter)
	plt.gcf().autofmt_xdate()
	temperCMP.show()
	# plt.savefig('temperature_CMP.png',bbox_inches='tight')

### to keep the images alive
input()

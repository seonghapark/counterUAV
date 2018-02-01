
from datetime import datetime, timedelta
from RTlist import getRT


def read_data(nodeNAME):
	data_dict = {}
	for i in range(len(nodeNAME)):
		################################ Raw data from beehive1
		## including time

		data_dict[nodeNAME[i]] = {}

		### temperature
		data_dict[nodeNAME[i]]["tmp112"] = []
		data_dict[nodeNAME[i]]["bmp180"] = []
		data_dict[nodeNAME[i]]["tsys01"] = []
		data_dict[nodeNAME[i]]["pr103j2"] = []
		data_dict[nodeNAME[i]]["tmp421"] = []
		data_dict[nodeNAME[i]]["hih6130"] = []
		data_dict[nodeNAME[i]]["htu21d"] = []

		data_dict[nodeNAME[i]]["lps25h"] = []
		data_dict[nodeNAME[i]]["sht25"] = []

		data_dict[nodeNAME[i]]["co_adc_tmp"] = []
		data_dict[nodeNAME[i]]["co_lmp_tmp"] = []
		data_dict[nodeNAME[i]]["so2_adc_tmp"] = []
		data_dict[nodeNAME[i]]["o3_tmp"] = []
		data_dict[nodeNAME[i]]["irr_tmp"] = []

		### pressure
		data_dict[nodeNAME[i]]["pressbmp180"] = []
		data_dict[nodeNAME[i]]["presslps25h"] = []

		### humidity
		data_dict[nodeNAME[i]]["huhih4030"] = []
		data_dict[nodeNAME[i]]["huhih6130"] = []
		data_dict[nodeNAME[i]]["huhtu21d"] = []
		data_dict[nodeNAME[i]]["husht25"] = []

		### light
		data_dict[nodeNAME[i]]["apds"] = []
		data_dict[nodeNAME[i]]["ml8511"] = []
		data_dict[nodeNAME[i]]["mlx"] = []
		data_dict[nodeNAME[i]]["tsl260"] = []
		data_dict[nodeNAME[i]]["tsl250as"] = []
		data_dict[nodeNAME[i]]["tsl250ls"] = []

		data_dict[nodeNAME[i]]["rawapds"] = []
		data_dict[nodeNAME[i]]["rawml8511"] = []
		data_dict[nodeNAME[i]]["rawmlx"] = []
		data_dict[nodeNAME[i]]["rawtsl260"] = []
		data_dict[nodeNAME[i]]["rawtsl250as"] = []
		data_dict[nodeNAME[i]]["rawtsl250ls"] = []

		data_dict[nodeNAME[i]]["SIR"] = []
		data_dict[nodeNAME[i]]["SUV"] = []
		data_dict[nodeNAME[i]]["SVL"] = []

		### sound level sensor
		data_dict[nodeNAME[i]]["spv"] = []

		### magnetic field
		data_dict[nodeNAME[i]]["magx"] = []
		data_dict[nodeNAME[i]]["magy"] = []
		data_dict[nodeNAME[i]]["magz"] = []
		data_dict[nodeNAME[i]]["magrms"] = []

		### accelerometer
		data_dict[nodeNAME[i]]["accx"] = []
		data_dict[nodeNAME[i]]["accy"] = []
		data_dict[nodeNAME[i]]["accz"] = []

		### chemical sensor
		data_dict[nodeNAME[i]]["irr"] = []
		data_dict[nodeNAME[i]]["iaq"] = []
		data_dict[nodeNAME[i]]["no2"] = []
		data_dict[nodeNAME[i]]["so2"] = []
		data_dict[nodeNAME[i]]["h2s"] = []
		data_dict[nodeNAME[i]]["o3"] = []
		data_dict[nodeNAME[i]]["co"] = []

		### time
		data_dict[nodeNAME[i]]["time"] = []
		time = 0


		inputcsv = './sensor_data_set_'+nodeNAME[i]+'.csv'
		with open(inputcsv) as f:
			for line in f:

				newtime = line.strip().split(';')[1]
				if time != newtime:
					time = newtime

					datetime_object = datetime.strptime(time, "%Y_%m_%d_%H:%M:%S")
					convtime = datetime_object - timedelta(hours=4)
					data_dict[nodeNAME[i]]["time"].append(convtime)

				if "temperature" in line:
					if "TMP112" in line:
						temperature = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["tmp112"].append(temperature)
					elif "BMP180" in line:
						temperature = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["bmp180"].append(temperature)
					elif "TSYS01" in line:
						temperature = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["tsys01"].append(temperature)
					elif "PR103J2" in line:
						pre_temperature = float(line.strip().split(';')[-1])
						temperature = round(getRT(pre_temperature), 2)
						data_dict[nodeNAME[i]]["pr103j2"].append(temperature)
					elif "TMP421" in line:
						temperature = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["tmp421"].append(temperature)
					elif "HIH6130" in line:
						temperature = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["hih6130"].append(temperature)
					elif "HTU21D" in line:
						temperature = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["htu21d"].append(temperature)
					elif "LPS25H" in line:
						temperature = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["lps25h"].append(temperature)
					elif "SHT25" in line:
						temperature = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["sht25"].append(temperature)
					elif "CO LMP Temp" in line:
						temperature = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["co_lmp_tmp"].append(temperature)
					elif "CO ADC Temp" in line:
						temperature = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["co_adc_tmp"].append(temperature)
					elif "SO2/H2S Temp" in line:
						temperature = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["so2_adc_tmp"].append(temperature)
					elif "O3/NO2 Temp" in line:
						temperature = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["o3_tmp"].append(temperature)
					elif "IAQ/IRR Temp" in line:
						temperature = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["irr_tmp"].append(temperature)

				elif "pressure" in line:
					if "BMP180" in line:
						pressure = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["pressbmp180"].append(pressure)
					elif "LPS25H" in line:
						pressure = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["presslps25h"].append(pressure)

				elif "humidity" in line:
					if "HIH6130" in line:
						humidity = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["huhih6130"].append(humidity)
					elif "SHT25" in line:
						pressure = float(line.strip().split(';')[-1])/100
						data_dict[nodeNAME[i]]["husht25"].append(pressure)
					elif "HTU21D" in line:
						humidity = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["huhtu21d"].append(humidity)
					elif "HIH4030" in line:
						humidity = float(line.strip().split(';')[-1]) * 5 / 1023 - 0.85
						humidity = humidity * 100 / 3
						data_dict[nodeNAME[i]]["huhih4030"].append(humidity)


				elif "intensity" in line:
					if "APDS-9006-020" in line:
						intensity = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["rawapds"].append(intensity)

						irrad = (intensity / 0.001944) / 405.1   # 405.1 unit: mA/lux
						data_dict[nodeNAME[i]]["apds"].append(irrad)
					elif "ML8511" in line:
						intensity = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["rawml8511"].append(intensity)
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

						data_dict[nodeNAME[i]]["ml8511"].append(irrad)
					elif "MLX75305" in line:
						intensity = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["rawmlx"].append(intensity)
						irrad = (intensity  * 0.0000625 * 2.50 - 0.09234) / 0.007   #with gain 1, the factor is 7mA/(uW/cm^2)
						data_dict[nodeNAME[i]]["mlx"].append(irrad)
					elif "TSL260RD" in line:
						intensity = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["rawtsl260"].append(intensity)
						irrad = (intensity  * 0.0000625 * 2.50 - 0.006250) / 0.058
						data_dict[nodeNAME[i]]["tsl260"].append(irrad)
					elif "TSL250RD-AS" in line:
						intensity = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["rawtsl250as"].append(intensity)
						irrad = intensity  * 0.0000625 * 2.5 / 0.064
						data_dict[nodeNAME[i]]["tsl250as"].append(irrad)
					elif "TSL250RD-LS" in line:
						intensity = float(line.strip().split(';')[-1])
						data_dict[nodeNAME[i]]["rawtsl250ls"].append(intensity)
						irrad = (intensity * 0.0000625 * 2.5 - 0.005781) / 0.064
						data_dict[nodeNAME[i]]["tsl250ls"].append(irrad)

	return data_dict

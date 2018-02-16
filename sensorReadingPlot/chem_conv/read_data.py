
from datetime import datetime, timedelta
from RTlist import getRT

from chemsense import convert, import_data

def new_line(splited, value):
    new_row = ''
    for i in range(len(splited) - 1):
        new_row = new_row + splited[i] + ';'
    new_row = new_row + str(round(value, 2)) + '\n'
    return new_row

def new_line_chem(key, in_list):
    ppm = in_list[0]
    splited = in_list[1].strip().split(';')
    new_row = new_line(splited, ppm)
    return new_row

def intensity_conv(line):
	splited = line.strip().split(';')
	if "APDS-9006-020" in line:
		intensity = float(splited[-1])/ 0.001944
		irrad = intensity / 405.1   # 405.1 unit: mA/lux
		line = new_line(splited, irrad)
	elif "ML8511" in line:
		intensity = float(splited[-1]) * 0.0000625 * 2.50
		irrad = (intensity - 1) * 14.9916 / 0.12# - 18.71

		if 2.5 <= irrad <= 3.0:
			irrad = irrad - 0.3
		elif 3.0 <= irrad <= 4.0:
			irrad = irrad - 0.6
		elif 4.0 <= irrad <= 4.2:
			irrad = irrad - 0.4
		elif 4.5 < irrad:
			irrad = irrad + 0.25

		line = new_line(splited, irrad)
	elif "MLX75305" in line:
		intensity = float(splited[-1]) * 0.0000625 * 2.50 - 0.09234
		irrad = intensity / 0.007   #with gain 1, the factor is 7mA/(uW/cm^2)
		line = new_line(splited, irrad)
	elif "TSL260RD" in line:
		intensity = float(splited[-1]) * 0.0000625 * 2.50 - 0.006250
		irrad = intensity / 0.058
		line = new_line(splited, irrad)
	elif "TSL250RD-AS" in line:
		irrad = float(splited[-1]) * 0.0000625 * 2.5 / 0.064
		line = new_line(splited, irrad)
	elif "TSL250RD-LS" in line:
		intensity = float(splited[-1]) * 0.0000625 * 2.5 - 0.005781
		irrad = intensity / 0.064
		line = new_line(splited, irrad)

	return line

def pick_value(line, value, first_sensor, count, xl_data):
	write_bool = True
	splited = line.strip().split(';')
	if "adc_temperature" in line:
		temperature = float(splited[-1])/100
		line = new_line(splited, temperature)
		value['temp'] = value['temp'] + temperature
	elif "Chemsense" in line:
		if "ID" in line:
			value['id'] = splited[-1]
		else:
			chem_reading = float(splited[-1])
			value[splited[-2]] = [chem_reading, line]
			write_bool = False

	elif "pressure" in line:
		pressure = float(splited[-1])/100
		line = new_line(splited, pressure)

	elif "HTU21D" in line and "temperature" in line:
		temperature = float(splited[-1])
		line = new_line(splited, temperature)
	elif "PR103J2" in line:
		pre_temperature = float(splited[-1])
		temperature = round(getRT(pre_temperature), 2)
		line = new_line(splited, temperature)
	elif "LPS25H" in line:
		temperature = float(splited[-1])/100
		line = new_line(splited, temperature)
	elif "SHT25" in line:
		if "temperature" in line:
			temperature = float(splited[-1])/100
			line = new_line(splited, temperature)
		elif "humidity" in line:
			humidity = float(splited[-1])/100
			line = new_line(splited, humidity)
	elif "HIH4030" in line:
		humidity = float(splited[-1]) * 5 / 1024
		humidity = humidity * 30.68 + 0.958
		line = new_line(splited, humidity)

	elif "intensity" in line:
		line = intensity_conv(line)

	return line, value, write_bool

def acquire_sensor_spec(line):
	first_sensor = line.strip().split(';')[-3]
	sensor_type = line.strip().split(';')[-2]
	if first_sensor == 'Chemsense' or sensor_type == 'adc_temperature':
		first_sensor = ''

	return first_sensor

def read_data(nodeNAME, xl_data):
	first_sensor = ''
	count = 0
	chem_reading = {'temp': 0, 'id': ''}
	for i in range(len(nodeNAME)):
		outputcsv = './conv_data_set_'+nodeNAME[i]+'.csv'
		inputcsv = './sensor_data_set_'+nodeNAME[i]+'.csv'
		with open(inputcsv) as f:
			with open(outputcsv, 'w') as of:
				for line in f:
					if not first_sensor:
						first_sensor = acquire_sensor_spec(line)

					if chem_reading['id'] != '' and count != 0 and line.strip().split(';')[-3] == first_sensor:
						new_chem_value = convert(chem_reading, xl_data)
						for key, in_list in new_chem_value.items():
							if key != 'id' and key != 'temp':
								new_line = new_line_chem(key, in_list)
								of.write(new_line)
						chem_reading = {'temp': 0, 'id': ''}
					line, value, write_bool = pick_value(line, chem_reading, first_sensor, count, xl_data)
					if write_bool == True:
						of.write(line)
					count = count + 1

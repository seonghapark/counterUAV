# Conversion for chemsense
# chemsense version2, no data of IMU is comming from chemsense --> chemsense FW issue

import math

import dataset
import xlrd

def import_data(xl_data):
    xl_data = {}
    # directory of the sensor calibration data
    directory = "./calib_data.xlsx"

    db = dataset.connect()
    xl = xlrd.open_workbook(directory, "rb")

    for i, sheet in enumerate(xl.sheets()):
        for rownum in range(sheet.nrows):
            rowValues = sheet.row_values(rownum)
            if '088' in str(rowValues[0]):
                xl_data[str(rowValues[1])] = {
                    'Ireducing_gases':{'sensitivity': rowValues[9], 'baseline40': rowValues[30], 'Mvalue': rowValues[44]},   # IRR = RESP, baseline = Izero@25C
                    'oxidizing_gases': {'sensitivity': rowValues[10], 'baseline40': rowValues[31], 'Mvalue': rowValues[45]},
                    'so2': {'sensitivity': rowValues[11], 'baseline40': rowValues[32], 'Mvalue': rowValues[46]},
                    'h2s': {'sensitivity': rowValues[12], 'baseline40': rowValues[33], 'Mvalue': rowValues[47]},
                    'o3': {'sensitivity': rowValues[13], 'baseline40': rowValues[34], 'Mvalue': rowValues[48]},
                    'no2': {'sensitivity': rowValues[14], 'baseline40': rowValues[35], 'Mvalue': rowValues[49]},
                    'co': {'sensitivity': rowValues[15], 'baseline40': rowValues[36], 'Mvalue': rowValues[50]}
                }

    return xl_data


def chemical_sensor(value, xl_data):
    for key, in_list in value.items():
        if key != 'id' and key != 'temp':
            IpA = value[key][0]

            Tzero = 40.0

            if value['id'] in xl_data:
                Tavg = value['temp']
                sensitivity = xl_data[value['id']][key]['sensitivity']
                baseline = xl_data[value['id']][key]['baseline40']
                Minv = xl_data[value['id']][key]['Mvalue']

                InA = float(IpA)/1000.0 - baseline*math.exp((Tavg - Tzero) / Minv)
                converted = InA / sensitivity
                value[key][0] = converted
            else:
                value[key][0] = IpA / 1000

    return value


def convert(value, xl_data):
    if value['temp'] == 0:
        return 0
    else:
        base_temperature = round((value['temp'] / 5), 2)
        chemical_sensor(value, xl_data)

    return value

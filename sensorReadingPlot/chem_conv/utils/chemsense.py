# Conversion for chemsense
# chemsense version2, no data of IMU is comming from chemsense --> chemsense FW issue

import math

import dataset
import xlrd

mid_dict = {}
imported_data = {}

def import_data():
    xl_data = {}
    # directory of the sensor calibration data
    directory = "/home/sager/Downloads/calib_data.xlsx"

    db = dataset.connect()
    xl = xlrd.open_workbook(directory, "rb")

    for i, sheet in enumerate(xl.sheets()):
        for rownum in range(sheet.nrows):
            rowValues = sheet.row_values(rownum)
            if '088' in str(rowValues[0]):
                xl_data[str(rowValues[1])] = {
                    'IRR':{'sensitivity': rowValues[9], 'baseline40': rowValues[30], 'Mvalue': rowValues[44]},   # IRR = RESP, baseline = Izero@25C
                    'IAQ': {'sensitivity': rowValues[10], 'baseline40': rowValues[31], 'Mvalue': rowValues[45]},
                    'SO2': {'sensitivity': rowValues[11], 'baseline40': rowValues[32], 'Mvalue': rowValues[46]},
                    'H2S': {'sensitivity': rowValues[12], 'baseline40': rowValues[33], 'Mvalue': rowValues[47]},
                    'OZO': {'sensitivity': rowValues[13], 'baseline40': rowValues[34], 'Mvalue': rowValues[48]},
                    'NO2': {'sensitivity': rowValues[14], 'baseline40': rowValues[35], 'Mvalue': rowValues[49]},
                    'CMO': {'sensitivity': rowValues[15], 'baseline40': rowValues[36], 'Mvalue': rowValues[50]}
                }

    return xl_data


def key_unit(k):
    if 'T' in k:
        return 'C'
    if 'P' in k:
        return 'hPa'

    return '%RH'


def chemical_sensor(ky, IpA):
    global imported_data
    Tzero = 40.0

    if len(imported_data) == 0:
        imported_data = import_data()

    if mid_dict['BAD'] in imported_data:
        Tavg = (float(mid_dict['AT0']) + float(mid_dict['AT1']) + float(mid_dict['AT2']) + float(mid_dict['AT3']) + float(mid_dict['LTM'])) / 500.0

        sensitivity = imported_data[mid_dict['BAD']][ky]['sensitivity']
        baseline = imported_data[mid_dict['BAD']][ky]['baseline40']
        Minv = imported_data[mid_dict['BAD']][ky]['Mvalue']

        InA = float(IpA)/1000.0 - baseline*math.exp((Tavg - Tzero) / Minv)
        converted = InA / sensitivity
        return converted, 'ppm'
    else:
        return IpA, 'raw'


def convert_pair(key, val):
    if 'BAD' in key:
        chem_id = val
        return 'id', val, ''
    if 'SH' in key or 'HD' in key or 'LP' in key or 'AT' in key or 'LT' in key:
        return key, float(val)/100.0, key_unit(key)
    if 'SVL' in key or 'SIR' in key or 'SUV' in key:
        return key, int(val), 'raw'
    if 'AC' in key or 'GY' in key or 'VIX' in key or 'OIX' in key:
        return key, int(val), 'raw'

    conv_val, unit = chemical_sensor(key, val)
    return key, conv_val, unit


def convert(value):
    global mid_dict

    chem_dict = {}
    mid_dict = {}
    for pair in value['chemsense_raw'].split():
        try:
            key, val = pair.split('=')
        except ValueError:
            continue

        # ignore sequence number
        if key == 'SQN':
            continue

        mid_dict[key] = val

    for key, value in mid_dict.items():
        k, v, u = convert_pair(key, val)
        chem_dict['chemsense_' + k.lower()] = (v, u)

    return chem_dict

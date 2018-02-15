# Conversion for HIH6130 temperature

# temperature value (x - do not care)
# bbbbbbbb bbbbbbxx
# y (C) = x / (2^14-1) * 165 - 40
# -40 C = 0 counts
# 125 C = 2^14 - 1 counts

def convert(value):
    raw_t = value['lightsense_hih6130_temperature']
    raw_h = value['lightsense_hih6130_humidity']

    # masked_t = (raw_t >> 2) & 0x3FFF
    temperature = float(raw_t / 4) * 1.0071415e-2 - 40.0

    masked_h = raw_h & 0x3FFF
    humidity = float(masked_h) * 6.103888e-3

    value['lightsense_hih6130_temperature'] = (round(temperature, 2), 'C')
    value['lightsense_hih6130_humidity'] = (round(humidity, 2), '%RH')

    return value

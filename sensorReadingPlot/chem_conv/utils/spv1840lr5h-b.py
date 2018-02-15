# Conversion for SPV1840LR5H-B

# V_I = (SPV_TSL_RAW - 1.75) / 453.33 - 1.75   # raw voltage of SPV
# SPV_RAW = (-V_I * 1023.00) / 5.00          # raw integer [0, 1023] of SPV

import math


def convert(value):
    raw_s = value['metsense_spv1840lr5h-b']

    def convert_to_db(value):
        mx = max(value)
        mn = min(value)
        ptp = mx - mn

        # count = 0
        if ptp < 1:
            ptp = 0.82
            # # sound level is lower than the lower limit of analogRead
            # # need to figure out how to estimate analogRead level

        value_voltage = ptp * 5.0 / 1024.0
        Pa = value_voltage / 0.03560778
        dBSPL = 20 * math.log10(Pa / 0.0002)
        return dBSPL

    reading = []
    for i in range(1, len(raw_s), 2):
        value_raw = (raw_s[i - 1] << 8) | raw_s[i]
        reading.append(value_raw)

    # if value_dB is lower than 55 dB, the value_dB is a guessed value not measured value
    # becasue of the lower limit of sensor reading through analogRead function
    value_dB = convert_to_db(reading)
    value['metsense_spv1840lr5h-b'] = (round(value_dB, 2), 'dB')

    return value

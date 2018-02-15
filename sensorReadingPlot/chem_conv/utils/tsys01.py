# Conversion for TSYS01 temperature

def convert(value):
    # coefficients
    c4 = 5714
    c3 = 7338
    c2 = 15996
    c1 = 22746
    c0 = 34484


    # assert len(coefficients) == 5
    raw_t = value['metsense_tsys01_temperature']
    raw_t >>= 8

    temperature = round((-2.0 * c4 * pow(10, -21) * pow(raw_t, 4) + \
        4.0 * c3 * pow(10, -16) * pow(raw_t, 3) + \
        -2.0 * c2 * pow(10, -11) * pow(raw_t, 2) + \
        1.0 * c1 * pow(10, -6) * raw_t + \
        -1.5 * c0 * pow(10, -2)), 2)

    value['metsense_tsys01_temperature'] = (temperature, 'C')

    return value

# Conversion for HMC5883L Magnetometer
    # converted_value = float(value) / 1100 (or 980)

def convert(value):
    raw_magx = value['lightsense_hmc5883l_hx']
    raw_magy = value['lightsense_hmc5883l_hy']
    raw_magz = value['lightsense_hmc5883l_hz']

    # print(raw_magx, raw_magy, raw_magz)

    raw_magx = round(raw_magx / 1100, 2)
    raw_magy = round(raw_magy / 1100, 2)
    raw_magz = round(raw_magz / 980, 2)

    value['lightsense_hmc5883l_hx'] = (raw_magx, 'Gx')
    value['lightsense_hmc5883l_hy'] = (raw_magy, 'Gy')
    value['lightsense_hmc5883l_hz'] = (raw_magz, 'Gz')

    return value
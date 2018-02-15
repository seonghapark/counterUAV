# Conversion for TSL250RD in Metsense

def convert(value):
    raw_l = value['metsense_tsl250rd_light']
    
    value_voltage = (raw_l * 3.3) / 1024.0
    
    # a = (math.log10(0.04)-math.log10(0.6))/(math.log10(0.6)-1)
    # b = math.log10(3)/(a*math.log10(50))
    # irrad = 10**((math.log10(input) - b)/a)

    irrad = round(value_voltage / 0.064, 4)

    # value['metsense_tsl250rd_light'] = (irrad, 'uW/cm^2')
    value['metsense_tsl250rd_light'] = (raw_l, 'raw')

    return value
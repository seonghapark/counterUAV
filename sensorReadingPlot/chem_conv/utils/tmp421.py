# Conversion for TMP421 temperature

def convert(value):
    raw_t = value['lightsense_tmp421']

    converted_value = 0.0
    h = (raw_t >> 8) & 0xFF
    l = raw_t & 0xFF
    
    bit = ((l >> 4) & 0x01) * 0.5
    converted_value += pow(bit, 4)

    bit = ((l >> 5) & 0x01) * 0.5
    converted_value += pow(bit, 3)

    bit = ((l >> 6) & 0x01) * 0.5
    converted_value += pow(bit, 2)

    bit = ((l >> 7) & 0x01) * 0.5
    converted_value += bit

    converted_value += h
    converted_value = round(converted_value, 2)

    if converted_value > 128.0:
        converted_value -= 256.0

    value['lightsense_tmp421'] = (converted_value, 'C')
    

    return value
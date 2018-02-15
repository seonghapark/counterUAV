# Conversion for ML8511

def convert(value):
    raw_l = value['lightsense_ml8511']
    
    # MCP output code transform factor 0.065 mV/(uW/cm^2): MCP mux
    value_voltage = raw_l * 0.0000625
    # voltage divider factor 5/2 to calc input voltage: voltage divider circuit
    value_voltage_divider = (value_voltage * 5.00) / 2.00

    # ML8511_val = ML8511_voltage * 12.49 - 14.735
    # ML8511_val = ML8511_voltage * 12.49 - 17.72
    #### voltage difference btw dark/10,000 mW/m^2: 1.2V --> 0.12
    #### subtranct 1.49916 / 0.12 - dark diff (cf. datasheet)
    ML8511_val = round((value_voltage_divider - 1) * 14.9916 / 0.12 - 18.71, 2)

    # if 2.5 <= ML8511_val <= 3.0:
    #     ML8511_val -= 0.3
    # elif ML8511_val <= 4.0:
    #     ML8511_val -= 0.6
    # elif ML8511_val <= 4.2:
    #     ML8511_val -= 0.4
    # elif 4.5 < ML8511_val:
    #     ML8511_val += 0.25

    # value['lightsense_ml8511'] = (ML8511_val, 'index')
    value['lightsense_ml8511'] = (raw_l, 'raw')

    return value
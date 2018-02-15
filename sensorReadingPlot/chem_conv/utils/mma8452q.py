# Conversion for mma8452q in Metsense

def convert(value):
    raw = []
    raw.append(value['metsense_mma8452q_acc_x'])
    raw.append(value['metsense_mma8452q_acc_y'])
    raw.append(value['metsense_mma8452q_acc_z'])

    for i in range(len(raw)):
        gcount = raw[i] >> 4
        if (raw[i] >> 8) > 0x7F:
            gcount -= 0x1000
        raw[i] = round(gcount / ((1 << 12) / 4) , 4)

    value['metsense_mma8452q_acc_x'] = (raw[0], 'gx')
    value['metsense_mma8452q_acc_y'] = (raw[1], 'gy')
    value['metsense_mma8452q_acc_z'] = (raw[2], 'gz')

    return value
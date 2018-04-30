#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  sans titre.py
#
#  Copyright 2016 belese <belese@belese-VPCEB3S1E>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
#adapted form arduino library :
#https://github.com/kerrydwong/AD770X

import spidev

REG_CMM = 0x0 #communication register 8 bit
REG_SETUP = 0x1 #setup register 8 bit
REG_CLOCK = 0x2 #clock register 8 bit
REG_DATA = 0x3 #data register 16 bit, contains conversion result
REG_TEST = 0x4 #test register 8 bit, POR 0x0
REG_NOP = 0x5 #no operation
REG_OFFSET = 0x6 #offset register 24 bit
REG_GAIN = 0x7 # gain register 24 bit

#channel selection for AD7706 (for AD7705 use the first two channel definitions)
#CH1 CH0
CHN_AIN1 = 0x0 #AIN1; calibration register pair 0
CHN_AIN2 = 0x1 #AIN2; calibration register pair 1
CHN_COMM = 0x2 #common; calibration register pair 0
CHN_AIN3 = 0x3 #AIN3; calibration register pair 2

#output update rate
#CLK FS1 FS0
UPDATE_RATE_20 = 0x0 # 20 Hz
UPDATE_RATE_25 = 0x1 # 25 Hz
UPDATE_RATE_100 = 0x2 # 100 Hz
UPDATE_RATE_200 = 0x3 # 200 Hz
UPDATE_RATE_50 = 0x4 # 50 Hz
UPDATE_RATE_60 = 0x5 # 60 Hz
UPDATE_RATE_250 = 0x6 # 250 Hz
UPDATE_RATE_500 = 0x7 # 500 Hz

#operating mode options
#MD1 MD0
MODE_NORMAL = 0x0 #normal mode
MODE_SELF_CAL = 0x1 #self-calibration
MODE_ZERO_SCALE_CAL = 0x2 #zero-scale system calibration, POR 0x1F4000, set FSYNC high before calibration, FSYNC low after calibration
MODE_FULL_SCALE_CAL = 0x3 #full-scale system calibration, POR 0x5761AB, set FSYNC high before calibration, FSYNC low after calibration

#gain setting
GAIN_1 = 0x0
GAIN_2 = 0x1
GAIN_4 = 0x2
GAIN_8 = 0x3
GAIN_16 = 0x4
GAIN_32 = 0x5
GAIN_64 = 0x6
GAIN_128 = 0x7

UNIPOLAR = 0x0
BIPOLAR = 0x1

CLK_DIV_1 = 0x1
CLK_DIV_2 = 0x2

MODE = 0b11 #SPI_CPHA | SPI_CPOL
BITS = 8
SPEED = 50000
DELAY = 10


class AD770X():
    def __init__(self, bus=0, device=0):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = SPEED
        self.spi.mode = 0b11
        self.spi.bits_per_word = BITS
        self.reset()

    def initChannel(self, channel, clkDivider=CLK_DIV_1, polarity=BIPOLAR, gain=GAIN_1, updRate=UPDATE_RATE_25):
        self.setNextOperation(REG_CLOCK, channel, 0)
        self.writeClockRegister(0, clkDivider, updRate)

        self.setNextOperation(REG_SETUP, channel, 0)
        self.writeSetupRegister(MODE_SELF_CAL, gain, polarity, 0, 0)

        while not self.dataReady(channel):
            pass

    def setNextOperation(self, reg, channel, readWrite):
        r = reg << 4 | readWrite << 3 | channel
        self.spi.xfer([r])

    '''
    Clock Register
       7      6       5        4        3        2      1      0
    ZERO(0) ZERO(0) ZERO(0) CLKDIS(0) CLKDIV(0) CLK(1) FS1(0) FS0(1)
    CLKDIS: master clock disable bit
    CLKDIV: clock divider bit
    '''
    def writeClockRegister(self, CLKDIS, CLKDIV, outputUpdateRate):
        r = CLKDIS << 4 | CLKDIV << 3 | outputUpdateRate

        r &= ~(1 << 2); # clear CLK
        self.spi.xfer([r])

    '''
    Setup Register
      7     6     5     4     3      2      1      0
    MD10) MD0(0) G2(0) G1(0) G0(0) B/U(0) BUF(0) FSYNC(1)
    '''
    def writeSetupRegister(self, operationMode, gain, unipolar, buffered, fsync):
        r = operationMode << 6 | gain << 3 | unipolar << 2 | buffered << 1 | fsync
        self.spi.xfer([r])

    def readADResult(self):
        b1 = self.spi.xfer([0x0])[0]
        b2 = self.spi.xfer([0x0])[0]

        r = int(b1 << 8 | b2)

        return r

    def readADResultRaw(self, channel):
        while not self.dataReady(channel):
            pass
        self.setNextOperation(REG_DATA, channel, 1)

        return self.readADResult()

    def readVoltage(self, channel, vref, factor=1):
        return float(self.readADResultRaw(channel)) / 65536.0 * vref * factor

    def dataReady(self, channel):
        self.setNextOperation(REG_CMM, channel, 1)
        b1 = self.spi.xfer([0x0])[0]
        return (b1 & 0x80) == 0x0

    def reset(self):
        for i in range(100):
            self.spi.xfer([0xff])


def main(args):
    import time
    ad7705 = AD770X()
    ad7705.initChannel(CHN_AIN1)
    while True:
        print(ad7705.readADResultRaw(CHN_AIN1))
        time.sleep(0.1)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
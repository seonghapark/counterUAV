import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import BoundaryNorm
sys.path.insert(0, '../raw_data/data_process')
sys.path.insert(0, './')
from wav_helper import wav_helper
from ifft_handler import ifft_handler


def main():
    h_ifft = ifft_handler()

    # constants for frame
    n = h_ifft.n  # Samples per a ramp up-time
    zpad = h_ifft.zpad

    LFM = [2400E6, 2500E6]  # Radar frequency sweep range
    MAX_DETECT = 3E8 / (2 * (LFM[1] - LFM[0])) * n / 2 # Max detection distance according to the radar frequency

    # parameter for plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    y = np.linspace(0, MAX_DETECT, int(zpad / 2))

    xlabel = plt.xlabel('Time(s)')
    ylabel = plt.ylabel('Distance(m)')
    cmap = plt.get_cmap('jet')
    norm = colors.BoundaryNorm([i for i in range(-80, 1)], ncolors=cmap.N, clip=True)

    h_wav = wav_helper(sys.argv[1])
    h_wav.read_wavs(intval=True)

    for name, sync, freq in h_wav.files():
        print('Processing IFFT from the retrieved data...')
        print('sync: ', sync)
        print('freq: ', freq)
        r_time, r_data = h_ifft.data_process(sync.astype(np.bool), freq.astype(np.int16))
        # print('freq: ', freq.astype(np.int16))

        len_time = len(r_time)

        ## constants to plot animation, initialize animate function
        ylim = plt.ylim(0, MAX_DETECT)
        
        print('r_time: ', r_time)
        print('r_data shape: ', r_data.shape)
        print('r_time: ', r_time.shape)

        # pcolormesh = plt.pcolormesh(r_time, y, r_data[:len_time], cmap=cmap, norm=norm)
        plt.pcolormesh(r_time, y, np.swapaxes(r_data[:len_time], 0, 1), cmap=cmap, norm=norm)     
        plt.suptitle(name, x=0.5, y=0.95, fontsize=10)
        colorbar = plt.colorbar()
        colorbar.set_label('Intensity (dB)')

        plt.pcolormesh(
            r_time, y, np.swapaxes(
                r_data[:len_time], 0, 1), cmap=cmap, norm=norm)
        plt.show()
       

if __name__ == '__main__':
    main()

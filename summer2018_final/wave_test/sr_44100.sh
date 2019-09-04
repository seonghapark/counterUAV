#!/bin/bash

python 1_read_data.py range_test2.wav & disown
python 2_fft.py & disown
python 5-0_draw.py & disown

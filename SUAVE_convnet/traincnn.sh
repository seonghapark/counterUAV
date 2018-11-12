#!/bin/bash -x

python3 -u run_cnn.py | tee ./log/cnn_$(date '+%Y-%m-%d_%H-%M-%S').log

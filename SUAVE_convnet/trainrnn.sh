#!/bin/bash -x

python3 -u run_rnn.py | tee ./log/rnn_$(date '+%Y-%m-%d_%H-%M-%S').log

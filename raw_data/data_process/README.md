## To read the files

Use 1_read_data.py with file name argument.
* python 1_read_data.py *FILENAME*

## To fft 

Use 2_r_analyzer.py

## To draw a plot

Use 5-0_r_draw.py

## To convert the files to wav

Use binary_converter.py.
* Must execute 1_read_data.py to read binary file.
* When converter get all binary data messages from rabbitmq, it converts data to wav file. 
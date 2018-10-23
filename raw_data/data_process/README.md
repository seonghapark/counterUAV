## To read the files

Use 1_read_data.py with file name argument.
* python 1_read_data.py *FILENAME*

## To convert the files to wav

Use binary_converter.py.
* Must execute 1_read_data.py to read binary file.
* When converter get all binary data messages from rabbitmq, it converts data to wav file. 
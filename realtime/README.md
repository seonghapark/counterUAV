### How to run the scripts:

1_read_data.py: read .txt, cut the data into the sampling rate (this must be changed to the right number, which is 11724), and send the slice of the data to 2_analyzer.py
2_analyzer.py: run fft to analyze the raw data (the data that are stored in .txt files) and send the analysis result to 3_draw.py
3_draw.py: draw result

Jul20armory_2.txt: example .txt that had collected on 7/20/2018 at armory
Jul20armory.txt: another example .txt that had collected on 7/20/2018 at armory

The three numbered scripts are connected through **rabbitmq** and they need to be executed in parallel. Rabbitmq (RMQ) is a messaging protocol that helps users to exchange data easily.
To use the RMQ, you have to install rabbitmq server on your laptop -- your laptop will be the main server, and the scripts will be clients.
More information see **https://www.rabbitmq.com/**

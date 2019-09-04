#! /usr/bin/python3

import argparse
import time

import pika
import numpy as np

EXCHANGE_NAME = 'radar'


def get_connection(url='amqp://localhost'):
    parameters = pika.URLParameters(url)

    parameters.connection_attempts = 5
    parameters.retry_delay = 5.0
    parameters.socket_timeout = 2.0
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare(
        EXCHANGE_NAME,
        exchange_type='direct',
        durable=True
    )
    return channel


def subscribe(channel):
    result = channel.queue_declare(exclusive=True)
    in_queue = result.method.queue
    channel.queue_bind(
        queue=in_queue,
        exchange=EXCHANGE_NAME,
        routing_key='raw'
    )
    return in_queue


def publish(channel, data):
    channel.publish(
        exchange=EXCHANGE_NAME,
        routing_key='ifft',
        body=data)


def dbv(input_value):
    return 20 * np.log10(abs(input_value))


def ifft(data, number_of_ifft_entities):
    data = data - data.mean(0)
    v = dbv(np.fft.ifft(data, number_of_ifft_entities, axis=0))
    s = v[0:int(v.shape[0] / 2)]
    return s - s.max()


def draw(plot):
    fig = plot.figure()
    fig.canvas.draw()


def do_process(data):
    if len(data) < 2:
        return
    if (data[0] >> 6) > 0:
        del data[:1]
    if len(data) % 2 == 1:
        del data[-1:]

    number_of_sample = int(len(data) * 20e-3)
    number_of_ifft_entities = int(8 * number_of_sample / 2)
    values = []
    sync = []
    for index in range(0, len(data), 2):
        high = data[index] & 0x1F
        low = data[index + 1] & 0x1F
        values.append(high << 5 | low)  
        sync.append(True if (data[index] >> 5) == 1 else False)

    thresh = 0
    a = np.array(sync)
    values = np.array(values)
    updown_ticks = (a > thresh)
    chunks = np.zeros([number_of_sample, int(number_of_ifft_entities / 2)], dtype=np.int16)
    chunks.fill(-80)
    index = 0
    for ii in range(0, len(updown_ticks) - number_of_sample):
        if updown_ticks[ii - 2:ii] != []:
            if (updown_ticks[ii] == True) & (updown_ticks[ii-2:ii].mean() == 0):
                chunks[index][:] = ifft(values[ii:ii+number_of_sample], number_of_ifft_entities)
                index += 1
    return chunks


def main(args):
    rabbitmq = get_connection()
    in_queue = subscribe(rabbitmq)
    try:
        while True:
            method, properties, body = rabbitmq.basic_get(queue=in_queue, no_ack=True)
            if method is not None:
                processed_data = do_process(bytearray(body))
                print(processed_data)
                publish(rabbitmq, processed_data.tostring())
            else:
                time.sleep(0.1)
    except Exception as ex:
        print(ex)
    finally:
        rabbitmq.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument('-a', '--aha', dest='', action='', help='')

    main(parser.parse_args())

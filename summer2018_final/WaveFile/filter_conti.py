#! /usr/lib/python3
import pika
import time
EXCHANGE_NAME = 'radar'


class rmq_commumication():
    def __init__(self):
        self.connection = self.get_connection()
        self.in_queue = self.subscribe(self.connection)

    def get_connection(self, url='amqp://localhost'):
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

    def subscribe(self, channel):
        result = channel.queue_declare(exclusive=True)
        in_queue = result.method.queue
        channel.queue_bind(
            queue=in_queue,
            exchange=EXCHANGE_NAME,
            routing_key='max'
        )
        return in_queue

    def publish(self, max_time, max_data, pf_data):
        max_time = np.array(max_time)
        max_data = np.array(max_data)
        pf_data = np.array(pf_data)

        data = max_time.tostring() + max_data.tostring() + pf_data.tostring()
        headers = {'max_time': len(max_time.tostring()), 'max_data': len(max_data.tostring()),
                   'particle_data': len(pf_data.tostring())}
        pika_properties = pika.BasicProperties(headers=headers)
        # pika_properties = pika.BasicProperties(content_type='application/json', headers=headers)
        self.connection.publish(
            exchange=EXCHANGE_NAME,
            properties=pika_properties,
            routing_key='particle',
            body=data)

    def get(self):
        method, properties, body = self.connection.basic_get(queue=self.in_queue, no_ack=True)

        if method is None:
            return None, None, None
        headers = properties.headers

        if len(body) != 0:
            self.max_time = np.fromstring(np.array(body[:headers['max_time']]), dtype=np.bool)
            self.result_time = np.fromstring(np.array(body[headers['max_time']:]), dtype=np.float64)
            self.max_data = self.result_time[len(self.max_time):]
            self.result_time = self.result_time[:len(self.max_time)]

            # self.max_data = np.reshape(self.max_data,
            #                            (int(len(self.max_data)), int(len(self.max_data) / len(self.max_time))))

        else:
            return None, None, None

        # print(self.max_time, self.max_data, self.result_time)

        return self.max_time, self.max_data, self.result_time

'''
Class: ParticleFilter
implements simple particle filter algorithm.
Author: Vinay
me@vany.in

'''

import numpy as np
import scipy
import scipy.stats
from numpy.random import uniform, randn
from numpy.linalg import norm

from filterpy.monte_carlo import systematic_resample


class ParticleFilter:
    def __init__(self, N, x_range, sensor_err, par_std):
        self.N = N
        self.x_range = x_range
        self.create_uniform_particles()
        self.weights = np.zeros(N)
        self.u = 0.00
        self.initial_pose = 0
        self.sensor_std_err = sensor_err
        self.particle_std = par_std

    # create particles uniformly in x range
    def create_uniform_particles(self):
        self.particles = np.empty((self.N, 1))
        self.particles[:, 0] = uniform(self.x_range[0], self.x_range[1], size=self.N)
        return self.particles

    # predict with normal distribution(randn)
    def predict(self, particles, std, u, dt=1.):
        self.N = len(particles)
        self.particles[:, 0] += u + (randn(self.N) * std)

    # update weights based on z(input)
    def update(self, particles, weights, z, R, init_var):
        self.weights.fill(1.)

        self.distance = np.linalg.norm(self.particles[:, 0:1] - init_var, axis=1)
        self.weights *= scipy.stats.norm(self.distance, R).pdf(z)

        self.weights += 1.e-300  # avoid round-off to zero
        self.weights /= sum(self.weights)  # normalize

    # returns mean and variance of the weighted particles
    def estimate(self, particles, weights):
        self.pos = self.particles[:, 0:1]
        self.mean = np.average(self.pos, weights=self.weights, axis=0)
        self.var = np.average((self.pos - self.mean) ** 2, weights=self.weights, axis=0)
        return self.mean, self.var

    def neff(self, weights):
        return 1. / np.sum(np.square(self.weights) + 1.e-300)  # handle zero round-off

    # resample particles
    def resample_from_index(self, particles, weights, indexes):
        self.particles[:] = self.particles[self.indexes]
        self.weights[:] = self.weights[self.indexes]
        self.weights /= np.sum(self.weights)

    # procedure of particle filter
    def filterdata(self, data):
        self.predict(self.particles, u=self.u, std=self.particle_std)
        self.update(self.particles, self.weights, z=data, R=self.sensor_std_err, init_var=self.initial_pose)
        if self.neff(self.weights) < self.N / 2:  # Perform systematic resampling.
            self.indexes = systematic_resample(self.weights)
            self.resample_from_index(self.particles, self.weights, self.indexes)
        mu, _ = self.estimate(self.particles, self.weights)
        return mu


if __name__ == '__main__':
    print('Connect RMQ')
    rabbitmq = rmq_commumication()
    pf = ParticleFilter(N=10000, x_range=(0, 200), sensor_err=1, par_std=1)

    ii = 0
    check = False
    last = -1

    try:
        while (True):
            max_time, max_data, result_time = rabbitmq.get()
            if max_time is None:
                time.sleep(0.2)
                continue

            # print("ParticlFilter class implementation")
            # pf_data = np.zeros(len(result_time)
            j = 0
            if len(max_data) != 0:     # 1초 단위 안에 값이 있는 경우
                pf_data = np.zeros(len(result_time))
                check = True
                for i in range(len(result_time)):   # 50번 돌면서
                    if max_time[i]:         # i번 째에 값이 있는 경우
                        pf_data[i] = pf.filterdata(data=max_data[j])
                        # pf_data.append(pf.filterdata(data=max_data[j]))
                        j += 1
                        last = pf_data[i]
                        print('1% ', last)
                    elif last != -1:              # i번 째에는 값이 없으나 그 전에 값이 있었던 경우
                        pf_data[i] = pf.filterdata(data=last)
                        # pf_data.append(pf.filterdata(data=last))
                        last = pf_data[i]
                        print('2% ', last)

            elif len(max_data) == 0 and check:     # 1초 단위에 값이없으나 그 전에 값이 있는 경우
                pf_data = np.zeros(len(result_time))
                for i in range(len(result_time)):
                    pf_data[i] = pf.filterdata(data=last)
                    # pf_data.append(pf.filterdata(data=last))
                    last = pf_data[i]
                    print('3% ', last)
            else:
                pf_data = []

            ii += 1
            print(pf_data, '\n')

            # rabbitmq.publish(max_time, max_data, pf_data)



    except(KeyboardInterrupt, Exception) as ex:
        print(ex)
    finally:
        print('Close all')
        rabbitmq.connection.close()
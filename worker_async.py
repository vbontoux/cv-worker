#!/usr/bin/env python

"""
Create multiple RabbitMQ connections from a single thread, using Pika and multiprocessing.Pool.
Based on tutorial 2 (http://www.rabbitmq.com/tutorials/tutorial-two-python.html).
"""

import multiprocessing
import time

import pika


def callback(ch, method, properties, body):
    print " [x] %r received %r" % (multiprocessing.current_process(), body,)
    time.sleep(body.count('.'))
    # print " [x] Done"
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
                   'localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_consume(callback,
                          queue='hello')

    print ' [*] Waiting for messages. To exit press CTRL+C'
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass

workers = 5
pool = multiprocessing.Pool(processes=workers)
for i in xrange(0, workers):
    pool.apply_async(consume)

# Stay alive
try:
    while True:
        continue
except KeyboardInterrupt:
    print ' [*] Exiting...'
    pool.terminate()
    pool.join()
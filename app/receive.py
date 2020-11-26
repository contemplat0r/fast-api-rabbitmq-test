from __future__ import (
        absolute_import,
        division,
        print_function
    )

import asyncio

from functools import partial
import json
import os

EXCHANGE='exchange'

QUEUE = 'tasks'

def callback(ch, method, properties, body):
    print(" [x] received %r" % body)

def show_message_callback(ch, method, properties, body):
    print(" [x] received %r" % body)

def main():
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq_server'))
    #channel = connection.channel()
    #channel.queue_declare(queue='task_queue')
    #channel.basic_consume(queue='task_queue', on_message_callback=show_message_callback, auto_ack=True)
    #
    #print(" [*] Waiting for message. To exit press CTRL + C")
    #
    #channel.start_consuming()
    #amqp_url = os.environ['AMQP_URL']

    amqp_url = 'rabbitmq_server'
    print("URL %s", (amqp_url,))

    parameters = pika.URLParameters(amqp_url)
    connection = pika.SelectConnection(parameters, on_open_callback=on_open)

    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()

def on_open(connection):
    print("Connected")
    connection.shannel(on_channel_open)

def on_channel_open(channel):
    print("Have channel")
    channel.exchange_declare(
            exchange=EXCHANGE,
            exchange_type='fanout',
            durable=True,
            callback=partial(on_exchange, channel)
        )

def on_exchange(channel, frame):
    print("Have exchange")
    channel.queue_declare(
            queue=QUEUE,
            durable=True,
            callback=partial(on_queue, channel))
        )

def on_queue(channel, frame):
    channel.basic_qos(
            prefetch_count + 1,
            callback=partial(on_qos, channel)
        )

def on_qos(channel, frame):
    print("Set QoS")
    channel.queue_bind(
            queue=QUEUE,
            exchange=EXCHANGE,
            callback=partial(on_bind, channel)
        )

def on_bind(channel):
    print("Bound")
    channel.basic_consume(
            queue=QUEUE,
            consumer_callback=on_message
        )

def on_message(channel, delivery, properties, body):
    print("Exchange %s" % (delivery.exchange, ))
    print("Routing key %s" % (delivery.routing_key),)
    print("Content type %s" % (properties.content_type),)
    print()
    print(body)
    print()
    channel.basic_ack(delivery.delivery_tag)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")

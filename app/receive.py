import pika, sys, os
import asyncio
import json

#from aio_pika import connect, IncomingMessage
import aio_pika

def callback(ch, method, properties, body):
    print(" [x] received %r" % body)

def show_message_callback(ch, method, properties, body):
    print(" [x] received %r" % body)

#async def main():
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq_server'))
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost:5672'))
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='amqp://guest:guest@localhost:5672/'))
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='amqp://guest:guest@rabbitmq_server:5672/'))
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='task_queue')


    channel.basic_consume(queue='task_queue', on_message_callback=show_message_callback, auto_ack=True)

    print(" [*] Waiting for message. To exit press CTRL + C")

    channel.start_consuming()




if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")

import asyncio

from __future__ import (
        absolute_import,
        division,
        print_function
    )

from functools import partial
import json
import os

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import List, Optional, Dict

import pika

EXCHANGE = 'exchange'

ROUTING_KEY = 'exchange.tasks'

DELAY = 5


class Task(BaseModel):
    taskid: str
    title: str
    params: Optional[Dict] = None

#class Task(BaseModel):
#    taskid: str
#    title: str
#    params: Dict[str, str] = {}


app = FastAPI()

async send_task_to_executor(task: Task):
    amqp_url = 'rabbitmq_server'
    parameters = pika.URLParameters(amqp_url)
    connection = pika.SelectConnection(parameters, on_open_callback=on_open) 

    try:
        connection.ioloop.start() 
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start() 

def on_open(connection):
    print("Connected")
    connection.channel(on_channel_open)

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
    send_message(channel, 0)

def send_message(channel, i):
    msg = "Message %d" % (i,)
    print(msg)

    channel.basic_publish(
            EXCHANGE,
            ROUTING_KEY,
            msg,
            pika.BasicProperties(content_type='text/plain', delivery_mode=2)
        )
    channel.connection.add_timeout(
            DELAY,
            partial(send_message, channel, delivery_mode=2)
        )


@app.post('/tasks/', response_model=str)
async def create_task(task: Task):
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq_server'))
    ##connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    #channel = connection.channel()
    #channel.queue_declare(queue='task_queue')
    #channel.basic_publish(exchange='', routing_key='task_queue', body=str(task))
    #connection.close()
    #return "task created"

    task_execution_result = await send_task_to_executor(task: Task)
    print("type(task_execution_result): ", type(task_execution_result))
    return str(task_execution_result)

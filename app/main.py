import asyncio
import json

import aio_pika
from aio_pika import Message

from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from typing import List, Optional, Dict

#from . import crud, models, schemas
import pika


class Task(BaseModel):
    taskid: str
    title: str
    params: Optional[Dict] = None

class Task(BaseModel):
    taskid: str
    title: str
    params: Dict[str, str] = {}


app = FastAPI()

#connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
#
#channel = connection.channel()
#
#channel.queue_declare(queue='hello')


#@app.post('/tasks/', response_model=str)
#async def create_task(task: Task):
#    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq_server'))
#    channel = connection.channel()
#    channel.queue_declare(queue='hello')
#    channel.basic_publish(exchange='', routing_key='hello', body=str(task))
#    connection.close()
#    return "task created"

async def send_task_to_executor(task_description={}):
    #connection await aio_pika.connect('amqp://guest:guest@localhost/')
    #connection = await aio_pika.connect(host='rabbitmq_server')
    #connection = await aio_pika.connect(host='amqp://guest:guest@rabbitmq_server:5672/')
    print("send_task_to_executor, task_description:\n", task_description)
    print("send_task_to_executor, type(task_description):", type(task_description))
    print("send_task_to_executor, task_description.dict():", task_description.dict())
    print("send_task_to_executor, type(task_description.dict()):", type(task_description.dict()))
    print("send_task_to_executor, json.dumps(task_description.dict()):", json.dumps(task_description.dict()))
    print("send_task_to_executor, type(json.dumps(task_description.dict())):", type(json.dumps(task_description.dict())))

    #connection = await aio_pika.connect(host='amqp://guest:guest@localhost')
    #connection = await aio_pika.connect(host='localhost')
    #connection = await aio_pika.connect(host='localhost')
    
#    async with connection:
#        routing_key = 'task_queue'
#        channel = connection.channel()
#        await channel.default_exchange.publish(
#                aio_pika.Message(body="Hello {}!".format(routing_key).encode()),
#                routing_key=routing_key
#            )

#    connection = await aio_pika.connect(host='localhost')
#    channel = await connection.channel()
#
#    #message = aio_pika.Message(body=json.dumps(task_description.dict()).encode("utf-8")),
#    message = Message(body=json.dumps(task_description.dict()).encode("utf-8")),
#
#    print("send_task_to_executor, type(message): ", type(message))
#    print("send_task_to_executor, dir(message):\n", dir(message))
#    print("send_task_to_executor, message:\n", message)
#
#    await channel.default_exchange.publish(
#        message,
#        routing_key = "task_queue"
#    )

#
#    await connection.close()

    routing_key = "task_queue"
    connection = await aio_pika.connect(host='localhost')
    channel = await connection.channel()
    await channel.default_exchange.publish(
            aio_pika.Message(body="Hello {}!".format(routing_key).encode()),
            routing_key=routing_key
        )
    await connection.close()


@app.post('/tasks/', response_model=str)
async def create_task(task: Task):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq_server'))
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue')
    channel.basic_publish(exchange='', routing_key='task_queue', body=str(task))
    connection.close()
    return "task created"

#@app.post('/tasks/', response_model=str)
#async def create_task(task: Task = Body(
#            ...,
#            example = {
#                "taskid": "task1234",
#                "title": "Example title",
#                "params": {
#                    "test1": "1234",
#                    "test2": "5678"
#                }
#            }
#        )
#    ):
#    await send_task_to_executor(task)
#
#    #return "task with id {} created".format(task['taskid'])
#    return "task with id {} created".format(task.taskid)


#async def create_task(task: Task=Body(...)):
#
#    await send_task_to_executor(task)
#
#    return "task with id {} created".format(task['taskid'])

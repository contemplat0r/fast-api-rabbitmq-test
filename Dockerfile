FROM tiangolo/uvicorn-gunicorn-fastapi:latest

RUN pip install pika aio_pika

RUN useradd web

COPY ./ /home/web

WORKDIR /home/web

RUN chown -R web:web ./

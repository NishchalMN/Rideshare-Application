print("Hello am the orchestrator")

from flask import Flask, render_template,\
jsonify,request,abort,redirect
import requests
from datetime import datetime
import docker
import pika
import json

def on_response_request(ch, method, props, body):
    print(props)
    response = {"status" : 200}
    print('---------------inside response')
    print(body)


app= Flask(__name__)

@app.route("/")
def home():
   return "came"

@app.route("/api/v1/db/write", methods=["POST"])
def write():
    print("-----------------Write Request received ")
    msg = request.get_json()
    print(msg)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rmq'))
    channel = connection.channel()
    channel.queue_declare(queue='writeQ')
    channel.basic_publish(exchange='',routing_key='writeQ',body=json.dumps(msg),properties=pika.BasicProperties(delivery_mode=2,))
    connection.close()
    print('msg sent...')
    return {'ret':200}

@app.route("/api/v1/db/read", methods=["POST","GET"])
def read():
    print("-----------------Read Request received ")
    msg = request.get_json()
    print(msg)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rmq'))
    channel = connection.channel()
    channel.queue_declare(queue='readQ')
    channel.basic_publish(exchange='',routing_key='readQ',body=json.dumps(msg),properties=pika.BasicProperties(delivery_mode=2,))

    channel.exchange_declare(exchange='Read',exchange_type='direct')
    channel.queue_declare(queue='responseQ', exclusive=False)      # because every slave can send responses to responseQ
    channel.queue_bind(exchange='Read',queue='responseQ')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='responseQ', on_message_callback=on_response_request)

    print(" [x] Awaiting write requests")
    channel.start_consuming()

    connection.close()
    print('msg sent...')
    return {'ret':200}

@app.route("/api/v1/crash/master",methods=["POST","GET"])
def killmaster():
    client=docker.from_env()
    #todo

@app.route("/api/v1/crash/slave",methods=["POST","GET"])
def killslave():
    client=docker.from_env()
    #todo

@app.route("/api/v1/worker/list",methods=["POST","GET"])
def list():
    client=docker.from_env()
    lis=client.list()
    return(jsonify(lis))


if __name__ == '__main__':
        app.run(host = "0.0.0.0", port = "80", debug=True, use_reloader = False)  #(use_reloader bcz bydefault flask runs 2 times)
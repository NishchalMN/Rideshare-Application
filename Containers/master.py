import pika
import json
import time
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rmq'))

worker = 'M'

def slave_sync(body):
    print("Slave Update")
    print(body)
    response = {"status" : 200}
    print(response)

def on_write_request(ch, method, props, body):
    print(props)
    print("Body:", body)
    response = {"status" : 200}
    print("Response:",response)

    # Implies master, so write to the sync Q and the fanout exchange
    if worker == 'M':
        newResponse = response
        responseStatus = newResponse["status"]
        print("Response status:" , responseStatus)

        if(responseStatus == 200 or responseStatus == 201):
            newBody = json.loads(body)
            print(type(newBody))
            ch.basic_publish(exchange='Slave',
                                routing_key='',
                                properties=pika.BasicProperties(
                                    delivery_mode = 2),
                                body=json.dumps(newBody)
                                )
            print("Published to syncQ")

            ch.basic_publish(exchange='',
                                routing_key='syncQ',
                                properties=pika.BasicProperties(
                                    delivery_mode = 2),
                                body=json.dumps(newBody)
                                )
            print("Published to newSlave Sync")


        # ch.basic_publish(exchange='Write',
        #                     routing_key=props.reply_to,
        #                     properties=pika.BasicProperties(correlation_id = \
        #                                                         props.correlation_id),
        #                     body=json.dumps(response))
        print("Published write")
        ch.basic_ack(delivery_tag=method.delivery_tag)


def on_read_request(ch, method, props, body):
    print(props)
    response = {"status" : 200}
    print(response)
    ch.basic_publish(exchange='Read',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=json.dumps(response))
    print("Published Read")
    ch.basic_ack(delivery_tag=method.delivery_tag)



if(worker == 'M'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rmq'))
    write_channel = connection.channel()

    write_channel.queue_declare(queue='writeQ')
    write_channel.exchange_declare(exchange='Write',exchange_type='direct')
    write_channel.queue_declare(queue='writeResponseQ', exclusive=False)
    write_channel.queue_bind(exchange='Write',queue='writeResponseQ')

    result = write_channel.exchange_declare(exchange='Slave',exchange_type='fanout')

    write_channel.queue_declare(queue='syncQ', exclusive=False)


    write_channel.basic_qos(prefetch_count=1)
    write_channel.basic_consume(queue='writeQ', on_message_callback=on_write_request)

    print(" [x] Awaiting write requests")
    write_channel.start_consuming()

elif(worker == 'S'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rmq'))

    sync_channel = connection.channel()
    read_channel = connection.channel()

    read_channel.queue_declare(queue='readQ')
    read_channel.exchange_declare(exchange='Read',exchange_type='direct')
    read_channel.queue_declare(queue='responseQ', exclusive=False)      # because every slave can send responses to responseQ
    read_channel.queue_bind(exchange='Read',queue='responseQ')

    read_channel.exchange_declare(exchange='Slave',exchange_type='fanout')
    result = read_channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    read_channel.queue_bind(exchange='Slave', queue=queue_name)

    sync_channel.queue_declare(queue='syncQ', exclusive=False)

    sync_channel.basic_qos(prefetch_count=0)
    print("Sync Starting")

    sync_q = sync_channel.queue_declare(queue='syncQ')
    while (sync_q.method.message_count != 0):
        result = sync_channel.basic_get(queue='syncQ', auto_ack=False)
        slave_sync(result[2])
        sync_q = sync_channel.queue_declare(queue='syncQ')
    print("Slave is in same level as Master")
    sync_channel.close()


    read_channel.basic_publish(exchange='',routing_key='responseQ',body=json.dumps({'ret':201}),properties=pika.BasicProperties(delivery_mode=2,))


    read_channel.basic_qos(prefetch_count=1, global_qos=False)
    read_channel.basic_consume(queue='readQ', on_message_callback=on_read_request)
    read_channel.basic_consume(queue=queue_name, on_message_callback=on_write_request, auto_ack=True)

    print(" [x] Awaiting read requests")
    read_channel.start_consuming()
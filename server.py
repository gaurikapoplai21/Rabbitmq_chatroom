import pika
import sys
import os

IP = 'localhost'
server = ''


cred = pika.PlainCredentials('admin', 'password')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=str(IP), port=5672, credentials=cred))
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')


def broadcast(body, props):
    channel.basic_publish(exchange='logs', routing_key='', properties=pika.BasicProperties(
        correlation_id=props.correlation_id), body=body)


def main():
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        print(" [x] %s" % body.decode())
        broadcast(body, properties)

    channel.basic_consume(
        queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:

        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

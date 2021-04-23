#!/usr/bin/env python
# 1 thread for each channel
import pika
import sys
import os
import threading
import time
import uuid


class Client:
    username = ''

    def __init__(self):
        self.getname()
        self.corr_id = str(uuid.uuid4())
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.daemon = True
        receive_thread.start()
        send_thread = threading.Thread(target=self.send)
        send_thread.daemon = True
        send_thread.start()

    def getname(self):
        print("Enter a username for the client")
        name = input()
        self.username = name

    def receive(self):

        connection1 = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel_receive = connection1.channel()
        result = channel_receive.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel_receive.queue_bind(exchange='logs', queue=queue_name)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            if self.corr_id != properties.correlation_id:
                print(" [x] %s" % body.decode())

        channel_receive.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel_receive.start_consuming()

    def send(self):

        connection2 = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel_send = connection2.channel()
        channel_send.queue_declare(queue='hello')
        first = self.username + " has entered the chat"
        channel_send.basic_publish(exchange='', routing_key='hello',properties=pika.BasicProperties(correlation_id=self.corr_id), body=first)
        
        while(True):

          try:
            str1 = input()
            message = '[{}] : {}'.format(self.username, str1)
            channel_send.basic_publish(exchange='', routing_key='hello', properties=pika.BasicProperties(correlation_id=self.corr_id), body=message)
        
          except:
            last = self.username + " has left the chat"
            # fix this
            channel_send.basic_publish(exchange='', routing_key='hello', properties=pika.BasicProperties(correlation_id=self.corr_id), body=last)
            break
            


if __name__ == '__main__':

    try:
        os.system('cls')
        client = Client()
        while(True):
            time.sleep(1)

    except KeyboardInterrupt:
        print(client.username + " has left the chat")
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

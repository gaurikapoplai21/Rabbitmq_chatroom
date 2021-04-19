#write a program where client send messages and server broadcasts them
#!/usr/bin/env python
#1 thread for each channel
import pika
import sys,os
import threading


'''
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')

#channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)



def main():
   while(1):
    str = input()
    
    channel.basic_publish(exchange='', routing_key='hello', body=str)
    #channel.basic_publish(exchange='logs', routing_key='', body=message)

    print(" [x] Sent ",str)

''' 


class Client:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        write_thread = threading.Thread(target=self.send)
        write_thread.start()   

    def receive(self):
        channel_receive = self.connection.channel()
        result = channel_receive.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel_receive.queue_bind(exchange='logs', queue=queue_name)
        print(' [*] Waiting for logs. To exit press CTRL+C')

        def callback(ch, method, properties, body):
            print(" [x] %r" % body)

        channel_receive.basic_consume(
           queue=queue_name, on_message_callback=callback, auto_ack=True)
        
        channel_receive.start_consuming()

    def send(self):
       channel_send = self.connection.channel()
       channel_send.queue_declare(queue='hello')
       while(True):
          str = input()
          channel_send.basic_publish(exchange='', routing_key='hello', body=str)
          print(" [x] Sent ",str)


if __name__ == '__main__':
    try:
       client = Client()

    except KeyboardInterrupt:
        client.connection.close()
        print('Interrupted')
        
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
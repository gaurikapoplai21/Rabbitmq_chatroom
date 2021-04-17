#!/usr/bin/env python
import os,sys,pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')


def main():
   while(1):
    str = input()
    
    channel.basic_publish(exchange='', routing_key='hello', body=str)
    print(" [x] Sent ",str)
   





if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        connection.close()
        print('Interrupted')
        
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
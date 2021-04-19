#write a program where client send messages and server broadcasts them
#!/usr/bin/env python
#1 thread for each channel
import pika
import sys,os
import threading





class Client:
    username = ''
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.getname() 
    
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        send_thread = threading.Thread(target=self.send)
        send_thread.start()
        
    def getname(self):
        print("Enter a username for the client")
        name = input()
        self.username = name
        
    def receive(self):
        try:
            channel_receive = self.connection.channel()
            result = channel_receive.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
            channel_receive.queue_bind(exchange='logs', queue=queue_name)
            print(' [*] Waiting for messages. To exit press CTRL+C')

            def callback(ch, method, properties, body):
                print(" [x] %s" % body.decode())

            channel_receive.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
            
            channel_receive.start_consuming()
        except KeyboardInterrupt:
            receive_thread.join()
            client.connection.close()
            


    def send(self):
        try: 
            channel_send = self.connection.channel()
            channel_send.queue_declare(queue='hello')
           
            while(True):
                try:
                    str = input()
                    message = '[{}] : {}'.format(self.username, str)

                    channel_send.basic_publish(exchange='', routing_key='hello', body=message)
                except KeyboardInterrupt:
                    break    
                  
        except KeyboardInterrupt:
            send_thread.join()
            client.connection.close()
            


if __name__ == '__main__':
    try:
       client = Client()

    except KeyboardInterrupt:
        
        print('Interrupted')
        
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
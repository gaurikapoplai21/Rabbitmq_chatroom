#!/usr/bin/env python
import pika
import sys
import os
import subprocess
from sys import platform
import socket

IP = ''
server = ''


    

if platform == "linux" or platform == "linux2":
    os.system('clear')
    cmd = "ip -4 addr | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'"
    IPoutput = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    IPs = IPoutput.split("\n")
    if len(IPs) == 1:
        IP = IPs[0]
    else:
        print("List of IPs to use for server:")
        for i in range(len(IPs)):
            print("[{}] {}".format(i+1, IPs[i]))
        choice = input("\nChoose an option [{} - {}]: ".format(1,len(IPs)))

        try:
            choice = int(choice)-1
            if choice < 0 or choice > len(IPs)-1:
                print("Invalid choice, defaulting to", IPs[0])
                IP = IPs[0]
            else:
                IP = IPs[choice]
        except:
            print("Invalid choice, defaulting to", IPs[0])
            IP = IPs[0]

    print("Server will be running at", IP)

elif platform == "darwin":
    os.system("clear")
    cmd = "ifconfig | grep -oE \"\\binet ([0-9]{1,3}\\.){3}[0-9]{1,3}\\b\" | awk '{print $2}'"
    IPoutput = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
    IPs = IPoutput.split("\n")
    if len(IPs) == 1:
        IP = IPs[0]
    else:
        print("Select IP to use for server 0 to", len(IPs)-1)
        for i in range(len(IPs)):
            print("[{}] {}".format(i, IPs[i]))
        choice = input()

        try:
            choice = int(choice)
            if choice < 0 or choice > len(IPs)-1:
                print("Invalid choice, defaulting to", IPs[0])
                IP = IPs[0]
            else:
                IP = IPs[choice]
        except:
            print("Invalid choice, defaulting to", IPs[0])
            IP = IPs[0]

    print("Server will be running at", IP)

elif platform == "win32":
    os.system('cls')
    IPs = []
    IPs.append("127.0.0.1")
    IPs.append(socket.gethostbyname(socket.gethostname()))
    print("Select IP to use for server 0 to", len(IPs)-1)
    for i in range(len(IPs)):
            print("[{}] {}".format(i, IPs[i]))
    choice = input()

    try:
            choice = int(choice)
            if choice < 0 or choice > len(IPs)-1:
                print("Invalid choice, defaulting to", IPs[0])
                IP = IPs[0]
            else:
                IP = IPs[choice]
    except:
            print("Invalid choice, defaulting to", IPs[0])
            IP = IPs[0]
    

else:
    print('Unsupported OS')
    exit(1)


connection = pika.BlockingConnection(pika.ConnectionParameters(host=str(IP)))
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

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        
        main()
    except KeyboardInterrupt:
        # fix this
        #broadcast("server connection closed.")
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

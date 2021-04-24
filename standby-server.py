#the IP should be set automatically same as the IP of the main server after choosing
#what if the standby server fails? send a msg/heartbeat to main server
#the main server should give heartbeats to standby server

#client has to start sending messages to the standby - no problem client doesn't care it sends mesg to queue
#what if the main server is back up again?


#standby failover catch up recovery : 
#request data from the time it has failed from primary server
#primary server stores data from the time standby stops giving heartbeat to the time it starts

#main server fail over - leader recovery:
#mkae follower leader

#leaderless replication - client sends message to all
#acknowledgement - so that from all servers client knows which have got


#handle rabbitmq failure

#primary server failure detection : heartbeat
#same file cli argument, primary, standby


signal = False


connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost")
channel = connection.channel()
channel.exchange_declare(exchange='logs', exchange_type='fanout')

def broadcast(body, props):
    channel.basic_publish(exchange='logs', routing_key='', properties=pika.BasicProperties(
        correlation_id=props.correlation_id), body=body)

def main():
    channel.queue_declare(queue='hello')

    def callback(ch, method, properties, body):
        if(signal):
               print(" [x] %s" % body.decode())
               broadcast(body, properties)    

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
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
# Rabbitmq_chatroom

Setup
--------

- Set the same value for erlang cookie across the all the machines in the cluster

  ``` echo "JFKZVCBYEISEQILVZMSD" | sudo tee /var/lib/rabbitmq/.erlang.cookie ```

- Connect to the main cluster

  - ``` sudo rabbitmqctl stop_app ```
  - ``` sudo rabbitmqctl join_cluster rabbit@<YOUR MAIN SERVER NAME> ```
  - ``` sudo rabbitmqctl start_app ```

- Check connection status

  - ``` sudo rabbitmqctl cluster_status ```
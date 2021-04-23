# Rabbitmq_chatroom

Setup
--------

- Add new user for rabbitmq in the server machine (server node)

  - ``` sudo rabbitmqctl add_user admin password ```
  - ``` sudo rabbitmqctl set_user_tags admin administrator ```
  - ``` sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*" ```


- Set the same value for erlang cookie across the all the machines in the cluster (all nodes)

  ``` echo "JFKZVCBYEISEQILVZMSD" | sudo tee /var/lib/rabbitmq/.erlang.cookie ```

- Connect to the main cluster (client nodes)

  - Add server nodes name and ip in /etc/hosts file
  - ``` sudo rabbitmqctl stop_app ```
  - ``` sudo rabbitmqctl join_cluster rabbit@<YOUR MAIN SERVER NAME> ```
  - ``` sudo rabbitmqctl start_app ```

- Check connection status (all nodes)

  - ``` sudo rabbitmqctl cluster_status ```
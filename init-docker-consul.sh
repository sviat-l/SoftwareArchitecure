
docker stop badger && docker rm badger

docker run -d -p 8500:8500 -p 8600:8600/udp \
          --name=badger hashicorp/consul agent \
          -server -ui -node=server-1 \
          -bootstrap-expect=1 \
          -client="0.0.0.0"

docker exec badger consul kv put hazelcast/cluster_name "dev"
docker exec badger consul kv put hazelcast/mq_name "message-queue"
docker exec badger consul kv put hazelcast/cluster_members "localhost:5701@localhost:5702@localhost:5703"

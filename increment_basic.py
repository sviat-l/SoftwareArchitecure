import hazelcast
import threading
import distributed_map

NUM_ITERATIONS = 10_000
KEY = 'key-without-locks'

def basic_increment(client_config, key, num_iter, map_name):
    client = hazelcast.HazelcastClient(**client_config)
    distrib_map = client.get_map(map_name).blocking()
    distrib_map.put_if_absent(key, 0)
    for _ in range(num_iter):
        distrib_map.put(key, distrib_map.get(key) + 1)
    client.shutdown()


if __name__ == "__main__":
      
    threads = [threading.Thread(target=basic_increment, 
                args=(distributed_map.CLIENT_CONFIG, KEY, NUM_ITERATIONS,
                            distributed_map.MAP_NAME)) for _ in range(3)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    tmp_client = hazelcast.HazelcastClient(**distributed_map.CLIENT_CONFIG)
    value = tmp_client.get_map(distributed_map.MAP_NAME).blocking().get(KEY)
    print(f"Value by key (without locks): {value}")
    tmp_client.shutdown()



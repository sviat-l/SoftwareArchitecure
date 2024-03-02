import hazelcast
NUMBER_OF_ENTRIES = 1000
MAP_NAME = "distributed-map"
CLIENT_CONFIG = { "cluster_name": "dev" }

if __name__ == "__main__":
    client = hazelcast.HazelcastClient(**CLIENT_CONFIG)
    distrib_map = client.get_map(MAP_NAME).blocking()

    for i in range(NUMBER_OF_ENTRIES):
        distrib_map.put(i, f"value: {i}")
        
    print(f"Successfully put {NUMBER_OF_ENTRIES} entries into the map {MAP_NAME}")
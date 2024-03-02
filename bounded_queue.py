import hazelcast
import threading
import time

CLIENT_CONFIG = {"cluster_name": "dev"}
QUEUE_NAME = "bounded-queue"
NUM_CONSUMERS = 2


def producer(n_min, n_max):
    client = hazelcast.HazelcastClient(**CLIENT_CONFIG)
    queue = client.get_queue(QUEUE_NAME).blocking()
    for i in range(n_min, n_max + 1):
        queue.put(i)
        print(f"Produced item: {i}")
    client.shutdown()


def consumer():
    client = hazelcast.HazelcastClient(**CLIENT_CONFIG)
    queue = client.get_queue(QUEUE_NAME).blocking()
    while True:
        item = queue.take()
        print(f"Consumer #{threading.current_thread().name} got: {item}")


if __name__ == "__main__":

    producer_thread = threading.Thread(target=producer, args=(1, 100))
    producer_thread.start()
    consumer_threads = [threading.Thread(target=consumer, args=(), name=str(i+1))
                                                    for i in range(NUM_CONSUMERS)]
    

    for consumer_thread in consumer_threads:
        consumer_thread.start()

    producer_thread.join()
    time.sleep(3)
    for consumer_thread in consumer_threads:
        consumer_thread.join()




##### Logging #####
import logging

logging.basicConfig(level=logging.INFO,
                    format='|%(asctime)s| - |%(name)s| - |%(levelname)s| - |%(message)s|')

MESSAGES_SEPARATOR = ","

##### Hazelcast Configurations #####
HAZELCAST_CLIENT_CONFIG = {
    "cluster_name": "dev",
    "cluster_members": [
        "127.0.0.1:5701",
        "127.0.0.1:5702",
        "127.0.0.1:5703"
    ]
}

### Manual ports ###
FACADE_SERVICE_PORT = 42000
MESSAGES_SERVICE_PORT = 42010
LOGGING_SERVICE_PORTS = [42020, 42021, 42022]

##### Services URLs #####
HOST_URL = "http://localhost"
FACADE_SERVICE_URL = f"{HOST_URL}:{FACADE_SERVICE_PORT}"
MESSAGES_SERVICE_URL = f"{HOST_URL}:{ MESSAGES_SERVICE_PORT}"
LOGGING_SERVICE_URLS = [f"{HOST_URL}:{port}" for port in LOGGING_SERVICE_PORTS]


#### Services Endpoints Paths ####
class ENDPOINT_PATHS:
    class logging:
        get_messages = "/messages"
        post_message = "/message"
    class messages:
        get_static_message = "/message"
    class facade:
        get_messages = "/messages"
        send_message = "/message"


##### Ports from files#####
LOGGING_SERVICE_PORTS_FILE = 'configs/ports/logging_services.txt'

def get_ports_from_file(file_path: str) -> list:
    with open(file_path, "r") as file:
        return [int(port) for port in file.read().splitlines()]

def get_logging_service_ports(file:str=LOGGING_SERVICE_PORTS_FILE) -> list:
    return get_ports_from_file(file)

#### Services URLs using ports from files ####
def get_logging_service_urls() -> list:
    return [f"{HOST_URL}:{port}" for port in get_logging_service_ports()]


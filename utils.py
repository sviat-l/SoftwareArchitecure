
##### Logging #####
import logging

logging.basicConfig(level=logging.INFO,
                    format='|%(asctime)s| - |%(name)s| - |%(levelname)s| - |%(message)s|')

def get_current_host():
    import socket
    return socket.gethostbyname(socket.gethostname())

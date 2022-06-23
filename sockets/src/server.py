import sys
import socket
import threading
import queue
import math
from loguru import logger
from request import HttpRequest, HttpResponse


class Server(object):
    hostname: str
    port: int
    serversocket: socket.socket

    concurrency_level: int | float
    task_queue: queue.Queue

    def __init__(
        self,
        hostname: str,
        port: int,
        concurrency_level: int | float = math.inf,
    ):
        self.hostname = hostname
        self.port = port
        self.concurrency_level = concurrency_level

        self.task_queue = queue.Queue()

        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.hostname, self.port))
        self.serversocket.listen(1)

        free_threads = self.concurrency_level

        while True:
            logger.info('Connection waiting...')
            clientsocket, _ = self.serversocket.accept()
            self.task_queue.put(clientsocket)
            if free_threads > 0:
                threading.Thread(target=self.handler, daemon=True).start()
                free_threads -= 1

    def handler(self):
        clientsocket = self.task_queue.get()

        sentence = clientsocket.recv(1024)

        request = HttpRequest()
        request.parse_from_text(sentence)
        logger.info(request.url)

        response = request.create_response()
        logger.info(f'Status: {response.status_code}')

        clientsocket.send(response.to_bytes())
        clientsocket.close()

        self.task_queue.task_done()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        max_threads = math.inf
    else:
        max_threads = int(sys.argv[1])

    server = Server('localhost', 12015, max_threads)
    try:
        server.start()
    except Exception as exc:
        logger.error(exc)
    finally:
        logger.info('Shotting down')

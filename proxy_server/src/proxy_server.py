from typing import Callable
import socket

from loguru import logger
import requests as r

from threadpool import ThreadPool
from config import LOG_FILE, Task, OK, BAD_REQUEST, RECV_SIZE, BLACKLIST_FILE, NOT_FOUND, Socket
from blacklist import BlackList


logger.add(LOG_FILE, level='INFO', rotation='10 MB')


class SocketProxyServer(object):
    port: int
    ip_addr: str

    def __init__(
        self,
        threadpool: ThreadPool,
        ip_addr: str = 'localhost',
        port: int = 8889,
    ):
        self.port = port
        self.ip_addr = ip_addr
        self.threadpool = threadpool

    def run(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.ip_addr, self.port))
        server_socket.listen(1)

        logger.info(f'Listening on port {self.port}')

        while True:
            try:
                client_data = server_socket.accept()
                self.threadpool.push(client_data)
            except KeyboardInterrupt:
                break

        self.threadpool.join()
        logger.info('Server stoped')


def read_socket(server_socket: Socket) -> str:
    receive_page = ''
    receive_bytes = server_socket.recv(RECV_SIZE)
    receive_page += receive_bytes.decode('CP866')

    while '\r\n\r\n' not in receive_page:
        receive_bytes = server_socket.recv(RECV_SIZE)
        receive_page += receive_bytes.decode('CP866')

    return receive_page


def blacklist_handler(blacklist: BlackList) -> Callable:
    return lambda task: handler(task, blacklist)


def handler(task: Task, blacklist: BlackList) -> None:
    client_socket, address = task
    logger.info(f'Connection to {address} is opened')

    try:
        receive_page = read_socket(client_socket)
        method = receive_page.split()[0]
        url = 'https://' + receive_page.split()[1][1:]
        logger.info(f'Request url {url}')

        body = None
        if '\r\n\r\n' in receive_page:
            body = receive_page.split('\r\n\r\n', 1)[1]

        if url in blacklist:
            logger.info(f'URL {url} in blacklist')
            client_socket.send(NOT_FOUND)
        else:
            response = r.request(method, url, data=body)
            logger.info(f'Response code {response.status_code}')
            response_content = response.content
            client_socket.send(OK(response_content.decode()))

    except Exception as exc:
        logger.error(exc)
        client_socket.send(BAD_REQUEST)

    client_socket.close()
    logger.info(b'Connection to {address} is closed')


def main(num_threads: int):
    blacklist = BlackList(BLACKLIST_FILE)
    handler_ = blacklist_handler(blacklist)
    threadpool = ThreadPool(num_threads, handler_)
    threadpool.start()

    proxy_server = SocketProxyServer(threadpool)
    proxy_server.run()


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        max_threads = 1
    else:
        max_threads = int(sys.argv[1])

    try:
        main(max_threads)
    except Exception as exc:
        logger.error(exc)
    finally:
        logger.info('Shotting down')

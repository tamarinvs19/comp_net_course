import socket
from typing import Final, Tuple


LOG_FILE: Final = 'proxy.log'
BLACKLIST_FILE: Final = 'blacklist.txt'

RECV_SIZE: Final = 4096

Socket = socket.socket
Address = str
Task = Tuple[Socket, Address]

BAD_REQUEST: Final = b'HTTP/1.1 400 Bad request\r\n\r\n'
NOT_FOUND: Final = b'HTTP/1.1 404 Not found\r\n\r\n'
OK: Final = lambda content: bytes(
    f'HTTP/1.1 200 OK\r\nContent-Length: {len(content)}\r\n\r\n{content}',
    encoding='utf-8',
)

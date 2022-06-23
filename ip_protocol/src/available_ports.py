import socket
from typing import Iterator


def port_scan(
    server_socket: socket.socket,
    target_ip: str,
    port: int,
) -> bool:
    try:
        server_socket.connect((target_ip, port))
        return True
    except:
        return False


def get_available_ports(
    ip_addr: str,
    from_: int,
    to_: int,
) -> Iterator[str]:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(from_, to_):
        if port_scan(server_socket, ip_addr, port):
            yield str(port)


if __name__ == '__main__':
    from sys import argv
    if len(argv) == 4:
        print('Available ports of {ip}:'.format(ip=argv[1]))
        print('\n'.join(
            get_available_ports(argv[1], int(argv[2]), int(argv[3])))
        )
    elif len(argv) == 2:
        print('Usage: python available_ports.py <ip-address> <from-port> <to-port>')
    else:
        print('Invalid arguments. See --help.')

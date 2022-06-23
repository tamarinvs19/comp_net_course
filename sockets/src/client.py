import socket
import sys
from request import HttpRequest, HttpResponse
from pprint import pprint


def get_file(host: str, port: int, file_name: str):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((host, port))

    try:
        request = HttpRequest(
            url=file_name,
        )
        message = request.to_bytes()
        clientsocket.sendall(message)

        data = clientsocket.recv(1024)
        response = HttpResponse()
        response.parse_from_text(data)

        if 'Content-Length' in response.fields.keys():
            while len(response.body) < int(response.fields['Content-Length']):
                data = clientsocket.recv(1024)
                response.body += data
        
        print(response.to_bytes())

    finally:
        clientsocket.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Incorrent arguments.\nUsage: python clinet.py <server_host> <server_port> <file_name>')
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        file_name = sys.argv[3]
        get_file(host, port, file_name)

import base64
import socket
import ssl
from argparse import ArgumentParser

from loguru import logger

import config as cfg


class EmailSender(object):
    sender_socket: socket.socket

    def __init__(self, host_name: str, port: int):
        mailserver = (host_name, port)
        self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sender_socket.connect(mailserver)
        recv = self.sender_socket.recv(1024)
        recv_content = recv.decode()
        logger.info(f'Message after connection request: {recv_content}.')
        if not recv_content.startswith('220'):
            raise Exception('220 reply not received from server.')

    def send_message_and_check_reply(self, message: str, code: int = -1, no_response: bool = False):
        logger.info(f'Command: {message}')
        self.sender_socket.send(message.encode())

        if no_response:
            return

        recv = self.sender_socket.recv(1024)
        recv_content = recv.decode()

        logger.info(f'Response: {recv_content}')

        if code != -1 and not recv_content.startswith(str(code)):
            raise Exception(f'{code} reply not received from server.')

    def close(self):
        self.sender_socket.close()


def read_content(content_filename: str):
    try:
        with open(content_filename, 'rt') as content_file:
            subject = content_file.readline().strip()
            content = [line[:-1] for line in content_file.readlines()]
    except FileNotFoundError:
        logger.error(f'File {content_filename} does not exists')
    except IOError:
        logger.error('Incorrect content file')
    else:
        return subject, content


def generate_file_data(filename: str):
    try:
        with open(filename, 'rb') as file:
            data = file.read()
        title = filename.split('/')[-1]
        msg = '\r\n'.join([
            '--=_frontier',
            'Content-Type: application/binary;name={title}',
            f'Content-Disposition: attachment; filename={title}',
            'Content-Transfer-Encoding: base64',
            '',
            base64.b64encode(data).decode(),
        ])
    except FileNotFoundError:
        logger.error(f'File {filename} does not exists')
    except IOError:
        logger.error('Incorrect content file')
    else:
        return msg


def send_mail(recipient: str, content_file: str, files: list[str]):
    smtp_username = cfg.SMTP_USER
    smtp_password = cfg.SMTP_PASSWORD
    username = smtp_username.split('@', maxsplit=1)[0]

    sender = EmailSender('smtp.gmail.com', 587)
    sender.send_message_and_check_reply(f'EHLO {username}\r\n', 250)
    sender.send_message_and_check_reply('STARTTLS\r\n', 220)
    sender.sender_socket = ssl.wrap_socket(sender.sender_socket)
    sender.send_message_and_check_reply(f'EHLO {username}\r\n', 250)
    sender.send_message_and_check_reply('AUTH LOGIN\r\n', 334)
    sender.send_message_and_check_reply(f'{base64.b64encode(smtp_username.encode()).decode()}\r\n', 334)
    sender.send_message_and_check_reply(f'{base64.b64encode(smtp_password.encode()).decode()}\r\n', 235)

    sender.send_message_and_check_reply(f'MAIL From: <{smtp_username}>\r\n', 250)

    sender.send_message_and_check_reply(f'RCPT To: <{recipient}>\r\n', 250)

    sender.send_message_and_check_reply('DATA\r\n', 354)

    subject, content = read_content(content_file)
    attached_files = [
        generate_file_data(filename)
        for filename in files
    ]
    letter = '\r\n'.join([
        f'From: {smtp_username}',
        f'To: {recipient}',
        f'Subject: {subject}',
        'Content-type: multipart/mixed; boundary="=_frontier"',
        '',
        '--=_frontier',
        'Content-type: text/html',
        '',
        *content,
        *attached_files,
        '--=_frontier',
        '',
    ])
    sender.send_message_and_check_reply(letter, -1, True)
    sender.send_message_and_check_reply('.\r\n', 250)

    sender.send_message_and_check_reply('QUIT\r\n')

    sender.close()
    logger.info('Sender was closed')


def _arg_parse():
    parser = ArgumentParser(
        description='Send the content file to a given email address.'
    )
    parser.add_argument(
        '-c',
        '--content',
        required=True,
        help='The file name with a content. The first line is subject. (required)',
    )
    parser.add_argument(
        '-r',
        '--recipient',
        required=True,
        help='A To: header value (required)',
    )
    parser.add_argument(
        '-f',
        '--files',
        required=False,
        action='append',
        metavar='FILE',
        default=[],
        dest='files',
        help='List of filenames for attachment.')
    return parser.parse_args()


def main():
    args = _arg_parse()
    send_mail(args.recipient, args.content, args.files)


if __name__ == '__main__':
    main()

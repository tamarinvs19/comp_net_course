from argparse import ArgumentParser
from loguru import logger

from ftp_client import FTPClient


def _arg_parse():
    parser = ArgumentParser(
        description='Simple ftp client.'
    )
    subparser = parser.add_subparsers(dest='command')

    parser_get_directory = subparser.add_parser('get_directory')
    parser_get_directory.add_argument(
        'path',
        type=str,
        default='',
        nargs='?',
        help='Directory path.'
    )

    parser_push_file = subparser.add_parser('push')
    parser_push_file.add_argument(
        'local_path',
        type=str,
        help='Local path to upload file.'
    )
    parser_push_file.add_argument(
        'server_path',
        type=str,
        default=None,
        help='Target path.'
    )

    parser_request_file = subparser.add_parser('request')
    parser_request_file.add_argument(
        'server_path',
        type=str,
        help='Local path to download file.'
    )
    parser_request_file.add_argument(
        'local_path',
        type=str,
        default=None,
        nargs='?',
        help='Target path.'
    )

    return parser.parse_args()


def main():
    args = _arg_parse()
    client = FTPClient('127.0.0.1', '21')

    if args.command == 'get_directory':
        print('\n'.join(client.get_directory_listening(args.path)))
    elif args.command == 'push':
        client.push_file(args.local_path, args.server_path)
    elif args.command == 'request':
        client.request_file(args.server_path, args.local_path)
    else:
        logger.error('Incorrect command')


if __name__ == '__main__':
    main()

import os
import ftplib
from typing import Optional
from loguru import logger

import config as cfg


class FTPClient:
    server_host: str
    server_port: str

    def __init__(self, server_host: str, server_port: str):
        self.server_host = server_host
        self.server_port = server_port

    def get_directory_listening(self, server_path: str = ''):
        logger.info('Get directory listening')
        ftp = ftplib.FTP(f'{self.server_host}', cfg.USERNAME, cfg.PASSWORD)
        directories: list[str] = []
        ftp.dir(server_path, directories.append)
        return directories

    def push_file(self, local_path: str, server_path: str):
        logger.info('Start pushing file')
        base_name = os.path.basename(server_path)
        path = os.path.dirname(server_path)
        try:
            ftp = ftplib.FTP(f'{self.server_host}', cfg.USERNAME, cfg.PASSWORD)
            ftp.cwd(path)
            ftp.storbinary(f'STOR {base_name}', open(local_path, 'rb'), 1024)
        except Exception as exc:
            logger.error(exc)
        logger.info('Push completed')

    def request_file(self, server_path: str, output_name: Optional[str] = None):
        logger.info('Start requesting file')
        base_name = os.path.basename(server_path)
        path = os.path.dirname(server_path)

        if output_name is None:
            output_name = base_name

        try:
            ftp = ftplib.FTP(f'{self.server_host}', cfg.USERNAME, cfg.PASSWORD)
            ftp.cwd(path)
            ftp.retrbinary(f'RETR {base_name}', open(output_name, 'wb').write)
            logger.info(f'File saved to {output_name}')
        except Exception as exc:
            logger.error(exc)
        logger.info('Request completed')

    def delete_file(self, server_path: str):
        logger.info('Start deleting file')
        base_name = os.path.basename(server_path)
        path = os.path.dirname(server_path)
        try:
            ftp = ftplib.FTP(f'{self.server_host}', cfg.USERNAME, cfg.PASSWORD)
            ftp.cwd(path)
            ftp.delete(base_name)
        except Exception as exc:
            logger.error(exc)
        logger.info('Delete completed')


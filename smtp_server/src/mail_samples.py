import smtplib

from argparse import ArgumentParser
from email.message import EmailMessage

from loguru import logger

import config as cfg


def smtp_send(
    recipients: list[str],
    from_address: str,
    subject: str,
    message: str,
    content_manager: str,
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
):
    try:
        for recipient in recipients:
            mail_message = EmailMessage()
            mail_message['To'] = recipient
            mail_message['From'] = from_address
            mail_message['Subject'] = subject
            if content_manager not in ['text', 'html']:
                raise ValueError(
                    f'<content_manager> can be only "text" or "html", not {content_manager}'
                )
            mail_message.set_content(message, content_manager)

            smtp_client = smtplib.SMTP_SSL(smtp_server, smtp_port)
            smtp_client.set_debuglevel(1)
            smtp_client.login(username, password)
            smtp_client.send_message(mail_message)
            smtp_client.quit()
    except smtplib.SMTPException as exc:
        logger.error(exc)


def arg_parse():
    parser = ArgumentParser(
        description='Send the content file to a given email address.'
    )
    parser.add_argument(
        '-c',
        '--content',
        required=True,
        help='The file name with html / text content. The first line is subject. (required)',
    )
    parser.add_argument(
        '-s',
        '--sender',
        required=True,
        help='The value of the From: header (required)',
    )
    parser.add_argument(
        '-r',
        '--recipient',
        required=True,
        action='append',
        metavar='RECIPIENT',
        default=[],
        dest='recipients',
        help='A To: header value (at least one required)',
    )
    return parser.parse_args()


def main():
    smtp_user = cfg.SMTP_USER
    smtp_password = cfg.SMTP_PASSWORD
    args = arg_parse()

    try:
        with open(args.content, 'rt') as content_file:
            subject = content_file.readline().strip()
            content = ''.join(content_file.readlines())
    except FileNotFoundError:
        logger.error(f'File {args.content} does not exists')
    except IOError:
        logger.error('Incorrect content file')
    else:
        smtp_send(
            recipients=args.recipients, 
            from_address=args.sender,
            subject=subject,
            message=content,
            content_manager='html',
            smtp_server='smtp.gmail.com',
            smtp_port=587, #465,
            username=smtp_user,
            password=smtp_password,
        )


if __name__ == '__main__':
    main()

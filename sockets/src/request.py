import datetime as dt
from file_reader import read_file


SP = b' '
CRLF = b'\r\n'
FSP = b': '

ENCODING = 'utf-8'



class HttpRequest(object):
    method: str
    url: str
    version: str
    fields: dict[str, str]
    body: bytes

    def __init__(
        self,
        method: str = 'GET',
        url: str = '/',
        version: str = 'HTTP/1.1',
        fields: dict[str, str] = {},
        body: bytes = b'',
    ):
        self.method = method
        self.url = url
        self.version = version
        self.fields = fields
        self.body = body

    def parse_from_text(self, text: bytes):
        rows = text.split(CRLF)
        self.method, self.url, self.version = [
            elem.decode(ENCODING) for elem in rows[0].split(SP)
        ]
        self.fields = {}
        for row in rows[1:-2]:
            field_name, value = [
                elem.decode(ENCODING) for elem in row.split(FSP)
            ]
            self.fields[field_name] = value

        self.body = rows[-1]

    def create_response(self):
        file, date = read_file(self.url)
        if file is not None:
            response = HttpResponse(
                self.version,
                '200 OK',
                {
                    'Date': dt.datetime.now().strftime(
                        '%a, %d %b %Y %H:%M:%S GMT'
                    ),
                    'Last-Modified': date.strftime(
                        '%a, %d %b %Y %H:%M:%S GMT'
                    ),
                    'Content-Length': str(len(file)),
                    'Content-Type': 'text/html',
                },
                file,
            )
        else:
            error_page = b'<html><head><title>Not Found</title></head><body><h1>Not Found</h1></body></html>'
            response = HttpResponse(
                self.version,
                '404 Not Found',
                {
                    'Date': dt.datetime.now().strftime(
                        '%a, %d %b %Y %H:%M:%S GMT'
                    ),
                    'Content-Length': str(len(error_page)),
                    'Content-Type': 'text/html',
                },
                error_page,
            )
        return response

    def to_bytes(self):
        rows: list[bytes] = []
        rows.append(
            SP.join([
                bytes(self.method, encoding=ENCODING),
                b'/' + bytes(self.url, encoding=ENCODING),
                bytes(self.version, encoding=ENCODING),
            ])
        )
        for field_name, value in self.fields.items():
            rows.append(
                FSP.join([
                    bytes(field_name, encoding=ENCODING),
                    bytes(value, encoding=ENCODING),
                ])
            )
        rows.append(b'')
        rows.append(self.body)

        return CRLF.join(rows)


class HttpResponse(object):
    version: str
    status_code: str
    fields: dict[str, str]
    body: bytes

    def __init__(
        self,
        version: str = 'HTTP/1.1',
        status_code: str = '',
        fields: dict[str, str] = {},
        body: bytes = b'',
    ):
        self.version = version
        self.status_code = status_code
        self.fields = fields
        self.body = body

    def to_bytes(self):
        rows: list[bytes] = []
        rows.append(
            SP.join([
                bytes(self.version, encoding=ENCODING),
                bytes(self.status_code, encoding=ENCODING),
            ])
        )
        for field_name, value in self.fields.items():
            rows.append(
                FSP.join([
                    bytes(field_name, encoding=ENCODING),
                    bytes(value, encoding=ENCODING),
                ])
            )
        rows.append(b'')
        rows.append(self.body)

        return CRLF.join(rows)

    def parse_from_text(self, text: bytes):
        rows = text.split(CRLF)
        self.method, self.status_code = [
            elem.decode(ENCODING) for elem in rows[0].split(SP, maxsplit=1)
        ]
        self.fields = {}
        for row in rows[1:-2]:
            field_name, value = [
                elem.decode(ENCODING) for elem in row.split(FSP)
            ]
            self.fields[field_name] = value

        self.body = rows[-1]


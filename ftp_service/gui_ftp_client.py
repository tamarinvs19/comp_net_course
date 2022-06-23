import tempfile
from typing import Callable
from functools import wraps

import tkinter as tk

from ftp_client import FTPClient


def check_client(function: Callable):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if self.client is None:
            self.create_client()
        return function(self, *args, **kwargs)
    return wrapper


def save_to_temp_file(content: str = '') -> str:
    _, path = tempfile.mkstemp()
    with open(path, 'wb') as ff:
        ff.write(content.encode())
    return path


class GUIClient:
    client: FTPClient = None
    root: tk.Tk

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry(
            '300x400'
        )

        frame1 = tk.Frame(self.root)
        frame1.pack(fill=tk.X)

        self.username_entry = tk.Entry(
            frame1,
            width=20,
        )
        self.username_entry.insert(0, 'TestUser')
        self.username_entry.pack(
            side=tk.LEFT,
            padx=5,
            pady=5,
        )

        self.password_entry = tk.Entry(
            frame1,
            width=20,
        )
        self.password_entry.insert(0, 'password')
        self.password_entry.pack(
            side=tk.RIGHT,
            padx=5,
            pady=5,
        )

        frame2 = tk.Frame(self.root)
        frame2.pack(fill=tk.X)

        self.host_entry = tk.Entry(
            frame2,
            width=20,
        )
        self.host_entry.insert(0, '127.0.0.1:21')
        self.host_entry.pack(
            side=tk.LEFT,
            padx=5,
            pady=5,
        )

        self.connect_button = tk.Button(
            frame2,
            text='Connect',
            width=16,
            command=self.connect,
        )
        self.connect_button.pack(
            side=tk.RIGHT,
            padx=5,
            pady=5,
        )

        frame3 = tk.Frame(self.root)
        frame3.pack(fill=tk.X)

        self.output_text = tk.Text(
            frame3,
            width=50,
            height=10,
        )
        self.output_text.pack(padx=5, pady=5)

        frame4 = tk.Frame(self.root)
        frame4.pack(fill=tk.X)

        self.filename_entry = tk.Entry(
            frame4,
            width=20,
        )
        self.filename_entry.pack(
            side=tk.LEFT,
            padx=5,
            pady=5,
        )

        self.create_button = tk.Button(
            frame4,
            text='Create',
            width=16,
            command=self.create,
        )
        self.create_button.pack(
            side=tk.RIGHT,
            padx=5,
            pady=5,
        )

        frame5 = tk.Frame(self.root)
        frame5.pack(fill=tk.X)

        self.retrieve_button = tk.Button(
            frame5,
            text='Retrieve',
            width=16,
            command=self.retrieve,
        )
        self.retrieve_button.pack(
            side=tk.RIGHT,
            padx=5,
            pady=5,
        )

        frame6 = tk.Frame(self.root)
        frame6.pack(fill=tk.X)

        self.update_button = tk.Button(
            frame6,
            text='Update',
            width=16,
            command=self.update,
        )
        self.update_button.pack(
            side=tk.RIGHT,
            padx=5,
            pady=5,
        )

        frame7 = tk.Frame(self.root)
        frame7.pack(fill=tk.X)

        self.delete_button = tk.Button(
            frame7,
            text='Delete',
            width=16,
            command=self.delete,
        )
        self.delete_button.pack(
            side=tk.RIGHT,
            padx=5,
            pady=5,
        )

        self.root.mainloop()

    def create_client(self):
        host, port = self.host_entry.get().split(':')
        self.client = FTPClient(host, port)

    def open_new_window(self, content: str = ''):
        new_window = tk.Toplevel(self.root)

        frame1 = tk.Frame(new_window)
        frame1.pack(fill=tk.X)

        input_text = tk.Text(
            frame1,
            width=100,
        )
        input_text.insert('1.0', content)
        input_text.pack(padx=5, pady=5)

        frame2 = tk.Frame(new_window)
        frame2.pack(fill=tk.X)

        save_button = tk.Button(
            frame2,
            text='Save',
            width=16,
            command=lambda: self.push_file(input_text.get('1.0', 'end - 1 chars')),
        )
        save_button.pack(
            side=tk.RIGHT,
            padx=5,
            pady=5,
        )

    def push_file(self, content: str):
        ff_path = save_to_temp_file(content)
        self.client.push_file(ff_path, self.filename_entry.get())

    @check_client
    def connect(self):
        directories = self.client.get_directory_listening()
        directories_text = [
            directory.split(':')[1].split(maxsplit=1)[1]
            for directory in directories
        ]
        self.output_text.delete('1.0', 'end')
        self.output_text.insert('1.0', '\n'.join(directories_text))

    @check_client
    def create(self):
        self.open_new_window()

    @check_client
    def retrieve(self):
        ff_path = save_to_temp_file()
        self.client.request_file(self.filename_entry.get(), ff_path)
        with open(ff_path, 'rb') as ff:
            content = '\n'.join(map(lambda x: x.decode(), ff.readlines()))
        self.output_text.delete('1.0', 'end')
        self.output_text.insert('1.0', content)

    @check_client
    def update(self):
        ff_path = save_to_temp_file()
        self.client.request_file(self.filename_entry.get(), ff_path)
        with open(ff_path, 'rb') as ff:
            content = '\n'.join(map(lambda x: x.decode(), ff.readlines()))
        self.open_new_window(content)

    @check_client
    def delete(self):
        self.client.delete_file(self.filename_entry.get())


if __name__ == '__main__':
    gui = GUIClient()

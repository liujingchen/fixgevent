import _multiprocessing
from _multiprocessing import Connection as OldConnection
from time import sleep

import multiprocessing.forking as forking

forking.duplicate = lambda x: 6

"""
class Connection(object):
    def __init__(self, handle, readable=True, writable=True):
        self._connection = OldConnection(handle, readable, writable)
        self.closed = self._connection.closed
        self.readable = self._connection.readable
        self.writable = self._connection.writable

    def close(self, *args, **kwargs):
        return self._connection.close(*args, **kwargs)

    def fileno(self, *args, **kwargs):
        return self._connection.fileno(*args, **kwargs)

    def poll(self, *args, **kwargs):
        return self._connection.poll(*args, **kwargs)

    def recv(self, *args, **kwargs):
        return self._connection.recv(*args, **kwargs)

    def recv_bytes(self, *args, **kwargs):
        return self._connection.recv_bytes(*args, **kwargs)

    def recv_bytes_into(self, *args, **kwargs):
        return self._connection.recv_bytes(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self._connection.send(*args, **kwargs)

    def send_bytes(self, *args, **kwargs):
        return self._connection.send_bytes(*args, **kwargs)

    def __repr__(self):
        return self._connection.__repr__()

_multiprocessing.Connection = Connection
"""

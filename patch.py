import socket


class Connection(object):
    def __init__(self, handle, readable=True, writable=True):
        self._socket = socket.fromfd(handle, socket.AF_UNIX, socket.SOCK_STREAM)
        """
        self._connection = OldConnection(handle, readable, writable)
        self.closed = self._connection.closed
        self.readable = self._connection.readable
        self.writable = self._connection.writable
        """

    def close(self, *args, **kwargs):
        return self._socket.close(*args, **kwargs)

    def fileno(self, *args, **kwargs):
        return self._socket.fileno(*args, **kwargs)

    def poll(self, *args, **kwargs):
        return self._socket.poll(*args, **kwargs)

    def recv(self, *args, **kwargs):
        return self._socket.recv(*args, **kwargs)

    def recv_bytes(self, *args, **kwargs):
        return self._socket.recv_bytes(*args, **kwargs)

    def recv_bytes_into(self, *args, **kwargs):
        return self._socket.recv_bytes(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self._socket.send(*args, **kwargs)

    def send_bytes(self, *args, **kwargs):
        return self._socket.send_bytes(*args, **kwargs)

    def __repr__(self):
        return self._socket.__repr__()


def my_patch():
    import _multiprocessing
    _multiprocessing.Connection = Connection

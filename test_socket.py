from multiprocessing import Process
from gevent.monkey import patch_socket
import os
import sys
import socket
from multiprocessing.forking import duplicate
from _multiprocessing import Connection
# import patch
from time import sleep

if len(sys.argv) > 1 and sys.argv[1] == 'break':
    patch_socket(False, False)
    pass

server_address = './uds_socket'

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise


def other_process_run():
    sock_other = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock_other.bind(server_address)
    sock_other.listen(1)
    c, address = sock_other.accept()
    print "address=" + address
    fd = duplicate(c.fileno())
    c.close()
    conn = Connection(fd)
    try:
        print conn.recv_bytes(10)
    finally:
        conn.close()
    print "other process exit"

p = Process(target=other_process_run)
p.start()

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sleep(1)
sock.connect(server_address)
fd = duplicate(sock.fileno())
conn = Connection(fd)
sock.close()
conn.send_bytes("hello")
conn.close()

p.join()
print "main process exit"

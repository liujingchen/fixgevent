# (Trying to) make gevent works with multiprocess.
Reproduce the bug of gevent's monkey_patch breaking multiprocess.
```
pip install gevent

python run.py  # without gevent monkey patch socket, will success
python run.py break  # fail due to the bug
python run.py fix  # fix the bug using the patch here, will success (using a dirty solution...)
```

# More details
## The problem
If you use gevent to monkey patch socket, then try to use the synchronization mechanism of python's multiprocessing module (the Manager),
you will get EAGAIN error "Resource temporarily unavailable".

The reason is, python's multiprocessing is using socket for the communication between processes, but it is not using the standard "socket" module in python.
Instead, it implemented a class called "Connection" using C code.
When creating the Connection object, it first creates a standard socket object using python module, then get the file descriptor and send the file descriptor
to Connection, which is C code. In the C code, it calls system API like "recv" and "send" on the handle of the file descriptor directly.

Therefore, when gevent patches socket, it can not influence the behavior of multiprocessing module's socket at all.
The gevent patched socket module will replace all the blocking socket call with nonblocking call inside a event-driven loop.
At this time, when multiprocessing creates its Connection, the standard socket it creates is a gevent-patched socket, which is nonblocking.
The file descriptor will be nonblocking too, which is send to the C code. However, all the system calls in the C code are blocking,
which leads to EAGAIN error.

The next question is, why multiprocessing Connection is not using python's socket module? The answer is in its C source code (here)[https://github.com/python/cpython/tree/2.7/Modules/_multiprocessing].
There are two implementations of Connection: socket_connection.c and pipe_connection.c. The names explain everything.
The Connection sometimes is socket, but sometimes can be a pipe. The real implementation is hidden here, so that the python part can focus on the common behavior.
This is actually a very good design, just not considering gevent use case ...

# The solution
The solutions will be, to create another patch for the Connection of multiprocessing module, which replace it with another implementation using gevent's patched socket,
which is basically rewriting everything under the "_multiprocessing" source code folder.

But before anyone implement that, we can use a dirty solution. Very simple, just replace the gevent patched modules imported in mutiprocess module with the original ones.
In this way, only multiprocessing module is unpatched, other module can still use the benefits from gevent.

# Issues left
The above dirty solution only solved "socket", but still can not patch "thread" and "sys" if you want to use mutiprocessing.
Don't know the cause yet.

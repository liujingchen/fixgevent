import sys
from gevent.monkey import patch_all
from patch import my_dirty_patch
from multiprocessing import Manager, Process
import multiprocessing.util as util
from time import sleep
from logging import StreamHandler, Formatter

logger = util.get_logger()
logger.setLevel("DEBUG")
handler = StreamHandler(sys.stdout)
_DEFAULT_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s [in %(pathname)s:%(lineno)d, ' \
                  '%(thread)d (%(threadName)s), %(process)d (%(processName)s)]'
handler.setFormatter(Formatter(_DEFAULT_FORMAT))
logger.addHandler(handler)

if len(sys.argv) > 1:
    if sys.argv[1] == 'break':
        # We first try to solve the socket problem, thread and sys will be other stories.
        patch_all(socket=True, dns=True, time=True, select=True, os=True, ssl=True, subprocess=True, aggressive=True,
                  sys=False, thread=False, Event=False)
    elif sys.argv[1] == 'fix':
        # our dirty patch can fix socket now.
        patch_all(socket=True, dns=True, time=True, select=True, os=True, ssl=True, subprocess=True, aggressive=True,
                  sys=False, thread=False, Event=False)
        my_dirty_patch()
else:
    # will not break as long as socket, thread and sys is not patched.
    patch_all(socket=False, dns=True, time=True, select=True, os=True, ssl=True, subprocess=True, aggressive=True,
              sys=False, thread=False, Event=False)


manager = Manager()
shared_dict = manager.dict()
shared_dict['count'] = 0
stop_event = manager.Event()


def other_process_run():
    while True:
        if stop_event.is_set():
            logger.info("child process exit")
            break
        count = shared_dict['count']
        shared_dict['count'] = count + 1
        sleep(1)

p = Process(target=other_process_run)
p.start()

for i in range(0, 10):
    sleep(1)
    logger.info(str(shared_dict.get('count')))

stop_event.set()
p.join()
logger.info("main process exit")

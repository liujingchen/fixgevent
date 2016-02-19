from multiprocessing import Manager, Process
import multiprocessing.util as util
from gevent.monkey import patch_all
from time import sleep
from logging import StreamHandler, Formatter
import sys
from patch import my_patch
logger = util.get_logger()
logger.setLevel("DEBUG")
handler = StreamHandler(sys.stdout)
_DEFAULT_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s [in %(pathname)s:%(lineno)d, ' \
                  '%(thread)d (%(threadName)s), %(process)d (%(processName)s)]'
handler.setFormatter(Formatter(_DEFAULT_FORMAT))
logger.addHandler(handler)

if len(sys.argv) > 1:
    if sys.argv[1] == 'break':
        patch_all()
    elif sys.argv[1] == 'fix':
        patch_all()
        my_patch()

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

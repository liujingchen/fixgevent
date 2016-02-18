from multiprocessing import Manager, Process
from gevent.monkey import patch_all
from time import sleep
import sys

if len(sys.argv) > 1 and sys.argv[1] == 'break':
    patch_all()
manager = Manager()
shared_dict = manager.dict()
shared_dict['count'] = 0
stop_event = manager.Event()


def other_process_run():
    while True:
        if stop_event.is_set():
            print "child process exit"
            break
        count = shared_dict['count']
        shared_dict['count'] = count + 1
        sleep(1)

p = Process(target=other_process_run)
p.start()

for i in range(0, 10):
    sleep(1)
    print shared_dict.get('count')

stop_event.set()
p.join()
print "main process exit"

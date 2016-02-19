import new
import sys
from gevent.monkey import saved
from inspect import getmembers
import multiprocessing.connection
import multiprocessing.managers
import multiprocessing.forking
import multiprocessing.heap
import multiprocessing.pool
import multiprocessing.process
import multiprocessing.queues
import multiprocessing.reduction
import multiprocessing.sharedctypes
import multiprocessing.synchronize
import multiprocessing.util


def my_dirty_patch():
    patched_modules = dict()
    for module_name in saved:
        patched_modules[module_name] = _duplicate_patched_module(module_name)
    # actually only unpatching multiprocessing.connection is enough to fix socket problem.
    # but we may need these sooner or later.
    for sub_module in [multiprocessing.connection, multiprocessing.managers, multiprocessing.forking,
                       multiprocessing.heap, multiprocessing.pool, multiprocessing.process, multiprocessing.queues,
                       multiprocessing.reduction, multiprocessing.sharedctypes, multiprocessing.synchronize,
                       multiprocessing.util]:
        for patched_module_name, patched_module in patched_modules.iteritems():
            if getattr(sub_module, patched_module_name, None):
                setattr(sub_module, patched_module_name, patched_module)


def _duplicate_patched_module(module_name):
    # create a new empty module, copy everything from current loaded module (already patched by gevent),
    # then copy every old thing from gevent's "saved".
    m = new.module(module_name)
    for item_name, item in getmembers(sys.modules[module_name]):
        setattr(m, item_name, item)
    for item_name, item in saved[module_name].iteritems():
        setattr(m, item_name, item)
    return m

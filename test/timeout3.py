
import gevent
from gevent import Timeout
import time

def wait():
    print('running...')
    time.sleep(10)

try:
    gevent.with_timeout(1, wait)
except Timeout:
    print('Thread 3 timed out')






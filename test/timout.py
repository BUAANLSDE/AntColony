import gevent
from gevent import Timeout

seconds = 5

timeout = Timeout(seconds)
timeout.start()

def wait():
    gevent.sleep(5)

def test():
    while True:
	    pass

try:
    # gevent.spawn(wait).join()
    gevent.joinall([
	    gevent.spawn(wait),
        gevent.spawn(test)	
    ])
except Timeout:
    print('Could not complete')
    print('continue')

print('continue2')


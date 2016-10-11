__author__ = 'PC-LiNing'

from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from multiprocessing import Manager
from ctypes import Structure, c_double

class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]

def modify(n, x, s, A,l):
    n.value += 1
    x.value **= 2
    s.value = 'a77c8df1b9302c08f12a2a31308e14003b874621f4cb3786dd'.encode()
    result = ['test','test2']
    if not l:
        print('haha')
    for one in result:
        l.append(one)

    for a in A:
        a.x **= 2
        a.y **= 2


if __name__ == '__main__':
    lock = Lock()

    n = Value('i', 7)
    x = Value(c_double, 1.0/3.0, lock=False)
    s = Array('c', 64, lock=lock)
    A = Array(Point, [(1.875,-6.25), (-5.75,2.0), (2.375,9.5)], lock=lock)
    l = Manager().list()

    p = Process(target=modify, args=(n, x, s, A,l))
    p.start()
    p.join()

    print(n.value)
    print(x.value)
    print(s.value.decode('utf-8'))
    print(l)
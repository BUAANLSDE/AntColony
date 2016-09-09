
import multiprocessing
import time


def worker():
    name = multiprocessing.current_process().name
    for i in range(0,10):
        print(name+' running worker')
        time.sleep(2)

def my_service():
        name = multiprocessing.current_process().name
        for i in range(0,20):
            print(name+' running service')
            time.sleep(3)

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 3)
    pool.apply_async(my_service)
    # target() 不同步 ；target=func 同步
    service = multiprocessing.Process(name='my_service',target=my_service)
    service.start()
    worker_1 = multiprocessing.Process(name='worker 1', target=worker())
    worker_1.start()
    worker_1.join(10)



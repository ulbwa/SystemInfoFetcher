import multiprocessing

from time import time
from json import dumps
from threading import Thread

n = 100000


def worker(number):
    j = n
    while j > 0:
        j -= 0.1
    return j


if __name__ == '__main__':
    startTime = time()
    for a in range(1000):
        worker(a)
    single_th = round(time() - startTime, 2)

    try:
        startTime = time()
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
        pool.map(worker, range(1000))
        multi_th = round(time() - startTime, 2)
    except Exception:
        startTime = time()
        threads = list()
        for a in range(1000):
            threads.append(Thread(target=worker, args=(a, )))
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        multi_th = round(time() - startTime, 2)

    print(dumps({"single_th": single_th, "multi_th": multi_th}))

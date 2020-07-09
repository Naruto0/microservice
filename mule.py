import time
from datetime import datetime

from micro.worker import process_offers


def process_every(period, fun):
    def g_tick():
        t = time.time()
        count = 0
        while True:
            count += 1
            yield max(t + count*period - time.time(), 0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        fun(datetime.utcnow())


process_every(60, process_offers)

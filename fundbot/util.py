import random
import time

def get_random_dt():
    return int(time.time()*1000 - random.randint(1, 500))

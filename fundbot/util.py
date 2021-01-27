import random
import time

def get_random_dt():
    return int(time.time()*1000 - random.randint(1, 500))

def get_timestamp_from_dt(date):
    try:
        time_array = time.strptime(date, "%Y-%m-%d")
        time_stamp = int(time.mktime(time_array)*1000 - random.randint(1, 500))
    except Exception as e:
        raise e
    return time_stamp

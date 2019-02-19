# coding: utf-8

import json
import random
import requests
import sys
from multiprocessing import Pool
import multiprocessing as multi

MAX_SDK_COUNT = 5

def send_request(x):
    url = "http://localhost:5000/req"
    payload = {"app_id": random.randint(0,255)}
    headers = {"content-type": "application/json"}
    print(requests.post(url, json.dumps(payload), headers=headers).json())

if __name__ == "__main__":
    try:
        while True:
            n_cores = multi.cpu_count()
            with Pool(n_cores) as pool:
                pool.map(send_request, range(random.randint(1, MAX_SDK_COUNT)))
    except KeyboardInterrupt:
        sys.exit(0)

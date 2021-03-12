
from concurrent import futures

import requests


i = 0
cities = ["Moscow", "Minsk", "London", "Kiev"]
def get_request_result():
    global i
    requests.get(f'http://localhost:65432/temperature?city={cities[i]}')
    i += 1
    if i == 4:
        i = 0

with futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(
            lambda: get_request_result())
        for _ in range(20)
    ]

results = [
    f.result().status_code
    for f in futures
]

print("Results: %s" % results)
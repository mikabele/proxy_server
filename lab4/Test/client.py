from concurrent import futures
import requests


with futures.ThreadPoolExecutor(max_workers=4) as executor:
    futures = [
        executor.submit(
            lambda: requests.get("http://localhost:65432/temperature?city=Minsk"))
        for _ in range(8)
    ]

results = [
    f.result().status_code
    for f in futures
]

print("Results: %s" % results)
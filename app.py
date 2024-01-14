import redis
import requests
import threading
import time
import json

FETCH_DELAY = 1


def fetch_data(r: redis.Redis):
    def _simplify_data(d: dict):
        d.pop("disabled")
        d.pop("birthdate")
        # d.pop("id") TODO: Check if that is needed data?
        sensors: list[dict] = d['trace']['sensors']
        for s in sensors:
            s.pop("id")

    url = 'http://tesla.iem.pw.edu.pl:9080/v2/monitor/2'
    i = 1
    while True:
        response = requests.get(url=url)
        data: dict = response.json()
        _simplify_data(data)

        r.set(f'measurement:{i}', json.dumps(data))
        i += 1
        time.sleep(FETCH_DELAY)
    pass


def another_thread_function_example():
    while True:
        print('Example')
        time.sleep(1)
        break


def main():
    r = redis.Redis(host='localhost', port=6379)
    fetching_thread = threading.Thread(target=fetch_data, args=[r])
    example_thread = threading.Thread(target=another_thread_function_example)

    fetching_thread.start()
    example_thread.start()

    example_thread.join()
    fetching_thread.join()


if __name__ == '__main__':
    main()

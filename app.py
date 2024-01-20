import redis
import requests
import threading
import time
import json
import pandas as pd

FETCH_DELAY = 1
NUMBER_OF_DATA_TO_FETCH = 100
NUMBER_TO_DELETE = 5


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

    while len(r.keys()) < NUMBER_OF_DATA_TO_FETCH:
        response = requests.get(url=url)
        data: dict = response.json()
        _simplify_data(data)
        # Save measurement to redis as datetime int(HourMinuteSecond) -> json
        r.set(f'{int(time.strftime('%H%M%S', time.localtime(time.time())))}', json.dumps(data))
        time.sleep(FETCH_DELAY)
        i += 1
        if len(r.keys()) + NUMBER_TO_DELETE > NUMBER_OF_DATA_TO_FETCH:
            # Flush the oldest NUMBER_TO_DELETE elements
            keys = sorted(r.keys(), key=lambda x: x)
            r.delete(*keys[:NUMBER_TO_DELETE])
        if i > 10:
            break
    pass


def get_data_from_redis(r: redis.Redis):
    """
    :param r:
    :return: pandas dataframe with data from redis
    """

    keys = sorted(r.keys(), key=lambda x: x)
    # Transform data to list of dicts
    data = [json.loads(r.get(key)) for key in keys]
    # Transform data to pandas dataframe
    data = [[sample['firstname'], sample['id'], sample['lastname'], sample['trace']['name'], sample['trace']['id']]
            + [s['anomaly'] for idx, s in enumerate(sample['trace']['sensors'])]
            + [s['value'] for idx, s in enumerate(sample['trace']['sensors'])]
            for sample in data]
    df = pd.DataFrame(data,
                      columns="firstname id lastname trace_name trace_id anL1 anL2 anL3 anR1 anR2 anR3 L1 L2 L3 R1 R2 R3".split())

    return df


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
    print(get_data_from_redis(redis.Redis(host='localhost', port=6379))[0])

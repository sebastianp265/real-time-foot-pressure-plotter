"""
ID_ID
"""
import logging

import redis
import asyncio
import requests
import json
from config import *
import datetime
import random
from functools import reduce

CACHE = None
try:
    CACHE = redis.Redis(host=HOST, port=PORT)
except redis.ConnectionError as connection_error:
    print(f"Connection error occurred:\n{connection_error}")


async def simulate_anomalies(sensors: list) -> dict:
    """
    Simulate anomalies 
    """
    bet: float = random.random()
    if bet < ANOMALIES_THRESHOLD:
        position = random.randrange(SENSOR_NUMBER)
        sensors[position]["anomaly"] = True
    return sensors


async def add(person_id: int, data: dict) -> None:
    """
    Synchronously add one entry to personId list
    """
    serialized: str = bytes(json.dumps(data, separators=(",", ":")), "utf8")
    key_base: str = f"{person_id}_"
    key_data: str = f"{key_base}data"
    key_timestamp: str = f"{key_base}timestamp"
    CACHE.rpush(key_data, serialized)
    CACHE.rpush(key_timestamp, int(datetime.datetime.now().timestamp()))


async def add_anomaly(person_id: int, data: dict) -> None:
    """
    Adds anomalies to persons anomalies list
    """
    serialized: str = bytes(json.dumps(data, separators=(",", ":")), "utf8")
    key_base: str = f"{person_id}_"
    key_data: str = f"{key_base}anomaly"
    key_timestamp: str = f"{key_base}anomaly_timestamp"
    CACHE.rpush(key_data, serialized)
    CACHE.rpush(key_timestamp, int(datetime.datetime.now().timestamp()))


async def clean_old(person_id: int) -> None:
    """
  Asynchronously and periodically remove data older than MAX_SEC
  """
    print("Cleaning old")

    key_base: str = f"{person_id}_"
    key_data: str = f"{key_base}data"
    key_timestamp: str = f"{key_base}timestamp"
    while True:
        needs_cleaning = True
        while needs_cleaning:
            sample: list = CACHE.lrange(key_timestamp, 0, 0)
            if len(sample) > 0:
                to_check: int = int(float(sample[0]))
            else:
                break
            # print("to Check{:^12}".format(to_check))
            clean: bool = to_check <= int(datetime.datetime.now().timestamp()) - MAX_SEC
            if clean:
                print("Cleaning")
                CACHE.lpop(key_data)
                CACHE.lpop(key_timestamp)
            else:
                needs_cleaning = False
            await asyncio.sleep(0)
        await asyncio.sleep(CLEAR_DELAY)


async def pull_data(person_id: int) -> None:
    """
  Asynchronously and continuously pull data from server with REQUEST_DELAY delay
  """
    while True:
        loop = asyncio.get_event_loop()
        future_response = loop.run_in_executor(
            None, requests.get, f"{BASE_URL}{person_id}"
        )
        response = await future_response
        data: dict = response.json()
        trace: dict = data["trace"]
        sensors: dict = trace["sensors"]

        sensors = await simulate_anomalies(sensors)

        anomalies = map(lambda x: x["anomaly"], sensors)
        anomalies_present = reduce(lambda x, y: x or y, anomalies)
        if anomalies_present:
            await add_anomaly(person_id, sensors)

        await add(person_id, sensors)
        await asyncio.sleep(REQUEST_DELAY)


async def main():
    print(f"execution of loop starts {IDS}")
    try:
        pullers = asyncio.gather(*(pull_data(i) for i in IDS))
        cleaner = asyncio.gather(*(clean_old(i) for i in IDS))

        all_workers = asyncio.gather(pullers, cleaner)
        await all_workers

        while True:
            await asyncio.sleep(10)
    except requests.exceptions.Timeout as timeout_error:
        print(f"Connection to api has timed out:\n{timeout_error}")
    except requests.exceptions.ConnectionError as requests_connection_error:
        print(f"There was an error connecting to api:\n{requests_connection_error}")
        # Restart the container if connection to api is lost
        raise SystemExit(1)
    except redis.ConnectionError as redis_connection_error:
        print(f"Redis Connection error occurred:\n{redis_connection_error}")


logging.basicConfig(level=logging.DEBUG)
asyncio.run(main())

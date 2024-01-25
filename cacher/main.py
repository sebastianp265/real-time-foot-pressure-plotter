import asyncio
import dataclasses
import json
import random
import time

import redis
import requests

from PatientData import PatientData
from config import *

CACHE = None
try:
    CACHE = redis.Redis(host=HOST, port=PORT)
except redis.ConnectionError as connection_error:
    print(f"Connection error occurred:\n{connection_error}")
    exit(1)


# DONE
async def simulate_anomalies(patient_data: PatientData) -> None:
    """
    Simulate anomalies 
    """
    for sensor in patient_data.sensors:
        if random.random() < FAKE_ANOMALY_PROBABILITY:
            sensor.anomaly = "True"


async def store_patient_data(patient_data: PatientData, patient_id: int) -> None:
    """
    Store patient data in redis
    """

    print("Storing data...")
    key = f"patient:{patient_id}:timestamp:{time.time()}"
    patient_data_dict = dataclasses.asdict(patient_data)
    patient_data_json: str = json.dumps(patient_data_dict)

    CACHE.set(key, patient_data_json)

    measurements_key = f"patient:{patient_id}:measurements"
    CACHE.sadd(measurements_key, key)

    CACHE.expire(key, EXPIRATION_TIME)


async def pull_data(patient_id: int) -> None:
    """
    Asynchronously and continuously pull data from server with REQUEST_DELAY delay
    """
    while True:
        print("Pulling data...")
        loop = asyncio.get_event_loop()
        future_response = loop.run_in_executor(
            None, requests.get, f"{BASE_URL}{patient_id}"
        )
        response = await future_response
        data: dict = response.json()
        sensors: list[dict] = data["trace"]["sensors"]
        patient_data: PatientData = PatientData(sensors)

        await simulate_anomalies(patient_data)

        await store_patient_data(patient_data, patient_id)

        await asyncio.sleep(REQUEST_DELAY)


async def main():
    try:
        # pullers = asyncio.gather(*(pull_data(i) for i in PPL_IDS))
        pullers = asyncio.gather(*(pull_data(i) for i in [2]))
        all_workers = asyncio.gather(pullers)
        await all_workers
    except requests.exceptions.Timeout as timeout_error:
        print(f"Connection to api has timed out:\n{timeout_error}")
        raise SystemExit(1)
    except requests.exceptions.ConnectionError as requests_connection_error:
        print(f"There was an error connecting to api:\n{requests_connection_error}")
        raise SystemExit(1)
    except redis.ConnectionError as redis_connection_error:
        print(f"Redis Connection error occurred:\n{redis_connection_error}")
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())

import os

HOST: str = os.getenv("REDIS_HOST") if os.getenv("REDIS_HOST") else "localhost"
PORT: int = 6379
BASE_URL: str = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"  # URL to endpoint with data
REQUEST_DELAY: int = 1
EXPIRATION_TIME: int = 60
PPL_IDS = range(1, 7)  # IDs of ppl to request data about
NUMBER_OF_SENSORS: int = 6
FAKE_ANOMALY_PROBABILITY: float = 0.5 # Probability of generating 'fake' anomaly

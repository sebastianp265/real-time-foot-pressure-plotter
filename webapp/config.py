HOST: str = "real-time-foot-pressure-plotter-redis-1"  # REDIS CONTAINER ADDRESS
PORT: int = 6379  # REDIS PORT
BASE_URL: str = "http://tesla.iem.pw.edu.pl:9080/v2/monitor/"  # URL to endpoint with data
IDS = range(1, 7)  # IDs of ppl to request data about
SENSORS_ID = range(6)
BASIC_INTERVAL: int = 3 * 1000  # Interval in ms
ANOMALY_INTERVAL: int = 30 * 1000  # Interval in ms
WALKING_INTERVAL: int = 15 * 1000  # Interval in ms

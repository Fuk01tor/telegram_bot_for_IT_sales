import os

import redis

REDIS_URL = os.environ['REDIS_URL']
HEROKU_REDIS_MAUVE_URL = os.environ['HEROKU_REDIS_MAUVE_URL']

Users = redis.from_url(REDIS_URL, decode_responses=True)
Monitors = redis.from_url(HEROKU_REDIS_MAUVE_URL, decode_responses=True)

import os
from dotenv import load_dotenv
import redis

load_dotenv()

ENABLE_REDIS = True

if ENABLE_REDIS:
    db = redis.Redis(
        host=os.getenv("REDIS_HOST"),
        port=int(os.getenv("REDIS_PORT")),
        db=int(os.getenv("REDIS_DB")),
        decode_responses=True,
    )

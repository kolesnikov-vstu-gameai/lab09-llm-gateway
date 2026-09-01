import hashlib
import json

import redis

from .settings import CACHE_TTL_S, REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
STATS = {"hit": 0, "miss": 0}


def key_for(npc: str, message: str, model: str) -> str:
    return "cache:" + hashlib.sha256(f"{npc}|{model}|{message.strip().lower()}".encode()).hexdigest()


def get(k: str):
    v = r.get(k)
    STATS["hit" if v else "miss"] += 1
    return json.loads(v) if v else None


def put(k: str, value: dict) -> None:
    r.setex(k, CACHE_TTL_S, json.dumps(value, ensure_ascii=False))

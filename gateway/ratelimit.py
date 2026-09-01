"""Фиксированное окно на Redis: INCR key EXPIRE 60."""

import redis
from fastapi import HTTPException

from .settings import RATE_LIMIT_PER_MIN, REDIS_URL

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)


def check(api_key: str) -> None:
    key = f"rl:{api_key}"
    n = r.incr(key)
    if n == 1:
        r.expire(key, 60)
    if n > RATE_LIMIT_PER_MIN:
        raise HTTPException(429, "rate limit exceeded")

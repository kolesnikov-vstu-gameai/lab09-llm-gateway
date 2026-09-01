import os

from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
API_KEYS = set(filter(None, os.getenv("API_KEYS", "dev-key").split(",")))
RATE_LIMIT_PER_MIN = int(os.getenv("RATE_LIMIT_PER_MIN", "30"))
CACHE_TTL_S = int(os.getenv("CACHE_TTL_S", "3600"))
CHEAP_MODEL = os.getenv("CHEAP_MODEL", "gpt-4o-mini")
STRONG_MODEL = os.getenv("STRONG_MODEL", "gpt-4o")
PROVIDER = os.getenv("LLM_PROVIDER", "openai")

import logging
import time

from fastapi import Depends, FastAPI, HTTPException
from prometheus_client import Counter, Histogram, make_asgi_app
from pydantic import BaseModel

from . import cache, llm, moderation, ratelimit, router
from .auth import require_api_key

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("gateway")
app = FastAPI(title="LLM gateway")
app.mount("/metrics", make_asgi_app())
REQS = Counter("gateway_requests_total", "requests", ["model", "cached"])
LAT = Histogram("gateway_latency_seconds", "latency")


class ChatIn(BaseModel):
    npc: str
    message: str


class ChatOut(BaseModel):
    reply: str
    model: str
    cached: bool
    latency_ms: float


@app.get("/health")
def health():
    return {"status": "ok", "cache": cache.STATS}


@app.post("/v1/chat", response_model=ChatOut)
def chat(body: ChatIn, api_key: str = Depends(require_api_key)):
    t0 = time.perf_counter()
    ratelimit.check(api_key)
    if not moderation.check_input(body.message):
        raise HTTPException(400, "message rejected by moderation")
    model = router.choose_model(body.message)
    k = cache.key_for(body.npc, body.message, model)
    hit = cache.get(k)
    if hit:
        reply, used, cached = hit["reply"], hit["model"], True
    else:
        reply, used = llm.call_with_fallback(model, body.npc, body.message)
        reply = moderation.clean_output(reply)
        cache.put(k, {"reply": reply, "model": used})
        cached = False
    with LAT.time():
        pass
    ms = (time.perf_counter() - t0) * 1000
    REQS.labels(used, str(cached)).inc()
    log.info("key=%s npc=%s model=%s cached=%s ms=%.0f", api_key, body.npc, used, cached, ms)
    return ChatOut(reply=reply, model=used, cached=cached, latency_ms=ms)

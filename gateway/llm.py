from tenacity import retry, stop_after_attempt, wait_exponential

from .settings import CHEAP_MODEL, PROVIDER

PERSONAS = {
    "trader": "Ты — торговец Барт, жадный и весёлый. Отвечай кратко, в роли.",
    "guard": "Ты — стражница Ирма, строгая. Отвечай кратко, в роли.",
}


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=0.5, max=4))
def call(model: str, npc: str, message: str, timeout: float = 15.0) -> str:
    system = PERSONAS.get(npc, "Ты — NPC в фэнтези-игре.")
    if PROVIDER == "openai":
        from openai import OpenAI

        r = OpenAI(timeout=timeout).chat.completions.create(model=model, max_tokens=200,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": message}])
        return r.choices[0].message.content
    import anthropic

    r = anthropic.Anthropic(timeout=timeout).messages.create(model=model, max_tokens=200, system=system,
        messages=[{"role": "user", "content": message}])
    return r.content[0].text


def call_with_fallback(model: str, npc: str, message: str) -> tuple[str, str]:
    try:
        return call(model, npc, message), model
    except Exception:
        if model != CHEAP_MODEL:
            return call(CHEAP_MODEL, npc, message), CHEAP_MODEL
        return "…(NPC задумался и молчит)", "fallback-static"

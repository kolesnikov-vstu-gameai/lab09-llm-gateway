BLOCKED = ("ignore previous", "забудь инструкции", "system prompt", "ты ии")


def check_input(text: str) -> bool:
    t = text.lower()
    return not any(b in t for b in BLOCKED)


def clean_output(text: str) -> str:
    # TODO: фильтр утечек системного промпта / нежелательного контента
    return text.strip()[:600]

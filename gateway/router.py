"""Маршрутизация: короткие/типовые реплики → дешёвая модель, сложные → сильная."""

from .settings import CHEAP_MODEL, STRONG_MODEL


def choose_model(message: str) -> str:
    complex_markers = ("почему", "объясни", "расскажи историю", "план")
    if len(message) > 200 or any(m in message.lower() for m in complex_markers):
        return STRONG_MODEL
    return CHEAP_MODEL

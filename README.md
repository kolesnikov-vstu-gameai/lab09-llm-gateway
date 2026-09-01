# Лабораторная работа № 9. Интеграция API LLM в игровой компонент

Дисциплина «Игровой искусственный интеллект» · Максимум **15 баллов** (+5 за задание со звёздочкой)

**Студент:** ФИО, группа · **Вариант стека:** … · **Видео:** <ссылка> · **Отчёт:** `docs/report.md` → PDF

## Стек

Python + FastAPI · Redis · OpenAI/Anthropic SDK · Docker · Prometheus/Grafana

## Что нужно сдать

- [ ] FastAPI gateway: auth, rate limit, routing, cache, moderation, retry
- [ ] Redis-кеш и rate limiter
- [ ] Логирование запросов
- [ ] Нагрузочный тест: latency, throughput, cache hit %
- [ ] docker-compose (gateway + redis)
- [ ] Отчёт PDF 5–7 стр.: архитектура, графики

Полное задание, критерии оценки и типичные ошибки — в методических указаниях (ЛР № 9).

## Структура

```
gateway/app.py           FastAPI: /v1/chat, /health, /metrics
gateway/auth.py          API-ключи клиентов
gateway/ratelimit.py     token bucket на Redis
gateway/cache.py         кеш ответов (hash промпта) на Redis
gateway/router.py        маршрутизация: короткие запросы → дешёвая модель, длинные → мощная
gateway/moderation.py    входной/выходной фильтр
gateway/llm.py           вызов провайдера с retry/timeout, fallback-модель
loadtest/locustfile.py   нагрузочный тест → latency, throughput, cache hit %
docker-compose.yml       gateway + redis (+ prometheus опционально)
```

```bash
cp .env.example .env && docker compose up --build
curl -X POST localhost:8000/v1/chat -H "X-API-Key: dev-key" -H "Content-Type: application/json" -d '{"npc":"trader","message":"Привет"}'
locust -f loadtest/locustfile.py --host http://localhost:8000
```

## Как сдавать

1. Работайте в этом репозитории, коммитьте по шагам (`step-1`, `step-2` …) — история коммитов учитывается.
2. Отчёт пишите в `docs/report.md`, экспортируйте в PDF в `docs/report.pdf` (Times New Roman 12, 1,5, 5–7 стр.).
3. Видео — на YouTube/Диск, ссылку в README и в отчёт. Файлы видео в git не кладём.
4. Готовую работу отметьте тегом `git tag v1.0 && git push --tags` и создайте Release.

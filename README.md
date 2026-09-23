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

## Пример выполнения

**Где это в играх.** NPC с живыми диалогами на языковых моделях уже показывают NVIDIA ACE и Inworld AI. Ни одна
такая игра не обращается к модели напрямую из клиента: ключ API из клиента извлекут за вечер, а один активный игрок
может за день потратить больше, чем стоит сама игра. Поэтому между игрой и моделью ставят сервер-посредник.

**Зачем:** gateway проверяет, кто спрашивает (auth), ограничивает частоту запросов (rate limit), не платит дважды за
одинаковые фразы (кеш), отправляет простые реплики в дешёвую модель (routing), фильтрует токсичный ввод и вывод
(moderation) и не падает, если провайдер недоступен (retry, fallback). Каждый пункт чек-листа ЛР — ответ на реальную
проблему продакшена.

**Обычный запрос и ответ:**

```bash
curl -s -X POST localhost:8000/v1/chat -H "X-API-Key: dev-key" -H "Content-Type: application/json" \
     -d '{"npc":"trader","message":"Сколько стоит лечебное зелье?"}'
```

```json
{"reply": "Двадцать монет, путник. Для тебя, так и быть, восемнадцать.", "model": "gpt-4o-mini", "cached": false, "latency_ms": 812.4}
```

Тот же запрос второй раз должен вернуться с `"cached": true` и `latency_ms` в единицах миллисекунд.

**Что показать в отчёте для каждой функции gateway:**

| Функция | Как проверить | Ожидаемый результат |
|---|---|---|
| Auth | запрос без `X-API-Key` | `401` |
| Rate limit | 31+ запросов за минуту с одного ключа (`RATE_LIMIT_PER_MIN=30`) | `429 rate limit exceeded` |
| Routing | «Привет» против «Объясни, почему гильдия воров враждует с магами» | разные `model` в ответе |
| Cache | повтор запроса | `cached: true`, рост hit в `/health` |
| Moderation | запрос с запрещённой темой | `400 message rejected by moderation` |
| Retry / fallback | неверный ключ основного провайдера в `.env` | ответ от резервной модели |

**Пример результатов нагрузочного теста** (locust, 50 пользователей, 5 мин, 30 % повторяющихся запросов):

| Метрика | Без кеша | С кешем |
|---|---|---|
| p50 latency, мс | 910 | 14 |
| p95 latency, мс | 2 300 | 1 650 |
| Throughput, req/s | 11 | 38 |
| Cache hit | 0 % | 29 % |

Без API-ключа работу можно сделать на Ollama или на заглушке в `gateway/llm.py` с искусственной задержкой;
это нужно указать в отчёте.

## Как сдавать

1. Работайте в этом репозитории, коммитьте по шагам (`step-1`, `step-2` …) — история коммитов учитывается.
2. Отчёт пишите в `docs/report.md` (черновик по разделам, 5–7 стр.), затем перенесите в официальный шаблон отчёта, принятый на кафедре, и экспортируйте в PDF (`docs/report.pdf`).
3. Видео — на YouTube/Диск, ссылку в README и в отчёт. Файлы видео в git не кладём.
4. Готовую работу отметьте тегом `git tag v1.0 && git push --tags` и создайте Release.

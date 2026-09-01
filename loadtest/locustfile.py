import random

from locust import HttpUser, between, task

MSGS = ["Привет", "Что продаёшь?", "Расскажи историю города", "Почему стража злая?", "Пока"]


class GameClient(HttpUser):
    wait_time = between(0.2, 1.0)

    @task
    def chat(self):
        self.client.post("/v1/chat", json={"npc": random.choice(["trader", "guard"]), "message": random.choice(MSGS)},
                         headers={"X-API-Key": "dev-key"})

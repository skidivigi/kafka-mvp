from fastapi import FastAPI
from kafka import KafkaProducer
import json
import time
import random

app = FastAPI()

producer = None

for _ in range(30):
    try:
        producer = KafkaProducer(
            bootstrap_servers="kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode(),
        )

        print("Connected to Kafka")
        break

    except Exception as e:
        print(f"Kafka not ready: {e}")
        time.sleep(2)

if producer is None:
    raise RuntimeError("Cannot connect to Kafka")


@app.post("/order")
async def create_order():

    order = {
        "order_id": random.randint(1, 999999),
        "username": "fursov"
    }

    producer.send(
        "orders",
        order
    )

    producer.flush()

    return order
import psycopg
import json
import os
import time
from kafka import KafkaConsumer

time.sleep(20)

consumer_name = os.getenv("HOSTNAME", "unknown-consumer")

print(f"CONSUMER STARTED: {consumer_name}", flush=True)

consumer = KafkaConsumer(
    "orders",
    bootstrap_servers="kafka:9092",
    group_id="workers",
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode()),
)

print("CONNECTED TO KAFKA", flush=True)

conn = psycopg.connect(
    host="postgres",
    dbname="demo",
    user="demo",
    password="demo",
)

print("CONNECTED TO POSTGRES", flush=True)

cur = conn.cursor()

print("WAITING FOR MESSAGES", flush=True)

for msg in consumer:
    print(
        f"consumer={consumer_name} "
        f"partition={msg.partition} "
        f"offset={msg.offset} "
        f"value={msg.value}",
        flush=True,
    )

    cur.execute(
        """
        INSERT INTO orders(
            order_id,
            username,
            consumer_name,
            kafka_partition,
            kafka_offset
        )
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            msg.value["order_id"],
            msg.value["username"],
            consumer_name,
            msg.partition,
            msg.offset,
        ),
    )

    conn.commit()
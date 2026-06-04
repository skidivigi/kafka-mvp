#!/bin/bash
set -e

sleep 20

if /opt/kafka/bin/kafka-topics.sh \
    --bootstrap-server kafka:9092 \
    --describe \
    --topic orders >/dev/null 2>&1
then
    echo "Topic exists"

    /opt/kafka/bin/kafka-topics.sh \
      --bootstrap-server kafka:9092 \
      --alter \
      --topic orders \
      --partitions 3 || true
else
    echo "Creating topic"

    /opt/kafka/bin/kafka-topics.sh \
      --bootstrap-server kafka:9092 \
      --create \
      --topic orders \
      --partitions 3 \
      --replication-factor 1
fi
# Kafka MVP

Небольшой проект для изучения основных концепций Apache Kafka.

## Что делает MVP

```text
FastAPI Producer
        |
        v
      Kafka
        |
        v
 Consumer Group (N consumers)
        |
        v
    PostgreSQL
```

1. Producer принимает HTTP-запросы и публикует сообщения в Kafka Topic `orders`.
2. Kafka хранит сообщения и распределяет их по Partition.
3. Consumer Group читает сообщения из Kafka.
4. Consumers сохраняют обработанные сообщения в PostgreSQL.
5. Для каждой записи сохраняются:

   * consumer_name
   * kafka_partition
   * kafka_offset

Это позволяет наглядно увидеть распределение нагрузки между consumers.

## Изучаемые концепции

* Producer
* Consumer
* Topic
* Partition
* Consumer Group
* Offset
* Lag
* Rebalance
* Scaling Consumers
* Replication (теоретически)

## Полезные эксперименты

### Масштабирование consumers

```bash
docker compose up -d --scale consumer=3
```

### Генерация сообщений

```bash
make test-more
```

### Проверка распределения

```sql
SELECT
    consumer_name,
    kafka_partition,
    count(*)
FROM orders
GROUP BY consumer_name, kafka_partition;
```

## Основной вывод

В Kafka масштабируется не количество consumers, а количество partition.

```text
1 partition  -> максимум 1 активный consumer
3 partitions -> максимум 3 активных consumer
10 partitions -> максимум 10 активных consumer
```

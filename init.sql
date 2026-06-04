CREATE TABLE orders
(
    id serial primary key,
    order_id integer,
    username text,
    consumer_name text,
    kafka_partition integer,
    kafka_offset bigint,
    created_at timestamp default now()
);
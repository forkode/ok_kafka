# Ok Kafka

Ok Kafka is a Kafka queue wrapper that implements some additional logic, like
default serialization/deserialization, minimal topic description or some
standardized metadata.

## start kafka for testing
`docker run -p 2181:2181 -p 9092:9092 —env ADVERTISED_HOST=127.0.0.1 —env ADVERTISED_PORT=9092 spotify/kafka`

## environment variables
should be specified or you can provice the values directly to Producer and subscribe
```
KAFKA_URL - kafka location, for local development most probably localhost:9092
KAFKA_GROUP - kafka group, group of workers that do the same task
```

## how to use producer
```python
from ok_kafka import Producer

producer = Producer('my_fancy_service')
producer.some_topic(some='some', topic='topic', params='params')
```

## how to subscribe
```python
from ok_kafka import subscribe

@subscribe('application.business_process.particular_action')
def my_handler(message, message_meta):
    ...
```

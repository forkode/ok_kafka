# Ok Kafka

Ok Kafka is a Kafka queue wrapper that implements some additional logic, like
default serialization/deserialization, minimal topic description or some
standardized metadata.

## Start kafka for testing
`docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST='127.0.0.1' --env ADVERTISED_PORT=9092 spotify/kafka`

## Environment variables
Should be specified or you can provide the values directly to your 'Producer' and '@subscribe'
```
KAFKA_URL - kafka location, for local development most probably localhost:9092
KAFKA_GROUP - kafka group, group of workers that do the same task
```

## How to use producer
First you need to create a yaml file with topic schemas like so:
```yaml
my.fancy.topic1:  # inside should be json-schema
  type: object
  properties:
    int_property:
      type: integer
    decimal_property:
      type: number
    string_property:
      type: string
    datetime_property:
      type: string
      format: date-time
my.fancy.topic2:
  ...
```

then generate a producer
```sh
cat/curl my_topics.yaml | python3 -m ok_kafka.start > ./clients/kafka_producer.py
```

then use it
```python
from clients.kafka_producer import Producer

producer = Producer('my_fancy_service')
producer.some_topic(some='some', topic='topic', params='params')
```

## How to subscribe
```python
from ok_kafka import subscribe

@subscribe('application.business_process.particular_action')
def my_handler(message, message_meta):
    ...
```

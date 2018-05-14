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
first you need to create yaml file with topic schemas like this:
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

then generate producer
```sh
cat/curl my_topics | python3 -m ok_kafka.start > ./clients/kafka_producer
```

then just use it
```python
from clients.kafka_producer import Producer

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

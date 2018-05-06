"""Message producer.

usage:
   producer = Producer('my_fancy_service', kafka_url='localhost:9092')
   producer.some_topic(some='some', topic='topic', params='params')
"""
import os

from kafka import KafkaProducer

from ok_kafka import default_serializer
from ok_kafka.local_types import SerializerType, JSONType, MessageType
from ok_kafka.meta_tools import make_meta

KAFKA_URL = os.environ.get('KAFKA_URL')

__all__ = ['Producer']


class Producer:
    def __init__(
        self,
        issuer,  # type: str
        kafka_url=KAFKA_URL,  # type: str
        serialize=default_serializer.serialize,  # type: SerializerType
    ):
        # type: (...) -> None
        """Init.

        :param issuer: service that issued the message.
        :param kafka_url: to connect to kafka, something like '127.0.0.1:9092'
        :param serialize: serializer function
        """
        self.issuer = issuer
        self.serialize = serialize
        if not kafka_url:
            raise ValueError('Please specify "kafka_url" parameter')
        self.kafka_producer = KafkaProducer(bootstrap_servers=kafka_url)

    def _produce(self, topic, message):  # type: (str, MessageType) -> None
        serialized = self.serialize(message)  # type: bytes
        self.kafka_producer.send(topic, serialized)

    def test_topic(
        self,
        test,  # type: str
        _meta=None,  # type: JSONType
    ):
        # type: (...) -> None
        """Test topic.

        :param test: some test parameter
        :param _meta: nonstandard meta
        """
        if not _meta:
            _meta = make_meta(issuer=self.issuer)
        self._produce(
            'test_topic',
            {
                '_meta': _meta,
                'test': test,
            }
        )

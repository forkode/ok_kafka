"""Subscribe decorator to subscribe handler to particular topic.

usage:
    @subscribe('my.fancy.topic')  # url and group configured in environment
    def my_handler(message, message_meta):
        ...

    @subscribe(
        topic='application.business_process.partucular_action',
        group=my_custom_settings.KAFKA_GROUP,
        kafka_url=my_custom_settings.KAFKA_URL
    )
    def my_handler(message, message_meta):
        ...

    @subscribe(  # batch process a number of messages
        'my.fancy.topic',
        max_records=1000,
        timeout=5000,  # milliseconds
    )
    def my_mandler(pairs):
        for message, message_meta in pairs:
        ...

Note that "message" is a json (JSONType) with "Decimal"-s instead of floats
and message_meta is MessageMeta nametuple.
"""
import os
from types import MappingProxyType as FrozenDict
from typing import Callable, Dict, List, Optional, Tuple, Union

from kafka import KafkaConsumer, TopicPartition
from kafka.consumer.fetcher import ConsumerRecord

from ok_kafka import default_serializer
from ok_kafka import meta_tools
from ok_kafka.local_types import DecoratorType, DeserializerType, MessageType
from ok_kafka.meta_tools import get_message_and_meta, MessageMeta

KAFKA_URL = os.environ.get('KAFKA_URL')
KAFKA_GROUP = os.environ.get('KAFKA_GROUP')

__all__ = ['HandlerType', 'PollHandlerType', 'subscribe']


HandlerType = Callable[[MessageType, MessageMeta], None]
PollHandlerType = Callable[
    [
        List[Tuple[MessageType, MessageMeta]],
    ],
    None,
]


def subscribe(
    topic,  # type: str
    group=KAFKA_GROUP,  # type: Optional[str]
    kafka_url=KAFKA_URL,  # type: Optional[str]

    deserialize=default_serializer.deserialize,  # type: DeserializerType
    max_records=None,  # type: Optional[int]
    timeout=300000,  # type: Optional[int]  # milliseconds

    start_from_latest=True,  # type: bool
    commit=True,  # type: bool
    use_track_magic=True,  # type: bool
    options=FrozenDict({}),  # type: dict
):  # type: (...) -> DecoratorType
    """Subscribe handler function to some topic.

    :param topic: tipic to subscribe
    :param group: group name, each message is given only to 1 member of a group
    :param kafka_url: to connect to kafka, something like '127.0.0.1:9092'
    :param deserialize: function that deserialize raw 'bytes' message
    :param max_records: if specified handler receives this num of messages
      (or less if couln't collect that many in timeout)
    :param timeout: when max_records is given, timeout to collect records
    :param start_from_latest: for new consumer or on offset error.
      if true, consumer will receive messages pushed after first connection
      if false? consumer will receive all existing messages in a queue
    :param commit: commit after receiving messages
    :param use_track_magic: try to preserve track in message chain
    :param options: extra params to consumer, not considered as a stable api
    """

    if not group:
        raise ValueError('Please specify kafka "group" parameter')
    if not kafka_url:
        raise ValueError('Please specify "kafka_url" parameter')

    def decorator(
        handler,  # type: Union[PollHandlerType, HandlerType]
    ):
        # type: (...) -> Union[PollHandlerType, HandlerType]
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=kafka_url,
            group_id=group,
            auto_offset_reset='latest' if start_from_latest else 'earliest',
            **options
        )

        handler._consumer = consumer

        if max_records:
            while True:
                partition_records = consumer.poll(
                    timeout_ms=timeout, max_records=max_records,
                )  # type: Dict[TopicPartition, List[ConsumerRecord]]

                meta_tools.nonthreadsafe_track = None

                handler([
                   get_message_and_meta(record, deserialize, topic)
                   for records in partition_records.values()
                   for record in records
                ])

                if commit:
                    consumer.commit()

        else:
            for record in consumer:  # type: ConsumerRecord
                message, meta = get_message_and_meta(record, deserialize, topic)
                if use_track_magic:
                    meta_tools.nonthreadsafe_track = meta.track

                handler(message, meta)

                if commit:
                    consumer.commit()

        return handler
    return decorator

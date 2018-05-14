import os
import socket
from datetime import datetime
from typing import Optional, NamedTuple, Tuple
from uuid import uuid4

from kafka.consumer.fetcher import ConsumerRecord

from ok_kafka.local_types import DeserializerType, JSONType, MessageType

__all__ = [
    'MessageMeta', 'nonthreadsafe_track', 'make_meta', 'get_message_and_meta'
]

# used in the track magic: producer when called from handler implicitly passes
# track from the message that is being handled to the newly produced messages
nonthreadsafe_track = None

MessageMeta = NamedTuple('MessageMeta', [
    ('info', str),  # for humans not robots, log, save, but don't parse
    ('created_at', datetime),
    ('track', str),
    ('ver', str),
    ('issuer', str),
    ('process', JSONType),
])


def make_meta(
    track=None,  # type: Optional[str]
    ver='1',  # type: str
    issuer=None,  # type: Optional[str]
    process=None,  # type: JSONType
):
    # type: (...) -> JSONType
    """Create message metadata.

    :param track: ideally should be the same in all message chain
    :param ver: topic schema version
    :param issuer: name of the service that produced the message
    :param process: data to locate which process issued message
    """
    if not track:
        track = nonthreadsafe_track or str(uuid4())
    if not process:
        process = {
            'host': socket.gethostname(),
            'pid': os.getpid(),
        }

    return {
        'track': track,
        'ver': ver,
        'issuer': issuer,
        'process': process,
    }


def get_message_and_meta(
    record,  # type: ConsumerRecord
    deserialize,  # type: DeserializerType
    topic,  # type: str
):
    # type: (...) -> Tuple[MessageType, MessageMeta]
    """Helper method to deserialize data and create meta"""
    message = deserialize(record.value, topic)
    meta = message.pop('_meta', {})
    created_at = datetime.fromtimestamp(record.timestamp / 1000)

    message_meta = MessageMeta(
        info=f'kafka:{record.topic}:{record.partition}:{record.offset}',
        created_at=created_at,
        track=meta.get('track'),
        ver=meta.get('ver', '1'),
        issuer=meta.get('issuer'),
        process=meta.get('process'),
    )
    return message, message_meta

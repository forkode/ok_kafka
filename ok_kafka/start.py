import sys

from jinja2 import Template
import yaml


template = Template("""
{%- macro render_type_string(property) %}
{%- if not property.format -%}
    str
{%- elif property.format == 'date' -%}
    date
{%- elif property.format == 'date-time' -%}
    datetime
{%- endif %}
{%- endmacro %}


{%- macro render_type(property)  %}
{%- if property.type == 'boolean' -%}
    bool
{%- elif property.type == 'integer' -%}
    int
{%- elif property.type == 'number' -%}
    Decimal
{%- elif property.type == 'string' -%}
    {{ render_type_string(property) }}
{%- elif property.type == 'array' -%}
    list
{%- elif property.type == 'object' -%}
    dict
{%- else -%}
    Any
{%- endif %}
{%- endmacro -%}


# pylint: skip-file
\"\"\"Message producer.

usage:
   producer = Producer('my_fancy_service', kafka_url='localhost:9092')
   producer.some_topic(some='some', topic='topic', params='params')
\"\"\"
import os

from kafka import KafkaProducer

from ok_kafka import default_serializer
from ok_kafka.local_types import SerializerType, JSONType, MessageType
from ok_kafka.meta_tools import make_meta

MYPY = False
if MYPY:
    from datetime import datetime, date
    from decimal import Decimal

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
        \"\"\"Init.

        :param issuer: service that issued the message.
        :param kafka_url: to connect to kafka, something like '127.0.0.1:9092'
        :param serialize: serializer function
        \"\"\"
        self.issuer = issuer
        self.serialize = serialize
        if not kafka_url:
            raise ValueError('Please specify "kafka_url" parameter')
        self.kafka_producer = KafkaProducer(bootstrap_servers=kafka_url)

    def _produce(self, topic, message):  # type: (str, MessageType) -> None
        serialized = self.serialize(message)  # type: bytes
        self.kafka_producer.send(topic, serialized)

    {%- for topic, message in schema.items() %}

    def {{ topic.replace('.', '_') }}(
        self,
        {%- for property_name, property in message.properties.items() %}
        {{ property_name }},  # type: {{ render_type(property) }}
        {%- endfor  %}
        _meta=None,  # type: JSONType
    ):
        # type: (...) -> None
        \"\"\"{{ message.description }}

        {%- for property_name, property in message.properties.items() if property.description %}
        :param {{ property_name }}: {{ property.description }}
        {%- endfor  %}
        \"\"\"
        if not _meta:
            _meta = make_meta(issuer=self.issuer)
        self._produce(
            '{{ topic }}',
            {
                '_meta': _meta,
                {%- for property_name, property in message.properties.items() %}
                '{{ property_name }}': {{ property_name }},
                {%- endfor  %}
            }
        )
    {%- endfor %}
""")

print(
    template.render(
        schema=yaml.load(
            sys.stdin.read()
        )
    )
)

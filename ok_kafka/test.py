from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

from ok_kafka import subscribe
from ok_kafka.meta_tools import MessageMeta


def test_subscribe():
    mock_handler = Mock()
    mock_consumer = MagicMock()
    mock_consumer.return_value.__iter__.return_value = [Mock(
        value=b'{"test": true}', timestamp=1000000000000,
        topic='my.fancy.topic', partition=1, offset=2,
    )]

    with patch('ok_kafka.consume.KafkaConsumer', mock_consumer):
        subscribe(
            'my.fancy.topic', group='test_group', kafka_url='test_url',
        )(mock_handler)

    mock_consumer.assert_called_once_with(
        'my.fancy.topic', auto_offset_reset='latest',
        bootstrap_servers='test_url', group_id='test_group'
    )
    mock_handler.assert_called_once_with(
        {'test': True},
        MessageMeta(
            info='kafka:my.fancy.topic:1:2',
            created_at=datetime(2001, 9, 9, 5, 46, 40), track=None, ver='1',
            issuer=None, process=None,
        ))
    mock_consumer.return_value.commit.assert_called_once()

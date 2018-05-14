import json
from datetime import date, datetime
from decimal import Decimal

from ok_kafka.local_types import JSONType

__all__ = ['serialize', 'deserialize']


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        # type(Any) -> Union[None, bool, int, float, str, list, dict]
        if isinstance(o, Decimal):
            return float(o)
        if isinstance(o, date):
            return o.isoformat()
        if isinstance(o, datetime):
            return o.isoformat()
        return super(DecimalEncoder, self).default(o)


def serialize(value):  # type: (JSONType) -> bytes
    return json.dumps(value, cls=DecimalEncoder).encode('UTF8')


def deserialize(value, topic):  # type: (bytes) -> JSONType
    return json.loads(value, parse_float=Decimal)

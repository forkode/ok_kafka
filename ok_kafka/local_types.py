from decimal import Decimal
from typing import Callable, Dict, List, TypeVar, Union

__all__ = [
    'DecoratorType', 'DeserializerType', 'JSONType', 'MessageType',
    'SerializerType',
]

MessageType = TypeVar('MessageType')
DeserializerType = Callable[[bytes], MessageType]
SerializerType = Callable[[MessageType], bytes]

DecoratorType = Callable[[Callable], Callable]
JSONType = Union[
    None,
    bool,
    int,
    Decimal,
    str,
    List['JSONType'],
    Dict[str, 'JSONType'],
]

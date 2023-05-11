#!/usr/bin/env python3
"""Implementation of the `Cache` Class.
The Class Leverages Redis to Implement Different
Caching Functions and Methods"""


import redis
import uuid
from typing import Union, Callable, Optional, Any, TypeVar
from functools import wraps

T = TypeVar('T')


def count_calls(func: Callable) -> Callable:
    """A Decorator that Counts Number of Times a Method is called."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = func.__qualname__
        self.redis.incr(key)
        return func(*args, **kwargs)

    return wrapper


class Cache:
    """Class to Hold Implementation of Different Caching functions"""

    def __init__(self):
        """Initialization Method for the `Cache` Class"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Type Annotated Method to take `data` arg
        That generates random key, store input data in Redis using
        the Generated Key, and returns the key."""

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], T]] = None
            ) -> Optional[T]:
        """take a `key` string argument and an
        optional Callable argument named `fn`.
        This callable will be used to convert
        the data back to the desired format."""

        data = self._redis.get(key)
        if data is None:
            return None

        if fn and callable(fn):
            return fn(data)

        return data

    def get_str(self, key: str) -> str:
        """Gets the Random Key as Input,
        Retrives data and returns the data as a `str`"""

        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """Given Random Key as Input,
        Retrieves Cached data from Redit and returns as `int`"""

        return self.get(key, fn=int)

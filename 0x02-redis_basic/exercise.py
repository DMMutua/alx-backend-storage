#!/usr/bin/env python3
"""Implementation of the `Cache` Class.
The Class Leverages Redis to Implement Different
Caching Functions and Methods"""


import redis
import uuid
from typing import Union


class Cache:
    """Class to Hold Implementation of Different Caching functions"""

    def __init__(self):
        """Initialization Method for the `Cache` Class"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Type Annotated Method to take `data` arg
        That generates random key, store input data in Redis using
        the Generated Key, and returns the key."""

        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

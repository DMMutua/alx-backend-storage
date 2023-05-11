#!/usr/bin/env python3
"""Implementation of the `Cache` Class.
The Class Leverages Redis to Implement Different
Caching Functions and Methods"""


import redis
import uuid
from typing import Union, Callable, Optional, Any, TypeVar
import functools

T = TypeVar('T')


def count_calls(func: Callable) -> Callable:
    """A Decorator that Counts
    Number of Times a Method is called."""

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        key = func.__qualname__
        self._redis.incr(key)
        call = pickle.dumps((args, func(self, *args, **kwargs)))
        self._redis.rpush(key, call)
        return func(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """A Decorator that Stores the Call
    History of Cache Methods"""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key_inputs = "{}:inputs".format(method.__qualname__)
        key_outputs = "{}:outputs".format(method.__qualname__)
        self._redis.rpush(key_inputs, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(key_outputs, output)
        return output
    return wrapper


def replay(func: Callable) -> None:
    """display the history of calls of a particular function.
    """

    key_inputs = f"{func.__qualname__}:inputs"
    key_outputs = f"{func.__qualname__}:outputs"
    inputs = cache._redis.lrange(key_inputs, 0, -1)
    outputs = cache._redis.lrange(key_outputs, 0, -1)
    print(f"{func.__qualname__} was called {len(inputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{func.__qualname__}(*{inp.decode('utf-8')}) ->
                {out.decode('utf-8')}")


class Cache:
    """Class to Hold Implementation of Different Caching functions"""

    def __init__(self):
        """Initialization Method for the `Cache` Class"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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

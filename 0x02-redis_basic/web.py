#!/usr/bin/env python3
"""Implementation of the get_page function"""


import requests
import redis
from functools import wraps
from typing import Callable


# initialize Redis connection
r = redis.Redis()


def count_accesses(func: Callable) -> Callable:
    """Defines a Decorator for Counting accesses"""
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        r.incr(count_key)
        return func(url)
    return wrapper


def cache_with_expiry(expiration: int) -> Callable:
    """Defines a Decorator for caching with expiration"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            cache_key = f"cache:{url}"
            cached_page = r.get(cache_key)
            if cached_page:
                return cached_page.decode()
            page_content = func(url)
            r.set(cache_key, page_content, ex=expiration)
            return page_content
        return wrapper
    return decorator


@cache_with_expiry(10)
@count_accesses
def get_page(url: str) -> str:
    """uses the requests module to obtain the HTML
    content of a particular URL and returns it."""

    response = requests.get(url)
    return response.text

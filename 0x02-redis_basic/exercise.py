#!/usr/bin/env python3
'''0. Writing strings to Redis'''
import redis
from uuid import uuid4
from typing import Union


class Cache:
    '''create redis store for caching'''

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, int, bytes, float]) -> str:
        key = str(uuid4())
        self._redis.set(key, data)
        return key

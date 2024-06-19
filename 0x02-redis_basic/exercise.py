#!/usr/bin/env python3
'''0. Writing strings to Redis'''
import redis
from uuid import uuid4
from typing import Union


class Cache:
    '''create redis store for caching'''

    def __init__(self):
        '''store an instance of the Redis client as a private variable
        named _redis and flush it'''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, int, bytes, float]) -> str:
        '''takes a data argument and returns a string. The method should
        generate a random key (e.g. using uuid), store the input data
        in Redis using the random key and return the key.'''
        key = str(uuid4())
        self._redis.set(key, data)
        return key

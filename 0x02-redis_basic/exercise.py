#!/usr/bin/env python3
'''0. Writing strings to Redis'''
import redis
from uuid import uuid4
from typing import Union, Optional, Callable, Any


class Cache:
    '''create redis store for caching'''

    def __init__(self) -> None:
        '''store an instance of the Redis client as a private variable
        named _redis and flush it'''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, int, bytes, float]) -> str:
        '''takes a data argument and returns a string. The method should
        generate a random key (e.g. using uuid), store the input data
        in Redis using the random key and return the key.'''
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        ''' take a key string argument and an optional Callable argument.
        This callable will be used to convert the data back to
        the desired format.'''
        val = self._redis.get(key)
        if fn is str:
            return self.get_str(val)
        if fn is int:
            return self.get_int(val)
        if fn:
            return fn(val)
        return val

    def get_str(self, val: bytes) -> str:
        '''get str from bytes'''
        return val.decode('utf-8')

    def get_int(self, val: bytes) -> int:
        '''get int from bytes'''
        return int(val)

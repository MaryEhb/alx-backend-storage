#!/usr/bin/env python3
'''0. Writing strings to Redis'''
import redis
from uuid import uuid4
from typing import Union, Optional, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''count calls of method'''
    @wraps(method)
    def wrapper(self: Any, *args, **kwargs) -> str:
        ''' '''
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    ''' '''
    @wraps(method)
    def wrapper(self: Any, *args) -> str:
        ''' '''
        self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args)
        self._redis.rpush(f'{method.__qualname__}:outputs', output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    '''function to display the history of calls of a particular function.'''
    client = redis.Redis()
    calls = client.get(fn.__qualname__).decode('utf-8')
    inputs = [input.decode('utf-8') for input in
              client.lrange(f'{fn.__qualname__}:inputs', 0, -1)]
    outputs = [output.decode('utf-8') for output in
               client.lrange(f'{fn.__qualname__}:outputs', 0, -1)]
    print(f'{fn.__qualname__} was called {calls} times:')
    for input, output in zip(inputs, outputs):
        print(f'{fn.__qualname__}(*{input}) -> {output}')


class Cache:
    '''create redis store for caching'''

    def __init__(self) -> None:
        '''store an instance of the Redis client as a private variable
        named _redis and flush it'''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
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

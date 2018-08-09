#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging
import asyncio

from nose.tools import ok_, eq_

from .queue import AsyncQueue, Queue


RABBITMQ_URL = 'amqp://rabbitmq:5672'

QUEUE = 'test'

STRING = b'Hello world'


def test_create_queue():
    Queue.connect(RABBITMQ_URL)
    
    q = Queue(QUEUE)
    q.put(STRING.decode('utf-8'))

    eq_(q.receive_one()[2], STRING)


def test_async_queue():

    async def test():
        AsyncQueue.connect(RABBITMQ_URL)

        q = AsyncQueue(QUEUE)
        await q.put(STRING.decode('utf-8'))

        eq_((await q.receive_one()).body, STRING)
    
    asyncio.run(test())

    





    


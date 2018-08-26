
import asyncio
import logging

import aio_pika
import pika

from pika.connection import ConnectionParameters

from .base import BaseQueue


class AsyncQueue(BaseQueue):

    '''
    A async implementation
    '''

    @classmethod
    def connect(cls, *args, concurrent=20, **kwargs):
        '''
        Should take in connection parameters 
        '''
        cls.connection_args = args
        cls.connection_kwargs = kwargs

    async def _get_connection(self):
        return await aio_pika.connect_robust(*self.__class__.connection_args, **self.__class__.connection_kwargs)

    async def _get_channel(self, connection):
        channel = await connection.channel()
        if not self.initalized:
            await channel.declare_queue(self.queue_name)
            self.initalized = True
        return channel


    def __init__(self, queue_name):
        '''
        Should create a queue
        '''
        self.queue_name = queue_name
        self.initalized = False


    async def put(self, message):
        '''
        Should put a message in the queue
        '''
        connection = await self._get_connection()
        channel = await self._get_channel(connection)
        await channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=self.queue_name
        )
        await channel.close()
        await connection.close()


    async def receive(self):
        connection = await self._get_connection()
        channel = await self._get_channel(connection)
        try:
            async for message in await channel.declare_queue(self.queue_name):
                with message.process():
                    yield message
        finally:
            await channel.close()
            await connection.close()

    async def receive_one(self):
        return await self.receive().__anext__()


class Queue(BaseQueue):

    @classmethod
    def connect(cls, *args, **kwargs):
        '''
        Should take in connection parameters 
        '''
        cls.connection_args = args
        cls.connection_kwargs = kwargs


    def _get_connection(self):
        return pika.BlockingConnection(pika.connection.URLParameters(*self.__class__.connection_args, **self.__class__.connection_kwargs))

    def _get_channel(self, connection):
        channel = connection.channel()
        if not self.initialized:
            channel.queue_declare(self.queue_name)
            self.initialized = True
        return channel


    def __init__(self, queue_name):
        '''
        Should create a queue
        '''
        self.queue_name = queue_name
        self.initialized = False


    def put(self, message):
        '''
        Should put a message in the queue
        '''
        connection = self._get_connection()
        channel = self._get_channel(connection)
        try:
            channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message.encode()
            )
        finally:
            channel.close()
            connection.close()

    def receive(self):
        print('Ready to consume!')
        connection = self._get_connection()
        channel = self._get_channel(connection)
        try:
            for message in channel.consume(self.queue_name):
                method_frame, header_frame, body = message
                channel.basic_ack(method_frame.delivery_tag)
                yield method_frame, header_frame, body

        finally:
            channel.close()
            connection.close()

    def receive_one(self):
        return next(self.receive())


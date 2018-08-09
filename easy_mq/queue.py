import aio_pika 
import pika

from pika.connection import ConnectionParameters

from .base import BaseQueue


class AsyncQueue(BaseQueue):

    '''
    A async implementation
    '''

    @classmethod
    def connect(cls, *args, **kwargs):
        '''
        Should take in connection parameters 
        '''
        cls.connection_args = args
        cls.connection_kwargs = kwargs

    async def _get_connection(self):
        return await aio_pika.connect_robust(*self.__class__.connection_args, **self.__class__.connection_kwargs)

    async def _get_channel(self):
        connection = await self._get_connection()
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
        channel = await self._get_channel()
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message.encode()
            ),
            routing_key=self.queue_name
        )

    async def receive(self):
        channel = await self._get_channel()
        async for message in await channel.declare_queue(self.queue_name):
            with message.process():
                message.ack()
                yield message

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

    def _get_channel(self):
        connection = self._get_connection()
        channel = connection.channel()
        if not self.initalized:
            channel.queue_declare(self.queue_name)
            self.initalized = True
        return channel

    def __init__(self, queue_name):
        '''
        Should create a queue
        '''
        self.queue_name = queue_name
        self.initalized = False


    def put(self, message):
        '''
        Should put a message in the queue
        '''
        channel = self._get_channel()
        channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message.encode()
        )
        

    def receive(self):
        print('Ready to consume!')
        channel = self._get_channel()
        for message in channel.consume(self.queue_name):
            method_frame, header_frame, body = message
            channel.basic_ack(method_frame.delivery_tag)
            yield method_frame, header_frame, body


    def receive_one(self):
        return next(self.receive())


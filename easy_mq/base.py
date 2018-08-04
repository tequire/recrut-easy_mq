

class BaseQueue:

    '''
    Defines the basic interface for a queue
    '''

    @classmethod
    def connect(cls, *args, **kwargs):
        '''
        Should take in connection parameters 
        '''
        raise NotImplementedError

    def __init__(self, queue_name):
        '''
        Should create a queue
        '''
        raise NotImplementedError

    def put(self, message):
        '''
        Should put a message in the queue
        '''
        raise NotImplementedError

    def receive(self):
        '''
        should receive forever
        '''
        raise NotImplementedError
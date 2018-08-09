# EasyMQ

*Library for using RabbitMQ with python.*

This library was made to create a unified interface for async and sync message queues in Python. This project was made to manage queues between an async server and a sync server. 

To be implemented: 
- Message class
- More advanced features (these will be implemented as needed)

### Sync
```python 

from easy_mq.queue import Queue

Queue.connect('url')

q = Queue('queue_name')
q.put('message') 

for message in q.revivaid():
    print(message)

```

### Async 
```python 


from easy_mq.queue import AsyncQueue

AsyncQueue.connect('url')

async def main():

    q = AsyncQueue('queue_name')
    q.put('message') 

    async for message in q.revivaid():
        print(message)

import asyncio 
asyncio.run(main())

```

### To run tests 

```bash
source scripts/test.sh
```

# Basic lib

Library for using rabbit mq

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

AsyncQueue.connect(host='url')

async def main():

    q = AsyncQueue('queue_name')
    q.put('message') 

    async for message in q.revivaid():
        print(message)

import asyncio 
asyncio.run(main())

```

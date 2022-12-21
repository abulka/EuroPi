import asyncio

async def one():
    print('one')
    await asyncio.sleep(1)
    print('one again')
    return 'one'

async def two():
    print('two')
    await asyncio.sleep(2)
    print('two again')
    return 'two'

# main 

loop = asyncio.get_event_loop()
tasks = [one(), two()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

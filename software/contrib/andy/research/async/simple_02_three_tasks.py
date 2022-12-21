import asyncio

async def one():
    print('one')
    await asyncio.sleep(1)
    print('one again')
    return 'one'

async def two():
    task3 = asyncio.create_task(three())
    print('two')
    await asyncio.sleep(2)
    print('two again')
    print(await task3)
    return 'two'

async def three():
    print('three')
    await asyncio.sleep(3)
    print('three again')
    return 'three'

# main 

loop = asyncio.get_event_loop()
tasks = [one(), two()]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

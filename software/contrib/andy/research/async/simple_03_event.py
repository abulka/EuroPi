import asyncio

event1 = asyncio.Event()

async def one():
    print('one')
    await asyncio.sleep(1)
    print('one again')
    event1.set()
    await asyncio.sleep(1)
    event1.set()
    await asyncio.sleep(1)

    # cancel other tasks
    for task in asyncio.all_tasks():
        if task is not asyncio.current_task():
            task.cancel()

    return 'one'

async def two():
    try:                
        while True:
            await event1.wait()
            print('got event')
            event1.clear()
    except asyncio.CancelledError:
        print(f"Exiting task two...")    

# main 

loop = asyncio.get_event_loop()
tasks = [one(), two()]
try:
    loop.run_until_complete(asyncio.wait(tasks))
except asyncio.exceptions.CancelledError:
    pass
loop.close()

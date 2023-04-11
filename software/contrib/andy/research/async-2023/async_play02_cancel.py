import asyncio
import time

# experiments - ABORTED

# async def print_char(char, delay):
#     try:
#         while True:
#             print(char, end='', flush=True)
#             await asyncio.sleep(delay)
#     except asyncio.CancelledError:
#         print(f"\nTask {char} cancelled.")
#         raise
    
# async def main():
#     task1 = asyncio.create_task(print_char("A", 1))
#     task2 = asyncio.create_task(print_char("B", 2))
#     task3 = asyncio.create_task(print_char("C", 3))
    
#     try:
#         await asyncio.gather(task1, task2, task3)
#     except KeyboardInterrupt:
#         print("\nGot Ctrl-C, cancelling tasks...")
#         task1.cancel()
#         task2.cancel()
#         task3.cancel()
#         await asyncio.gather(task1, task2, task3, return_exceptions=True)

async def waste_time_freely():
    '''This method is also run by the asyncio loop and periodically prints
    something.
    '''
    try:
        while True:
            print('Sitting on the beach')
            await asyncio.sleep(2)
    except asyncio.CancelledError as e:
        print('Wasting time was canceled', e)
    finally:
        # when canceled, print that it finished
        print('Done wasting time')

async def heartbeat():
    while True:
        start = time.time()
        await asyncio.sleep(1)
        delay = time.time() - start - 1
        # print(f'heartbeat delay = {delay:.3f}s')

if __name__ == '__main__':

    def root_func():
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        # other_task = asyncio.ensure_future(mc.main())
        other_task = asyncio.ensure_future(waste_time_freely())
        heartbeat_task = asyncio.ensure_future(heartbeat())

        # return asyncio.gather(run_app_happily(root, other_task), other_task)
        # return asyncio.gather(run_app_happily(root, other_task), other_task, heartbeat_task)
        return asyncio.gather(other_task, heartbeat_task)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(root_func())
    except asyncio.CancelledError as e:
        print('Wasting time was canceled', e)
    loop.close()
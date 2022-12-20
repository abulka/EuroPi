import sys
import functools
import asyncio
import time
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg, oled, bootsplash, b1, b2, din, k1, k2

class Prompt:
    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.q = asyncio.Queue()
        self.loop.add_reader(sys.stdin, self.got_input)

    def got_input(self):
        asyncio.ensure_future(self.q.put(sys.stdin.readline()), loop=self.loop)

    async def __call__(self, msg, end='\n', flush=False):
        print(msg, end=end, flush=flush)
        return (await self.q.get()).rstrip('\n')

prompt = Prompt()
raw_input = functools.partial(prompt, end='', flush=True)

mc = MasterClockInner()

async def heartbeat():
    while True:
        start = time.time()
        await asyncio.sleep(1)
        delay = time.time() - start - 1
        print(f'heartbeat delay = {delay:.3f}s')

async def user_prompter():
    while True:
        # wait for user to press enter
        await prompt("press enter to continue")

        # simulate raw_input
        result = await raw_input('enter something:')
        if result == 'q':
            # for task in asyncio.Task.all_tasks():
            #     task.cancel()
            exit()

async def user_prompt_stop_start_mc():
    while True:
        # simulate raw_input
        result = await raw_input('')
        if result == 's':
            print('b1 down')
            b1.pin.value(0)
            b1.fake_debounce()
            print('b1 up')
            b1.pin.value(1)
            b1.fake_debounce()
            b1._falling_handler()

        elif result == 'q':
            # for task in asyncio.Task.all_tasks():
            #     task.cancel()
            exit()

def root_func():
    '''This will run both methods asynchronously and then block until they
    are finished
    '''
    # task1 = asyncio.ensure_future(user_prompter())
    task1 = asyncio.ensure_future(user_prompt_stop_start_mc())
    task2 = asyncio.ensure_future(heartbeat())
    task3 = asyncio.ensure_future(mc.main())

    return asyncio.gather(task1, task2, task3)

loop = asyncio.get_event_loop()
loop.run_until_complete(root_func())
loop.close()

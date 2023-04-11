import asyncio

async def print_char(char, delay):
    while True:
        print(char, end='', flush=True)
        await asyncio.sleep(delay)

async def main():
    task1 = asyncio.create_task(print_char("A", 1))
    task2 = asyncio.create_task(print_char("B", 2))
    task3 = asyncio.create_task(print_char("C", 3))
    
    await asyncio.gather(task1, task2, task3)

asyncio.run(main())

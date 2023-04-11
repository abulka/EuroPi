import asyncio

"""
cv_trigger and din_trigger should be independent. yes din_trigger causes
cv_trigger but they should still be 1 and 0 independently. report is also
independent. I am building a trigger to gate simulation where din_trigger is the
short trigger which results in a longer cv_trigger gate. 
"""

class DinTrigger:
    def __init__(self):
        self.din_period = 1000
        self.din_length = 500
        self.cv_length = 1500
        self.report_interval = 200
        self.din_state = 0
        self.cv_state = 0
        
    async def report(self, msg=''):
        while True:
            print(f'{self.din_state} {self.cv_state}')
            await asyncio.sleep(self.report_interval / 1000)
    
    async def cv_trigger(self):
        self.cv_state = 1
        await asyncio.sleep(self.cv_length / 1000)
        self.cv_state = 0

    async def din_trigger(self):
        while True:
            await asyncio.sleep(self.din_period / 1000)
            self.din_state = 1
            task = asyncio.create_task(self.cv_trigger())
            await asyncio.sleep(self.din_length / 1000)
            self.din_state = 0
            await task # need this otherwise cv_state appears always as 1

async def main():
    dt = DinTrigger()
    asyncio.create_task(dt.report())
    asyncio.create_task(dt.din_trigger())
    await asyncio.sleep(10)


asyncio.run(main())

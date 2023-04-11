import asyncio

class DinTrigger:
    def __init__(self, trigger_period=1000, gate_length=1500):
        self.trigger_period = trigger_period
        self.gate_length = gate_length
        
    async def cv1_out(self):
        print('high')
        await asyncio.sleep(self.gate_length / 1000)
        print('low')
    
    async def din_trigger(self):
        while True:
            print('trigger')
            await self.cv1_out()
            await asyncio.sleep(self.trigger_period / 1000)

async def main():
    dt = DinTrigger()
    await dt.din_trigger()

asyncio.run(main())

'''Example shows the recommended way of how to run Kivy with the Python built
in asyncio event loop as just another async coroutine.
'''
import asyncio

from kivy.app import async_runTouchApp
from kivy.lang.builder import Builder
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg, oled, bootsplash, b1, b2, din, k1, k2

kv = '''
BoxLayout:
    orientation: 'vertical'
    Button:
        id: btn
        text: 'Press me'
    GridLayout:
        cols: 3
        Button:
            id: btn
            text: 'Press me'
        Button:
            id: btn
            text: 'Press me'
        Button:
            id: btn
            text: 'Press me'
    Button:
        id: btn
        text: 'Press me'
    Button:
        id: btn
        text: 'Press me'
    BoxLayout:
        Label:
            id: label
            text: 'Button is "{}"'.format(btn.state)
'''


async def run_app_happily(root, other_task):
    '''This method, which runs Kivy, is run by the asyncio loop as one of the
    coroutines.
    '''
    # we don't actually need to set asyncio as the lib because it is the
    # default, but it doesn't hurt to be explicit
    await async_runTouchApp(root, async_lib='asyncio')  # run Kivy
    print('App done')
    # now cancel all the other tasks that may be running
    other_task.cancel()


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

if __name__ == '__main__':
    def root_func():
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        root = Builder.load_string(kv)  # root widget
        # other_task = asyncio.ensure_future(waste_time_freely())
        mc = MasterClockInner()
        other_task = asyncio.ensure_future(mc.main())

        return asyncio.gather(run_app_happily(root, other_task), other_task)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(root_func())
    except asyncio.CancelledError as e:
        print('Wasting time was canceled', e)
    loop.close()

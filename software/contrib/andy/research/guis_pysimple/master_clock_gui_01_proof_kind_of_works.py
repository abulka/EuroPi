# Andy's ongoing led demo using PySimpleGUI and asyncio

import asyncio
import random
import PySimpleGUI as sg
from master_clock import MasterClockInner

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def LEDIndicator(key=None, radius=30):
    return sg.Graph(canvas_size=(radius, radius),
                    graph_bottom_left=(-radius, -radius),
                    graph_top_right=(radius, radius),
                    pad=(0, 0), key=key)


def SetLED(window, key, color):
    graph = window[key]
    graph.erase()
    graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)


layout = [[sg.Text('My LED Status Indicators', size=(20, 1))],
          [sg.Text('CPU Use'), LEDIndicator('_cpu_')],
          [sg.Text('RAM'), LEDIndicator('_ram_')],
          [sg.Text('Temperature'), LEDIndicator('_temp_')],
          [sg.Text('Server 1'), LEDIndicator('_server1_')],
          [sg.Button('Andy')],
          [sg.Button('Exit')],
          ]

window = None

async def andy_pressed():
    print('andy pressed')
    await asyncio.sleep(1)
    print('andy done')

async def gui_window_loop():
    global window
    window = sg.Window('EuroPi', layout, default_element_size=(
        20, 1), auto_size_text=False, finalize=True)

    i = 0
    while True:
        await asyncio.sleep(0.200)

        event, value = window.read(0)
        if event == "Andy":
            asyncio.create_task(andy_pressed())
        if event == "Exit" or event == None:
            break
        if event == "__TIMEOUT__":
            i += 1
            SetLED(window, '_cpu_', 'green' if random.randint(
                1, 10) > 5 else 'red')
            SetLED(window, '_ram_', 'green' if random.randint(
                1, 10) > 5 else 'red')
            SetLED(window, '_temp_', 'green' if random.randint(
                1, 10) > 5 else 'red')
            SetLED(window, '_server1_',
                   'green' if random.randint(1, 10) > 5 else 'red')
            # continue
        print('HA', event, value)
    window.close()


async def auto_close_no_window():
    global window
    while True:
        if window.TKrootDestroyed:
            break
        await asyncio.sleep(0)
    return

try:
    window_main = asyncio.ensure_future(gui_window_loop())
    window_watcher = asyncio.ensure_future(auto_close_no_window())
    window_watcher.add_done_callback(
        lambda f: (print("done_callback called !"), loop.stop())
    )

    mc = MasterClockInner()
    master_clock = asyncio.ensure_future(mc.main())

    # OLD
    loop.run_forever()
    # NEW, not sure how to get this working
    # try:
    #     asyncio.run(window_main(loop=loop))
    # except KeyboardInterrupt:
    #     pass    
except:
    canceltasks = [task.cancel() for task in asyncio.all_tasks()]
    try:
        print(f"cancelling {len(canceltasks)} tasks")
        loop.run_until_complete(asyncio.wait(canceltasks, timeout=10))
    except asyncio.TimeoutError:
        print("timeout when trying to cancel running tasks")
finally:
    print("closing loop")
    loop.close()

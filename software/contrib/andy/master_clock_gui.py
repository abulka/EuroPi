# Andy's ongoing led demo using PySimpleGUI and asyncio
# Run 'psgdemos' for a demo of PySimpleGUI

import asyncio
import random
import PySimpleGUI as sg  # pip install PySimpleGUI
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg

sg.theme('SystemDefaultForReal')  # better looking buttons

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
          [sg.Text('cv1', justification='right'), LEDIndicator('_cv1_'),
           sg.Text('cv2', justification='right'), LEDIndicator('_cv2_'),
           sg.Text('cv3', justification='right'), LEDIndicator('_cv3_')],
          [sg.Text('cv4', justification='right'), LEDIndicator('_cv4_'),
           sg.Text('cv5', justification='right'), LEDIndicator('_cv5_'),
           sg.Text('cv6',  justification='right'), LEDIndicator('_cv6_')],
          [sg.Text('', size=(None, 1), font='Helvetica 24', k='_cvs_')],
          [sg.Text('', size=(None, 1), font='Helvetica 24', k='_cvs-msg_')],
          [sg.Button('Andy', use_ttk_buttons=True, font='Courier 16'),
          sg.Button('Exit', font='Courier 16')
           ],
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
        await asyncio.sleep(0.1)
        event, value = window.read(0)
        if event == "Andy":
            asyncio.create_task(andy_pressed())
        if event == "Exit" or event == None:
            break
        if event == "__TIMEOUT__":
            global mc
            # make a copy since master clock is updating it
            cvs_snapshot = [1 if value !=
                            0 else 0 for value in mc.cvs_snapshot]
            window['_cvs_'].update(f'{cvs_snapshot}')
            window['_cvs-msg_'].update(f'{get_cvs_snapshot_msg()}')
            for index, value in enumerate(cvs_snapshot):
                ref = f'_cv{index+1}_'
                SetLED(window, ref, 'red' if value != 0 else 'green')

        # print('HA', event, value)
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

# Andy's ongoing led demo using PySimpleGUI and asyncio
# Run 'psgdemos' for a demo of PySimpleGUI

import asyncio
import random
import PySimpleGUI as sg  # pip install PySimpleGUI
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg, oled

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


# def drawOnDisplay(window, key='canvas', color='green'):

# column_to_be_centered2 = [
#         [sg.Text('digital', justification='center'), LEDIndicator('_din_'),
#      sg.Text('analogue', justification='center'), LEDIndicator('_ain_')]]

# column_to_be_centered3 = [
#     [sg.Button('Btn1', use_ttk_buttons=True, font='Courier 14'),
#      sg.Button('Btn2', use_ttk_buttons=True, font='Courier 14')
#      ]]

# column_to_be_centered = [
#         [sg.Slider(range=(1, 500),
#                default_value=222,
#                size=(20, 15),
#                orientation='horizontal',
#                font=('Helvetica', 12)),
#      sg.Slider(range=(1, 500),
#                default_value=222,
#                size=(20, 15),
#                orientation='horizontal',
#                font=('Helvetica', 12))],
# ]

layout = [
    # [sg.VPush()],
    # [sg.Push(), sg.Column(column_to_be_centered, element_justification='c'), sg.Push()],
    # [sg.VPush()],
    # [sg.VPush()],
    # [sg.Push(), sg.Column(column_to_be_centered2, element_justification='c'), sg.Push()],
    # [sg.VPush()],
    # [sg.VPush()],
    # [sg.Push(), sg.Column(column_to_be_centered3, element_justification='c'), sg.Push()],
    # [sg.VPush()],

    [sg.Text('digital', justification='right'), LEDIndicator('_din_'),
     sg.Text('analogue', justification='right'), LEDIndicator('_ain_')],
    # [sg.Multiline('128x32 MULTILINE TEXT display', size=(None, 4),
    #               font='Helvetica 14', k='_disp_', no_scrollbar=True)],
    # [sg.Canvas(size=(128, 32), key='canvas')],
    [sg.Canvas(size=(128*5, 32*5), background_color='white', key='canvas')],
    [sg.Slider(range=(1, 500),
               default_value=222,
               size=(20, 15),
               orientation='horizontal',
               font=('Helvetica', 12)),
     sg.Slider(range=(1, 500),
               default_value=222,
               size=(20, 15),
               orientation='horizontal',
               font=('Helvetica', 12))],
    [sg.Button('Btn1', use_ttk_buttons=True, font='Courier 14', pad=(100,0)), 
     sg.Button('Btn2', use_ttk_buttons=True, font='Courier 14')
     ],
    [sg.Text('My LED Status Indicators', size=(20, 1))],
    [sg.Text('cv1', justification='right'), LEDIndicator('_cv1_'),
     sg.Text('cv2', justification='right'), LEDIndicator('_cv2_'),
     sg.Text('cv3', justification='right'), LEDIndicator('_cv3_')],
    [sg.Text('cv4', justification='right'), LEDIndicator('_cv4_'),
     sg.Text('cv5', justification='right'), LEDIndicator('_cv5_'),
     sg.Text('cv6',  justification='right'), LEDIndicator('_cv6_')],
    [sg.Text('', size=(None, 1), font='Helvetica 24', k='_cvs_')],
    [sg.Text('', size=(None, 1), font='Helvetica 24', k='_cvs-msg_')],
    [sg.Button('Andy', use_ttk_buttons=True, font='Courier 16'),
     sg.Button('Exit', use_ttk_buttons=True, font='Courier 16')
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

    SetLED(window, '_din_', 'red')
    SetLED(window, '_ain_', 'red')
    
    canvas = window['canvas'].TKCanvas
    txt = demo(canvas)

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

        # drawOnDisplay(window)
        # colour = 'red' if i % 2 == 0 else 'green'
        # canvas.itemconfig(cir, fill=colour)
        # canvas.itemconfig(txt, text=f'ABCDEFG {i}')
        canvas.itemconfig(txt, text=f'ABCDEFG {oled.latest_text} {i}')
        # canvas.itemconfig(txt, angle=90)
        i += 1

        # print('HA', event, value)
    window.close()

def demo(canvas):
    cir = canvas.create_oval(50, 50, 100, 100)

    canvas.create_text((0, 0,),  anchor='nw', text=oled.latest_text, font=('Helvetica', 14), fill='DarkKhaki') # must have fill, and anchor='nw' helps position text
    canvas.create_text(50, 50, text='Hi', fill='black', font=('Helvetica', 24))
    txt = canvas.create_text(10, 100, text=oled.latest_text, anchor='nw', font=('Courier', 50), fill='blue') # font='TkMenuFont'
    
    lin = canvas.create_line(10, 10, 200, 50, 90, 150, 50, 80, arrow='last', fill='green')  # must have fill
    rect = canvas.create_rectangle(120, 10, 200, 50, fill='burlywood1', outline='blue')
    return txt


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

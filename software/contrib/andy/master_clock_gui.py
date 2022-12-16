# Andy's ongoing led demo using PySimpleGUI and asyncio
# Run 'psgdemos' for a demo of PySimpleGUI

import asyncio
import random
import PySimpleGUI as sg  # pip install PySimpleGUI
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg, oled, bootsplash, b1, b2, din, k1, k2


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


layout = [
    [sg.Text('digital', justification='right'), LEDIndicator('_din_'), sg.Button('dinbtn', use_ttk_buttons=True, font='Courier 10'),
     sg.Text('analogue', justification='right'), LEDIndicator('_ain_')],
    [sg.Canvas(size=(128*2, 32*2), background_color='white', key='canvas')],
    [sg.Slider(range=(1, 65535),
               k='k1',
               default_value=222,
               size=(20, 15),
               orientation='horizontal',
               font=('Helvetica', 12)),
     sg.Slider(range=(1, 65535),
               k='k2',
               default_value=222,
               size=(20, 15),
               orientation='horizontal',
               font=('Helvetica', 12))],
    [sg.RealtimeButton(sg.SYMBOL_CIRCLE, key='b1'), sg.RealtimeButton(sg.SYMBOL_CIRCLE, key='b2')],
    # [sg.Button('b1', use_ttk_buttons=True, font='Courier 14', pad=(100, 0)),
    #  sg.Button('b2', use_ttk_buttons=True, font='Courier 14')],
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


async def andy_pressed(canvas):
    print('andy pressed')
    canvas.delete('all')
    bootsplash()
    await asyncio.sleep(2)
    print('andy done')


async def gui_window_loop():
    global window
    window = sg.Window('EuroPi', layout, default_element_size=(
        20, 1), auto_size_text=False, finalize=True)

    SetLED(window, '_din_', 'green')
    SetLED(window, '_ain_', 'green')

    b1.pin.value(1) # reverse pin logic high/low/pull stuff
    b2.pin.value(1) # reverse pin logic high/low/pull stuff

    canvas = window['canvas'].TKCanvas
    values_last = { 'k1': 0, 'k2': 0, 'b1': 'up', 'b2': 'up' }

    i = 0
    while True:
        await asyncio.sleep(0.1)
        event, values = window.read(0)

        # this is how you intercept slider changes it seems
        if int(values['k1'] != values_last['k1']):
            values_last['k1'] = values['k1']
            k1.pin._pin._value = int(values['k1'])
        if int(values['k2'] != values_last['k2']):
            values_last['k2'] = values['k2']
            k2.pin._pin._value = int(values['k2'])

        if event == "Andy":
            asyncio.create_task(andy_pressed(canvas))

        # Buttons are normally high, and 'pulled' low when on, value 0
        # means button is down and pulse state in EuroPi is HIGH.
        # Only call fake_debounce() on the transition from up to down, not all the time
        if event == "b1":
            if values_last['b1'] == 'up':
                b1.pin.value(0)
                b1.fake_debounce()
            values_last['b1'] = 'down'
        if event == "b2":
            if values_last['b2'] == 'up':
                b2.pin.value(0)
                b2.fake_debounce()
            values_last['b2'] = 'down'
        if event == "dinbtn":
            din._rising_handler()
        if event == "Exit" or event == None:
            break
        if event == "__TIMEOUT__":
            # Update LEDS - note the display is running at a different async loop
            # speed than the EuroPi clock, so we can't turn off leds with the 
            # same timing as the EuroPi clock. So unfortunately 
            # some leds stay on permanently e.g. cv1.

            # make a copy since master clock is updating it
            cvs_snapshot = [1 if value !=
                            0 else 0 for value in mc.cvs_snapshot]
            # window['_cvs_'].update(f'{cvs_snapshot}')
            # window['_cvs-msg_'].update(f'{get_cvs_snapshot_msg()}')
            for index, values in enumerate(cvs_snapshot):
                ref = f'_cv{index+1}_'
                SetLED(window, ref, 'red' if values != 0 else 'green')

        # Fake button up events, if got to here then no button was pressed
        if event != "b1" and values_last['b1'] == 'down':
            print('b1 up')
            values_last['b1'] = 'up'
            b1.pin.value(1)
            b1.fake_debounce()
            b1._falling_handler()
        if event != "b2" and values_last['b2'] == 'down':
            print('b2 up')
            values_last['b2'] = 'up'
            b2.pin.value(1)
            b2.fake_debounce()
            b2._falling_handler()

        update_display(canvas)
        i += 1

        # print('HA', event, values)
    window.close()


def update_display(canvas):
    if not oled.flush_to_ui:
        return
    for cmd in oled.commands:
        command = cmd[0]
        params = cmd[1]
        if command == 'text':
            text, x, y, colour = params
            font_size = 14
            fill = 'black'
            if colour == 88:
                fill = 'green'
                font_size = 12
            canvas.create_text((x, y,),  anchor='nw', text=text, font=(
                'Helvetica', font_size), fill=fill)  # must have fill, and anchor='nw' helps position text
        elif command == 'fill':
            value = params[0]
            if value == 0:
                canvas.delete('all')
        elif command == 'blit':
            frame_buffer, x, y = params
            filename = 'software/contrib/andy/logo.xbm'
            convert_to_xbm(frame_buffer, filename)
            canvas.create_bitmap(
                130, 20, bitmap=f'@{filename}', foreground='green')  # WORKS!  🎉
        else:
            print('unknown command', command)
    oled.commands = []
    oled.flush_to_ui = False


def convert_to_xbm(frame_buffer, filename):
    msg = f'#define im_width {frame_buffer.width}\n#define im_height {frame_buffer.height}\nstatic char im_bits[] = {{\n'
    idx = 0
    for byte in frame_buffer.buffer:

        # change byte endian
        byte = (byte & 0xF0) >> 4 | (byte & 0x0F) << 4
        byte = (byte & 0xCC) >> 2 | (byte & 0x33) << 2
        byte = (byte & 0xAA) >> 1 | (byte & 0x55) << 1

        msg += '0x{:02x}'.format(byte) + ','
        idx += 1
        if idx % 8 == 0:
            msg += '\n'
    msg += '};'
    # write to file
    with open(filename, 'w') as f:
        f.write(msg)


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

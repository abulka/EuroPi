# PySimpleGui-asyncio-tasks.py
# But it doesn't use threads?
# https://gist.github.com/ultrafunkamsterdam/f840d48ba3451121b7197e7cde7ac303

import asyncio
import random
import PySimpleGUI as sg

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


form = sg.FlexForm(
    "Andy Demo", auto_size_text=True, default_element_size=(40, 1)
)

layout = [[sg.Text('My LED Status Indicators', size=(20,1))],
          [sg.Text('CPU Use'), LEDIndicator('_cpu_')],
          [sg.Text('RAM'), LEDIndicator('_ram_')],
          [sg.Text('Temperature'), LEDIndicator('_temp_')],
          [sg.Text('Server 1'), LEDIndicator('_server1_')],
          [sg.Button('Exit')]]

layout2 = [
    [
        sg.Text(
            "Hi Andy",
            size=(30, 1),
            font=("Helvetica", 25),
            text_color="blue",
        )
    ],
    [
        sg.Submit(),
        sg.Cancel(),
        # sg.SimpleButton("Customized", button_color=("white", "green")),
        sg.Button("Exit", button_color=("white", "green")),
    ],
]

WINDOWS = set()

async def gui_window_loop():
    
    main = form.Layout(layout2)
    WINDOWS.add(main)

    window = sg.Window('My new window', layout, default_element_size=(12, 1), auto_size_text=False, finalize=True)
    WINDOWS.add(window)

    i = 0
    while True:
        await asyncio.sleep(0.01)

        event, value = main.read(0)
        # if event == "__TIMEOUT__":
        #     continue
        print('HA', event, value)
        if event == "Cancel":
            print('Cancel was clicked by Andy')
            break
        if event == "Exit" or event == None:
            break
        # print(event, value)

        event, value = window.read(0)
        if event == "__TIMEOUT__":
            i += 1
            print(i)
            SetLED(window, '_cpu_', 'green' if random.randint(1, 10) > 5 else 'red')
            SetLED(window, '_ram_', 'green' if random.randint(1, 10) > 5 else 'red')
            SetLED(window, '_temp_', 'green' if random.randint(1, 10) > 5 else 'red')
            SetLED(window, '_server1_', 'green' if random.randint(1, 10) > 5 else 'red')
            continue
        print('HA', event, value)
        if event == "Cancel":
            print('Cancel was clicked by Andy')
            break
        if event == "Exit" or event == None:
            break


    main.close()
    window.close()


async def auto_close_no_window():
    while True:
        for window in WINDOWS:
            if window.TKrootDestroyed:
                WINDOWS.remove(window)
                break
        await asyncio.sleep(0)
        if len(WINDOWS) == 0:
            return

try:
    window_main = asyncio.ensure_future(gui_window_loop())
    # window_main2 = asyncio.ensure_future(gui_window_loop2())

    window_watcher = asyncio.ensure_future(auto_close_no_window())
    window_watcher.add_done_callback(
        lambda f: (print("done_callback called !"), loop.stop())
    )

    loop.run_forever()

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

# main = form.Layout(layout)

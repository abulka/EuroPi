# PySimpleGui-asyncio-tasks.py
# But it doesn't use threads?
# https://gist.github.com/ultrafunkamsterdam/f840d48ba3451121b7197e7cde7ac303

import asyncio
import PySimpleGUI as sg

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

form = sg.FlexForm(
    "Andy Demo", auto_size_text=True, default_element_size=(40, 1)
)

layout = [
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
        sg.Button("Quit", button_color=("white", "green")),
    ],
]

WINDOWS = set()

async def gui_window_loop():
    main = form.Layout(layout)
    WINDOWS.add(main)
    while True:
        await asyncio.sleep(0.01)
        event, value = main.read(0)
        if event == "__TIMEOUT__":
            continue
        print('HA', event, value)
        if event == "Cancel":
            print('Cancel was clicked by Andy')
            break
        if event == "Quit" or event == None:
            break
        # print(event, value)
    main.close()


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

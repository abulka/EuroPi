# Andy's ongoing led demo using PySimpleGUI and asyncio
# Run 'psgdemos' for a demo of PySimpleGUI

import asyncio
import random
import PySimpleGUI as sg  # pip install PySimpleGUI
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg, oled
from PIL import Image, ImageTk  # pip install pillow
from PIL.XbmImagePlugin import XbmImageFile


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
    [sg.Canvas(size=(128*2, 32*2), background_color='white', key='canvas')],
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
    # txt = demo(canvas)
    convert_to_xbm()

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
        # canvas.itemconfig(txt, text=f'ABCDEFG {oled.latest_text} {i}')
        # canvas.itemconfig(txt, angle=90)
        update_display(canvas)
        # canvas.create_bitmap(130, 20, bitmap='questhead', foreground='red')  #  🎉 https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/bitmaps.html
        # display custom bitmap from bytearray

        # tk.BitmapImage(data=...)
        # canvas.create_bitmap(130, 20, bitmap='@' + bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]), foreground='red') # CRASH
        # canvas.create_bitmap(130, 20, bitmap='@/Volumes/SSD/Data/Devel/EuroPi/software/contrib/andy/Untitled-2.xbm', foreground='red') # WORKS!
        # canvas.create_bitmap(130, 20, bitmap='@software/contrib/andy/Untitled-2.xbm', foreground='red') # WORKS! 🎉
        # canvas.create_image(130, 20, image=BITMAP, foreground='red') # CRASH

        # im1 = Image.open('/Volumes/SSD/Data/Devel/EuroPi/software/contrib/andy/Untitled-1.png').convert("1") # 🎉
        # size = (im1.width // 4, im1.height // 4)
        # im1 = ImageTk.BitmapImage(im1.resize(size))
        # canvas.create_image(130, 20, image=im1, foreground='red') # CRASH
        # canvas.create_bitmap(130, 20, bitmap=im1, foreground='red') # CRASH
        # save as xbm
        # XbmImageFile(im1).save('/Volumes/SSD/Data/Devel/EuroPi/software/contrib/andy/Untitled-3.xbm')
        # save as png
        # im1.save('/Volumes/SSD/Data/Devel/EuroPi/software/contrib/andy/Untitled-3.png', format='PNG') # WORKS
        
        # im1.save('/Volumes/SSD/Data/Devel/EuroPi/software/contrib/andy/Untitled-3.xbm', format='XBM') # WORKS  🎉
        # canvas.create_bitmap(130, 20, bitmap='@software/contrib/andy/Untitled-3.xbm', foreground='red') # WORKS!  🎉

        # write BITMAP to file
        BITMAP = """
        #define im_width 32
        #define im_height 32
        static char im_bits[] = {
        0xaf,0x6d,0xeb,0xd6,0x55,0xdb,0xb6,0x2f,
        0xaf,0xaa,0x6a,0x6d,0x55,0x7b,0xd7,0x1b,
        0xad,0xd6,0xb5,0xae,0xad,0x55,0x6f,0x05,
        0xad,0xba,0xab,0xd6,0xaa,0xd5,0x5f,0x93,
        0xad,0x76,0x7d,0x67,0x5a,0xd5,0xd7,0xa3,
        0xad,0xbd,0xfe,0xea,0x5a,0xab,0x69,0xb3,
        0xad,0x55,0xde,0xd8,0x2e,0x2b,0xb5,0x6a,
        0x69,0x4b,0x3f,0xb4,0x9e,0x92,0xb5,0xed,
        0xd5,0xca,0x9c,0xb4,0x5a,0xa1,0x2a,0x6d,
        0xad,0x6c,0x5f,0xda,0x2c,0x91,0xbb,0xf6,
        0xad,0xaa,0x96,0xaa,0x5a,0xca,0x9d,0xfe,
        0x2c,0xa5,0x2a,0xd3,0x9a,0x8a,0x4f,0xfd,
        0x2c,0x25,0x4a,0x6b,0x4d,0x45,0x9f,0xba,
        0x1a,0xaa,0x7a,0xb5,0xaa,0x44,0x6b,0x5b,
        0x1a,0x55,0xfd,0x5e,0x4e,0xa2,0x6b,0x59,
        0x9a,0xa4,0xde,0x4a,0x4a,0xd2,0xf5,0xaa
        };
        """        
        with open('/Volumes/SSD/Data/Devel/EuroPi/software/contrib/andy/Untitled-4.xbm', 'w') as f:
            f.write(BITMAP)
        # canvas.create_bitmap(130, 20, bitmap='@software/contrib/andy/Untitled-4.xbm', foreground='red') # WORKS!  🎉
        canvas.create_bitmap(130, 20, bitmap='@software/contrib/andy/logo.xbm', foreground='red') # WORKS!  🎉

        # canvas.create_bitmap(130, 20, bitmap='@/Volumes/SSD/Data/Devel/EuroPi/software/contrib/andy/Untitled-3.xbm', foreground='red') # CRASH

        i += 1

        # print('HA', event, value)
    window.close()

def update_display(canvas):
    if not oled.flush_to_ui:
        return
    for cmd in oled.commands:
        command = cmd[0]
        params = cmd[1]
        if command == 'text':
            text, x, y, colour = params
            canvas.create_text((x, y,),  anchor='nw', text=text, font=('Helvetica', 14), fill='black') # must have fill, and anchor='nw' helps position text
        elif command == 'fill':
            value = params[0]
            if value == 0:
                canvas.delete('all')
        else:
            print('unknown command', command)
    oled.commands = []
    oled.flush_to_ui = False

def demo(canvas):
    cir = canvas.create_oval(50, 50, 100, 100)

    canvas.create_text((0, 0,),  anchor='nw', text=oled.latest_text, font=('Helvetica', 14), fill='DarkKhaki') # must have fill, and anchor='nw' helps position text
    canvas.create_text(50, 50, text='Hi', fill='black', font=('Helvetica', 24))
    txt = canvas.create_text(10, 100, text=oled.latest_text, anchor='nw', font=('Courier', 50), fill='blue') # font='TkMenuFont'
    
    lin = canvas.create_line(10, 10, 200, 50, 90, 150, 50, 80, arrow='last', fill='green')  # must have fill
    rect = canvas.create_rectangle(120, 10, 200, 50, fill='burlywood1', outline='blue')
    return txt

def convert_to_xbm(byte_array=None):
    logo = b'\x00\x00\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x04\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc4\x04\x00\x18\x00\x00\x00p\x07\x00\x00\x00\x00\x00\x00\x0c$\x02\x00~\x0c\x18\xb9\x8c8\xc3\x00\x00\x00\x00\x00\x10\x14\x01\x00\xc3\x0c\x18\xc3\x060c\x00\x00\x00\x00\x00\x10\x0b\xc0\x80\x81\x8c\x18\xc2\x020#\x00\x00\x00\x00\x00 \x04\x00\x81\x81\x8c\x18\x82\x02 #\x00\x00\x00\x00\x00A\x8a|\x81\xff\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00FJC\xc1\x80\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00H\x898\x00\x80\x0c\x18\x83\x060c\x00\x00\x00\x00\x00S\x08\x87\x00\xc3\x060\x81\x8c8\xc3\x00\x00\x00\x00\x00d\x08\x00\xc0<\x01\xc0\x80p7\x03\x00\x00\x00\x00\x00X\x08p \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00#\x88H \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00L\xb8& \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x91P\x11 \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\xa6\x91\x08\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc9\x12\x84`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x12C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x11 \x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00H\x0c\x90\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x12\x88\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x12F\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04@@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    msg = '#define im_width 128\n#define im_height 32\nstatic char im_bits[] = {\n'
    idx = 0
    for byte in logo:
        # print byte in hex format
        # print('0x{:02x}'.format(byte), end=' ')
        msg += '0x{:02x}'.format(byte) + ','
        idx += 1
        if idx % 8 == 0:
            msg += '\n'
    msg += '};'
    # write to file
    with open('software/contrib/andy/logo.xbm', 'w') as f:
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

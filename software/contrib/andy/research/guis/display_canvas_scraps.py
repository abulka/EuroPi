import PySimpleGUI as sg  # pip install PySimpleGUI
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg, oled, bootsplash
from PIL import Image, ImageTk  # pip install pillow
from PIL.XbmImagePlugin import XbmImageFile

from PIL import Image, ImageTk  # pip install pillow
from PIL.XbmImagePlugin import XbmImageFile


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


# layout = [
#     [sg.VPush()],
#     [sg.Push(), sg.Column(column_to_be_centered, element_justification='c'), sg.Push()],
#     [sg.VPush()],
#     [sg.VPush()],
#     [sg.Push(), sg.Column(column_to_be_centered2, element_justification='c'), sg.Push()],
#     [sg.VPush()],
#     [sg.VPush()],
#     [sg.Push(), sg.Column(column_to_be_centered3, element_justification='c'), sg.Push()],
#     [sg.VPush()],

#     [sg.Text('digital', justification='right'), LEDIndicator('_din_'),
#      sg.Text('analogue', justification='right'), LEDIndicator('_ain_')],
#     [sg.Multiline('128x32 MULTILINE TEXT display', size=(None, 4),
#                   font='Helvetica 14', k='_disp_', no_scrollbar=True)],
# ]

# txt = demo(canvas)
# convert_to_xbm()

def demo(canvas):
    cir = canvas.create_oval(50, 50, 100, 100)

    canvas.create_text((0, 0,),  anchor='nw', text=oled.latest_text, font=('Helvetica', 14), fill='DarkKhaki') # must have fill, and anchor='nw' helps position text
    canvas.create_text(50, 50, text='Hi', fill='black', font=('Helvetica', 24))
    txt = canvas.create_text(10, 100, text=oled.latest_text, anchor='nw', font=('Courier', 50), fill='blue') # font='TkMenuFont'
    
    lin = canvas.create_line(10, 10, 200, 50, 90, 150, 50, 80, arrow='last', fill='green')  # must have fill
    rect = canvas.create_rectangle(120, 10, 200, 50, fill='burlywood1', outline='blue')
    return txt

def demo2(canvas):
    # drawOnDisplay(window)
    # colour = 'red' if i % 2 == 0 else 'green'
    # canvas.itemconfig(cir, fill=colour)
    # canvas.itemconfig(txt, text=f'ABCDEFG {i}')
    # canvas.itemconfig(txt, text=f'ABCDEFG {oled.latest_text} {i}')
    # canvas.itemconfig(txt, angle=90)
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

    # img2 = sg.tkinter.BitmapImage(data=BITMAP) # works
    # canvas.create_bitmap(130, 20, bitmap=img2, foreground='red') # CRASH
    # canvas.create_image(130, 20, image=img2, foreground='red') # CRASH

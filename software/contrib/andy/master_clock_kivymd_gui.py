import time
from io import BytesIO
from PIL import Image, ImageOps
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image as kiImage
from kivy.graphics.context_instructions import Color 
from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from europi import FrameBuffer, MONO_HLSB

KV = '''
#:set leds dp(20)
<CanvasCvIn>:
    canvas:
        Color:
            rgb: .3, .7, .2
        Ellipse:
            pos: self.center_x, self.center_y - leds/2
            size: leds, leds
<CanvasLed>:
    canvas:
        Color:
            rgb: 1, 0, 0
        Ellipse:
            pos: self.center_x, self.center_y - leds/2
            size: leds, leds            
<Display>:
    canvas:
        Color:
            rgb: 1, 1, 1  # white
        Rectangle:
            pos: self.pos
            size: self.size
MDScreen:
    md_bg_color: get_color_from_hex('2F4F4F')
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint: 1, 0.5
            orientation: 'horizontal'
            CanvasCvIn:
            CanvasCvIn:
        BoxLayout:
            # padding: '100dp', '50dp'
            size_hint: 0.8, 0.2
            pos_hint: {'center_x':0.5}
            Display:
                id: disp
        BoxLayout:
            orientation: 'horizontal'
            padding: '10dp', '20dp'
            spacing: '20dp'
            MDSlider:
                min: 1
                max: 65535
                value: 50
                hint: True
                hint_bg_color: "red"
                hint_text_color: "white"
                hint_radius: [6, 0, 6, 0]
                on_value: print(f'Slider value is {int(self.value)}')
            MDSlider:
                min: 1
                max: 65535
                value: 50
                hint: True
                hint_bg_color: "red"
                hint_text_color: "white"
                hint_radius: [6, 0, 6, 0]
                on_value: app.on_slider_value(self)            
        MDBoxLayout:
            orientation: "horizontal"
            pos_hint: {'center_x':0.5}
            adaptive_width: True
            adaptive_height: True
            spacing: 20
            MDRoundFlatButton:
                text: 'b1'
                md_bg_color: get_color_from_hex('008B8B')
                line_color: get_color_from_hex('008B8B')
                text_color: get_color_from_hex('FFFFFF')
                on_press: print('b1 pressed')
                on_release: print('b1 released')
            MDRoundFlatButton:
                text: 'b2'
                md_bg_color: get_color_from_hex('008B8B')
                line_color: get_color_from_hex('008B8B')
                text_color: get_color_from_hex('FFFFFF')
                on_press: print('b2 pressed')
                on_release: print('b2 released')
        GridLayout:
            cols: 3
            rows: 2
            CanvasLed:
            CanvasLed:
            CanvasLed:
            CanvasLed:
            CanvasLed:
            CanvasLed:
        MDBoxLayout:
            orientation: 'horizontal'
            padding: '30dp', '20dp'
            spacing: '20dp'
            MDWidget:
            MDRaisedButton:
                text: 'Exit'
                on_press:
                    app.stop()
            MDWidget:
            MDRaisedButton:
                text: 'Draw Logo'
                on_press: app.root.ids.disp.drawLogo()
            MDWidget:
            MDRaisedButton:
                text: 'Clear Display'
                on_press:
                    print('The button was pressed')
                    on_press: app.root.ids.disp.clear()
                on_release:
                    print('The button was released')
            MDWidget:

'''

class CanvasCvIn(MDWidget):
    pass

class CanvasLed(MDWidget):
    pass

class Display(MDWidget):
    def clear(self):
        # self.canvas.clear()  # this clears but breaks future drawing? (in KivyMD only)

        # workaround
        texture = Texture.create(size=(128, 32))
        size = 128 * 32 * 3
        buf = [255 for x in range(size)]
        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=(128, 32))

    def drawLogo(self):
        image = b"\x00\x00\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x04\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc4\x04\x00\x18\x00\x00\x00p\x07\x00\x00\x00\x00\x00\x00\x0c$\x02\x00~\x0c\x18\xb9\x8c8\xc3\x00\x00\x00\x00\x00\x10\x14\x01\x00\xc3\x0c\x18\xc3\x060c\x00\x00\x00\x00\x00\x10\x0b\xc0\x80\x81\x8c\x18\xc2\x020#\x00\x00\x00\x00\x00 \x04\x00\x81\x81\x8c\x18\x82\x02 #\x00\x00\x00\x00\x00A\x8a|\x81\xff\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00FJC\xc1\x80\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00H\x898\x00\x80\x0c\x18\x83\x060c\x00\x00\x00\x00\x00S\x08\x87\x00\xc3\x060\x81\x8c8\xc3\x00\x00\x00\x00\x00d\x08\x00\xc0<\x01\xc0\x80p7\x03\x00\x00\x00\x00\x00X\x08p \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00#\x88H \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00L\xb8& \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x91P\x11 \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\xa6\x91\x08\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc9\x12\x84`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x12C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x11 \x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00H\x0c\x90\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x12\x88\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x12F\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04@@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        TH = bytearray(image)
        fb = FrameBuffer(TH, 128, 32, MONO_HLSB)
        # oled.blit(fb, 0, 0)

        filename = 'software/contrib/andy/temp.xbm'
        convert_to_xbm(fb, filename)

        # importing image class from PIL package
        # creating image object
        image = Image.open(filename)
        print(image, type(image), image.size, image.mode)
        # convert to rgb
        image_rgb = image.convert('RGB')
        image_rgb = ImageOps.invert(image_rgb)
        # print(image_rgb, type(image_rgb), image_rgb.size, image_rgb.mode)

        # canvas_img = Image.new('RGB', (240, 120), color=(255, 255, 255))
        # (do stuff to canvas_img)
        data = BytesIO()
        image_rgb.save(data, format='png')
        data.seek(0) # yes you actually need this
        im = CoreImage(BytesIO(data.read()), ext='png')
        # self.beeld = kiImage() # only use this line in first code instance
        # self.beeld.texture = im.texture       
        texture = im.texture
        # texture.flip_vertical()  # not necessary, but does work
        with self.canvas:
            # Color(1,1,1,1) # doesn't seem necessary
            pos = self.pos
            # pos = (pos[0] + 5, pos[1] + 5)
            Rectangle(texture=texture, pos=pos, size=(128, 32))

        # Drawing text

        mylabel = CoreLabel(text="Simulator", font_size=11, color=(0, 0, 0, 1))
        # Force refresh to compute things and generate the texture
        mylabel.refresh()
        # Get the texture and the texture size
        texture = mylabel.texture
        texture_size = list(texture.size)
        # Draw the texture on any widget canvas
        # myWidget = self
        # myWidget.canvas.add(Rectangle(texture=texture, size=texture_size))
        with self.canvas:
            pos = self.pos
            pos = (pos[0] + 55, pos[1] + 2)
            Rectangle(texture=texture, pos=pos, size=texture_size)

# Util

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


class EuroApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_slider_value(self, widget):
        print(f'EuroApp Slider value is {int(widget.value)}')

    # def on_start(self):
    #     self.fps_monitor_start()

Window.size = (450, 700)
EuroApp().run()

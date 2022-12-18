from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window

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
                # on_touch_down: self.draw()
                on_touch_down: self.drawLogo()
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
                    exit()
            MDWidget:
            MDRaisedButton:
                text: 'test1'
            MDWidget:
            MDRaisedButton:
                text: 'test2'
                # pos_hint: {"center_x": 0.5}
                on_press:
                    # label.text = 'The button was pressed'
                    print('The button was pressed')
                on_release:
                    # label.text = 'The button was released'
                    print('The button was released')
            MDWidget:

'''

class CanvasCvIn(MDWidget):
    pass

class CanvasLed(MDWidget):
    pass

class Display(MDWidget):
    def draw(self):
        # create a 64x64 texture, defaults to rgba / ubyte
        texture = Texture.create(size=(64, 64))

        # create 64x64 rgb tab, and fill with values from 0 to 255
        # we'll have a gradient from black to white
        size = 64 * 64 * 3
        buf = [int(x * 255 / size) for x in range(size)]

        # then, convert the array to a ubyte string
        buf = bytes(buf)

        # then blit the buffer
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

        # that's all ! you can use it in your graphics now :)
        # if self is a widget, you can do this
        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=(64, 64))

    def drawLogo(self):
        image = b"\x00\x00\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x04\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc4\x04\x00\x18\x00\x00\x00p\x07\x00\x00\x00\x00\x00\x00\x0c$\x02\x00~\x0c\x18\xb9\x8c8\xc3\x00\x00\x00\x00\x00\x10\x14\x01\x00\xc3\x0c\x18\xc3\x060c\x00\x00\x00\x00\x00\x10\x0b\xc0\x80\x81\x8c\x18\xc2\x020#\x00\x00\x00\x00\x00 \x04\x00\x81\x81\x8c\x18\x82\x02 #\x00\x00\x00\x00\x00A\x8a|\x81\xff\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00FJC\xc1\x80\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00H\x898\x00\x80\x0c\x18\x83\x060c\x00\x00\x00\x00\x00S\x08\x87\x00\xc3\x060\x81\x8c8\xc3\x00\x00\x00\x00\x00d\x08\x00\xc0<\x01\xc0\x80p7\x03\x00\x00\x00\x00\x00X\x08p \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00#\x88H \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00L\xb8& \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x91P\x11 \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\xa6\x91\x08\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc9\x12\x84`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x12C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x11 \x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00H\x0c\x90\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x12\x88\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x12F\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04@@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        TH = bytearray(image)
        # fb = FrameBuffer(TH, 128, 32, MONO_HLSB)
        # oled.blit(fb, 0, 0)

        # Experimental code
        texture = Texture.create(size=(128, 32))
        size = 128 * 32 * 3
        buf = [int(x * 255 / size) for x in range(size)]
        print(buf)
        buf = bytes(buf)
        print(len(image), len(buf))
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=(128, 32))

        # Drawing text

        mylabel = CoreLabel(text="Hi there!", font_size=12, color=(0, 0, 0, 1))
        # Force refresh to compute things and generate the texture
        mylabel.refresh()
        # Get the texture and the texture size
        texture = mylabel.texture
        texture_size = list(texture.size)
        # Draw the texture on any widget canvas
        # myWidget = self
        # myWidget.canvas.add(Rectangle(texture=texture, size=texture_size))
        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=texture_size)


class EuroApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_slider_value(self, widget):
        print(f'EuroApp Slider value is {int(widget.value)}')

    # def on_start(self):
    #     self.fps_monitor_start()

Window.size = (350, 700)
EuroApp().run()

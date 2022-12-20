from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window

KV = '''
<Display>:
    canvas:
        Color:
            rgb: 1, 1, 1  # white
        Rectangle:
            pos: self.pos
            size: self.size
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint: 0.8, 0.2
        pos_hint: {'center_x':0.5}
        Display:
            id: disp
            # on_touch_down: self.draw()
            on_touch_down: self.drawLogo()
    Button:
        text: 'Draw Logo'
        on_release: app.root.ids.disp.drawLogo()
        # size_hint: 0.2, 0.1
        pos_hint: {'center_x':0.5}
    Button:
        text: 'Clear'
        on_release: app.root.ids.disp.clear()
        # pos_hint: {'center_x':0.5}
    Button:
        text: 'Draw Gradient'
        on_release: app.root.ids.disp.drawGradient()
        # size_hint: 0.2, 0.1
        pos_hint: {'center_x':0.5}
    Button:
        text: 'Exit'
        on_release: app.stop()
        # size_hint: 0.2, 0.1
        pos_hint: {'center_x':0.5}
'''

class Display(Widget):
    def clear(self):
        self.canvas.clear()  # this clears but breaks future drawing?

        # texture = Texture.create(size=(128, 32))
        # size = 128 * 32 * 3
        # buf = [255 for x in range(size)]
        # buf = bytes(buf)
        # texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        # with self.canvas:
        #     Rectangle(texture=texture, pos=self.pos, size=(128, 32))

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


    def drawGradient(self):
        # Experimental code
        texture = Texture.create(size=(128, 32))
        size = 128 * 32 * 3
        buf = [int(x * 255 / size) for x in range(size)]
        print(buf)
        buf = bytes(buf)
        # print(len(image), len(buf))
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=(128, 32))

    def drawLogo(self):
        image = b"\x00\x00\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x04\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc4\x04\x00\x18\x00\x00\x00p\x07\x00\x00\x00\x00\x00\x00\x0c$\x02\x00~\x0c\x18\xb9\x8c8\xc3\x00\x00\x00\x00\x00\x10\x14\x01\x00\xc3\x0c\x18\xc3\x060c\x00\x00\x00\x00\x00\x10\x0b\xc0\x80\x81\x8c\x18\xc2\x020#\x00\x00\x00\x00\x00 \x04\x00\x81\x81\x8c\x18\x82\x02 #\x00\x00\x00\x00\x00A\x8a|\x81\xff\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00FJC\xc1\x80\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00H\x898\x00\x80\x0c\x18\x83\x060c\x00\x00\x00\x00\x00S\x08\x87\x00\xc3\x060\x81\x8c8\xc3\x00\x00\x00\x00\x00d\x08\x00\xc0<\x01\xc0\x80p7\x03\x00\x00\x00\x00\x00X\x08p \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00#\x88H \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00L\xb8& \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x91P\x11 \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\xa6\x91\x08\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc9\x12\x84`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x12C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x11 \x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00H\x0c\x90\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x12\x88\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x12F\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04@@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        TH = bytearray(image)
        # fb = FrameBuffer(TH, 128, 32, MONO_HLSB)
        # oled.blit(fb, 0, 0)

        # time.sleep(1)
        
        """
        I'm trying to draw a 128x32 texture on a widget canvas. I have a 128x32
        logo in a bytearray which is in mono (.xbm) format and need to translate
        it properly. 

        ```
        image = b"\x00\x00\x00\x01\xf0\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x02\x08\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x04\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xc4\x04\x00\x18\x00\x00\x00p\x07\x00\x00\x00\x00\x00\x00\x0c$\x02\x00~\x0c\x18\xb9\x8c8\xc3\x00\x00\x00\x00\x00\x10\x14\x01\x00\xc3\x0c\x18\xc3\x060c\x00\x00\x00\x00\x00\x10\x0b\xc0\x80\x81\x8c\x18\xc2\x020#\x00\x00\x00\x00\x00 \x04\x00\x81\x81\x8c\x18\x82\x02 #\x00\x00\x00\x00\x00A\x8a|\x81\xff\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00FJC\xc1\x80\x0c\x18\x82\x02 #\x00\x00\x00\x00\x00H\x898\x00\x80\x0c\x18\x83\x060c\x00\x00\x00\x00\x00S\x08\x87\x00\xc3\x060\x81\x8c8\xc3\x00\x00\x00\x00\x00d\x08\x00\xc0<\x01\xc0\x80p7\x03\x00\x00\x00\x00\x00X\x08p \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00#\x88H \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00L\xb8& \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\x91P\x11 \x00\x00\x00\x00\x000\x00\x00\x00\x00\x00\x00\xa6\x91\x08\xa0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc9\x12\x84`\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x12C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\x11 \x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00H\x0c\x90\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x12\x88\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x12F\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x10A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08  \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04@@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x008\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        TH = bytearray(image)
        ```
        
        XBM image data consists of a line of pixel values stored in a static
        array. Because a single bit represents each pixel (0 for white or 1 for
        black), each byte in the array contains the information for eight
        pixels, with the upper left pixel in the bitmap represented by the low
        bit of the first byte in the array. 
        """


        # importing image class from PIL package
        from PIL import Image, ImageOps
        # creating image object
        image = Image.open('software/contrib/andy/temp.xbm')
        print(image, type(image), image.size, image.mode)
        # convert to rgb
        image_rgb = image.convert('RGB')
        image_rgb = ImageOps.invert(image_rgb)
        print(image_rgb, type(image_rgb), image_rgb.size, image_rgb.mode)
        from kivy.core.image import Image as CoreImage
        from kivy.uix.image import Image as kiImage
        from kivy.graphics.context_instructions import Color 
        from io import BytesIO

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

class EuroApp(App):
    def build(self):
        return Builder.load_string(KV)

Window.size = (350, 700)
EuroApp().run()

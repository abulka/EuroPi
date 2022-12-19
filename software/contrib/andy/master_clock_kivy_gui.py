'''Example shows the recommended way of how to run Kivy with the Python built
in asyncio event loop as just another async coroutine.
'''
import asyncio
from PIL import Image, ImageOps
from io import BytesIO
from kivy.app import async_runTouchApp
from kivy.lang.builder import Builder
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg, oled, bootsplash, b1, b2, din, k1, k2
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage
from kivy.core.text import Label as CoreLabel
from kivy.graphics.context_instructions import Color 
from kivy.properties import StringProperty
from kivy.clock import Clock
from europi_simulator_util import convert_to_xbm
from europi import FrameBuffer, MONO_HLSB

kv = '''
# MainThing:
EuroPiLayout:

#:set leds dp(20)
<CanvasCvIn>:
    canvas:
        Color:
            rgb: .3, .7, .2
        Ellipse:
            pos: self.center_x, self.center_y - leds/2
            size: leds, leds
<CanvasLed>:
    state: 'off'
    canvas:
        Color:
            rgb: (0,1,0) if self.state == 'off' else (1,0,0)
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
<EuroPiLayout>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgb: .14, .14, .14
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        size_hint: 1, 0.5
        orientation: 'horizontal'
        CanvasCvIn:
        CanvasCvIn:
    BoxLayout:
        size_hint: 0.8, 0.5
        pos_hint: {'center_x':0.5}
        Display:
            id: disp
            # on_touch_down:
            #     print(id)
            #     # self.clear()
            #     self.drawLogo()
    BoxLayout:
        orientation: 'horizontal'
        padding: '30dp', '20dp'
        spacing: '20dp'
        Slider:
            min: 0
            max: 100
            value: 50
            on_value: root.on_slider_value(self)
        Slider:
            min: 0
            max: 100
            value: 50
            on_value: root.on_slider_value(self)
    BoxLayout:
        size_hint: 1, 0.5
        padding: '130dp', '0dp'
        spacing: '20dp'
        # orientation: 'horizontal' # this breaks the buttons?
        Button:
            text: 'b1'
        Button:
            text: 'b2'
    GridLayout:
        cols: 3
        rows: 2
        CanvasLed:
            id: cv1
            state: 'off'
        CanvasLed:
            id: cv2
        CanvasLed:
            id: cv3
        CanvasLed:
            id: cv4
        CanvasLed:
            id: cv5
        CanvasLed:
            id: cv6
            state: 'on'
    DebugArea:
<DebugArea>:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            padding: '30dp', '20dp'
            spacing: '20dp'
            Button:
                text: 'Exit'
                on_press:
                    # app.stop()
                    exit()
            Button:
                text: 'Draw Logo'
                on_press: root.parent.ids.disp.drawLogo()
            Button:
                text: 'Clear Display'
                on_press:
                    on_press: root.parent.ids.disp.clear()
            Button:
                text: 'LED'
                on_press:
                    cv1 = root.parent.ids.cv1
                    # print('LED', cv1.state)
                    # cv1.set_state('on')
                    cv1.toggle_state()
            Button:
                text: 'DUMP'
                on_press:
                    # label.text = 'The button was pressed'
                    # print('app', app) # CRASH
                    # print('app.root', app.root) # CRASH
                    print('root.parent', root.parent)
                    print('root.parent.ids', root.parent.ids)
                    print('root.ids', root.ids)
                    print('self.ids', self.ids)
                    print('self.parent.ids', self.parent.ids)
                on_release:
                    # label.text = 'The button was released'
                    print('The button was released')
            Button:
                id: btn
                text: 'Press me'
        BoxLayout:
            Label:
                id: label
                text: 'Button is "{}"'.format(btn.state)
'''

class EuroPiLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(EuroPiLayout, self).__init__(**kwargs)
        Clock.schedule_interval(self.custom_update, 0.2) # run method every t

    def custom_update(self, dt):
        # print('custom_update:', self, self.ids['cv1'])
        # self.ids['cv1'].toggle_state()
        self.update_leds()

    def update_leds(self):
        # make a copy since master clock is updating it
        cvs_snapshot = [1 if value !=
                        0 else 0 for value in mc.cvs_snapshot]
        # window['_cvs_'].update(f'{cvs_snapshot}')
        # window['_cvs-msg_'].update(f'{get_cvs_snapshot_msg()}')
        for index, val in enumerate(cvs_snapshot):
            ref = f'cv{index+1}'
            self.ids[ref].set_state('on' if val != 0 else 'off')


    def on_slider_value(self, widget):
        print(f'Slider value is {int(widget.value)}')


class DebugArea(BoxLayout):
    pass

class CanvasLed(Widget):
    state = StringProperty()

    def __init__(self, **kwargs):
        super(CanvasLed, self).__init__(**kwargs)
        Clock.schedule_once(self.after_init) # run method on next frame

    def after_init(self, dt):
        print('after_init LED:', self.state)  # dt might be the time since last frame or something

    def set_state(self, value):
        # toggle state
        # print('LED: set_state from', self.state, '->', value)
        self.state = value

    def toggle_state(self):
        self.state = 'on' if self.state == 'off' else 'off'

class CanvasCvIn(Widget):
    pass

class Display(Widget):
    def clear(self):
        with self.canvas:
            Color(rgba=(1,1,1,1))
            Rectangle(pos=self.pos, size=(128, 32))

        # Clear tequnique 2 - not used
        # self.canvas.after.clear()

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

        # Clear tequnique 2 - not used
        # with self.canvas.after:    # add '.after' (but not .before)
        #     Rectangle(texture=texture, pos=self.pos, size=(128, 32))

async def run_app_happily(root, other_task):
    '''This method, which runs Kivy, is run by the asyncio loop as one of the
    coroutines.
    '''
    # we don't actually need to set asyncio as the lib because it is the
    # default, but it doesn't hurt to be explicit
    await async_runTouchApp(root, async_lib='asyncio')  # run Kivy
    print('App done')
    # now cancel all the other tasks that may be running
    other_task.cancel()


async def waste_time_freely():
    '''This method is also run by the asyncio loop and periodically prints
    something.
    '''
    try:
        while True:
            print('Sitting on the beach')
            await asyncio.sleep(2)
    except asyncio.CancelledError as e:
        print('Wasting time was canceled', e)
    finally:
        # when canceled, print that it finished
        print('Done wasting time')

if __name__ == '__main__':
    mc = MasterClockInner()

    def root_func():
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        root = Builder.load_string(kv)  # root widget
        # other_task = asyncio.ensure_future(waste_time_freely())
        other_task = asyncio.ensure_future(mc.main())

        return asyncio.gather(run_app_happily(root, other_task), other_task)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(root_func())
    except asyncio.CancelledError as e:
        print('Wasting time was canceled', e)
    loop.close()

'''Example shows the recommended way of how to run Kivy with the Python built
in asyncio event loop as just another async coroutine.
'''
import asyncio
import random
import time
from PIL import Image, ImageOps
from io import BytesIO
from kivy.app import async_runTouchApp
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage
from kivy.core.text import Label as CoreLabel
from kivy.graphics.context_instructions import Color 
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from master_clock import MasterClockInner
from europi import cvs, oled, bootsplash, b1, b2, din, k1, k2
from europi import FrameBuffer, MONO_HLSB
from europi_simulator_util import convert_to_xbm
from europi_simulator_util import get_cvs_snapshot_msg, get_cvs_snapshot

kv = '''
# MainThing:
EuroPiLayout:

# giving colour to label
<CustLabel@Label>:
    color: 'grey'

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
            id: k1
            min: 1
            max: 65535
            value: 50
            on_value: root.on_slider_value_k1(self)
        Slider:
            id: k2
            min: 1
            max: 65535
            value: 50
            on_value: root.on_slider_value_k2(self)
    BoxLayout:
        size_hint: 1, 0.5
        padding: '130dp', '0dp'
        spacing: '20dp'
        # orientation: 'horizontal' # this breaks the buttons?
        Button:
            text: 'b1'
            on_press: root.on_button_press_b1(self)
            on_release: root.on_button_release_b1(self)
        Button:
            text: 'b2'
            on_press: root.on_button_press_b2(self)
            on_release: root.on_button_release_b2(self)
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
                orientation: 'vertical'
                size_hint: 0.5, 1.5
                CustLabel:
                    text: "Sounds"
                CheckBox:
                    canvas.before:
                        Color:
                            rgb: 0.5, 0.5, 0.5
                        Rectangle:
                            pos:self.center_x-8, self.center_y-8
                            size:[16,16]
                        Color:
                            rgb: 0,0,0
                        Rectangle:
                            pos:self.center_x-7, self.center_y-7
                            size:[14,14]
                    active: False
                    on_active: root.parent.on_checkbox_click(self)
        BoxLayout:
            Label:
                id: label
                text: 'Button is "{}"'.format(btn.state)
'''

sound1 = SoundLoader.load('sounds/wav1.wav')
sound2 = SoundLoader.load('sounds/wav2.wav')
sound3 = SoundLoader.load('sounds/wav3.wav')
sound4 = SoundLoader.load('sounds/wav4.wav')
sound5 = SoundLoader.load('sounds/wav1.wav')
sound6 = SoundLoader.load('sounds/wav2.wav')

class EuroPiLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(EuroPiLayout, self).__init__(**kwargs)

        b1.pin.value(1) # reverse pin logic high/low/pull stuff
        b2.pin.value(1) # reverse pin logic high/low/pull stuff
        self.play_sounds = False
        Clock.schedule_interval(self.custom_update, .1) # run method every t

    def custom_update(self, dt):
        # print('custom_update:', self, self.ids['cv1'])
        # self.ids['cv1'].toggle_state()
        self.update_leds()
        
        display_widget = self.ids['disp']

        # x = random.randint(0, 100)
        # y = random.randint(0, 20)
        # display_widget.blah('fred', x, y)

        display_widget.update_display()


    def update_leds(self):
        # make a copy since master clock is updating it
        cvs_snapshot = [1 if value !=
                        # 0 else 0 for value in mc.cvs_snapshot]
                        0 else 0 for value in get_cvs_snapshot()]
        # window['_cvs_'].update(f'{cvs_snapshot}')
        # window['_cvs-msg_'].update(f'{get_cvs_snapshot_msg()}')
        for index, val in enumerate(cvs_snapshot):
            ref = f'cv{index+1}'
            new_state = 'on' if val != 0 else 'off'
            self.ids[ref].set_state(new_state)
            if (new_state == 'on' and self.play_sounds):
                if (ref == 'cv1'):
                    # sound1.play()
                    pass
                elif (ref == 'cv2'):
                    sound2.play()
                elif (ref == 'cv3'):
                    sound3.play()
                elif (ref == 'cv4'):
                    sound4.play()
                elif (ref == 'cv5'):
                    sound5.play()
                elif (ref == 'cv6'):
                    sound6.play()

    def on_checkbox_click(self, widget):
        print(f'Checkbox value is {widget.active}')
        self.play_sounds = widget.active

    def on_slider_value_k1(self, widget):
        # print(f'Slider value is {int(widget.value)}')
        k1.pin._pin._value = int(widget.value)

    def on_slider_value_k2(self, widget):
        # print(f'Slider value is {int(widget.value)}')
        k2.pin._pin._value = int(widget.value)

    def on_button_press_b1(self, widget):
        print('b1 down')
        b1.pin.value(0)
        b1.fake_debounce()

    def on_button_release_b1(self, widget):
        print('b1 up')
        b1.pin.value(1)
        b1.fake_debounce()
        b1._falling_handler()

    def on_button_press_b2(self, widget):
        print('b2 down')
        b2.pin.value(0)
        b2.fake_debounce()

    def on_button_release_b2(self, widget):
        print('b2 up')
        b2.pin.value(1)
        b2.fake_debounce()
        b2._falling_handler()

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
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.cmd_last = []

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

        self.image_out(fb)

        self.text_out('Simulator', 55, 2)

    def image_out(self, fb):
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

        # Clear technique 2 - not used
        # with self.canvas.after:    # add '.after' (but not .before)
        #     Rectangle(texture=texture, pos=self.pos, size=(128, 32))

    def text_out(self, text, x, y, colour=None):
        mylabel = CoreLabel(text=text, font_size=10, color=(0, 0, 0, 1))
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
            pos = (pos[0] + x, pos[1] + (32 - y) - 10)
            Rectangle(texture=texture, pos=pos, size=texture_size)

    def update_display(self):
        if (len(oled.commands) > 1_000):
            raise Exception(f'Too many commands {len(oled.commands)}')

        if not oled.flush_to_ui:
            return
        
        cmds = oled.commands.copy()
        if cmds != self.cmd_last:
            # print('************************** update_display', len(cmds), 'commands')
            for cmd in cmds:
                command = cmd[0]
                params = cmd[1]
                if command == 'text':
                    text, x, y, colour = params
                    font_size = 14
                    fill = 'black'
                    if colour == 88:
                        fill = 'green'
                        font_size = 12
                    # print('text', text, x, y, colour)
                    # break # calling the next line causes the async problem
                    self.text_out(text, x, y)
                elif command == 'fill':
                    value = params[0]
                    if value == 0:
                        self.clear()
                elif command == 'blit':
                    frame_buffer, x, y = params
                    self.image_out(frame_buffer)
                    filename = 'software/contrib/andy/temp.xbm'
                    convert_to_xbm(frame_buffer, filename)
                else:
                    print('unknown command', command)
        else:
            pass
            # print('Display - No change')

        self.cmd_last = cmds.copy()
        oled.commands = []
        oled.flush_to_ui = False

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

async def heartbeat():
    while True:
        start = time.time()
        await asyncio.sleep(1)
        delay = time.time() - start - 1
        # print(f'heartbeat delay = {delay:.3f}s')

if __name__ == '__main__':
    mc = MasterClockInner()

    def root_func():
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        root = Builder.load_string(kv)  # root widget
        # other_task = asyncio.ensure_future(waste_time_freely())
        other_task = asyncio.ensure_future(mc.main())
        heartbeat_task = asyncio.ensure_future(heartbeat())

        # return asyncio.gather(run_app_happily(root, other_task), other_task)
        return asyncio.gather(run_app_happily(root, other_task), other_task, heartbeat_task)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(root_func())
    except asyncio.CancelledError as e:
        print('Wasting time was canceled', e)
    loop.close()

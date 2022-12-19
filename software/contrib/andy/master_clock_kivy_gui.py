'''Example shows the recommended way of how to run Kivy with the Python built
in asyncio event loop as just another async coroutine.
'''
import asyncio

from kivy.app import async_runTouchApp
from kivy.lang.builder import Builder
from master_clock import MasterClockInner
from europi import cvs, get_cvs_snapshot_msg, oled, bootsplash, b1, b2, din, k1, k2
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

kv = '''
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
        size_hint: 0.8, 0.2
        pos_hint: {'center_x':0.5}
        Display:
            id: disp
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
        CanvasLed:
        CanvasLed:
        CanvasLed:
        CanvasLed:
        CanvasLed:            
BoxLayout:
    orientation: 'vertical'
    EuroPiLayout:
        size_hint: 1, 5

    # Debug Area
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
            # on_press: app.root.ids.disp.drawLogo()
        Button:
            text: 'Clear Display'
            on_press:
                on_press: app.root.ids.disp.clear()
        Button:
            text: 'test2'
            on_press:
                # label.text = 'The button was pressed'
                print('The button was pressed')
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
    def on_slider_value(self, widget):
        print(f'Slider value is {int(widget.value)}')

class CanvasLed(Widget):
    pass

class CanvasCvIn(Widget):
    pass

class Display(Widget):
    def clear(self):
        self.canvas.clear()

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
    def root_func():
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        root = Builder.load_string(kv)  # root widget
        # other_task = asyncio.ensure_future(waste_time_freely())
        mc = MasterClockInner()
        other_task = asyncio.ensure_future(mc.main())

        return asyncio.gather(run_app_happily(root, other_task), other_task)

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(root_func())
    except asyncio.CancelledError as e:
        print('Wasting time was canceled', e)
    loop.close()

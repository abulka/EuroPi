from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget

KV = '''
#:set leds dp(20)
<CanvasCvIn>:
    canvas:
        Color:
            rgb: 0, 0, 1
        Ellipse:
            # pos: self.pos
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
            rgb: 0, 1, 0 # green
            # rgb: 1, 1, 1 # white
        Rectangle:
            pos: self.pos
            size: self.size
MDScreen:
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            CanvasCvIn:
            CanvasCvIn:
        BoxLayout:
            padding: '130dp', '0dp'
            Display:
        BoxLayout:
            orientation: 'horizontal'
            padding: '30dp', '20dp'
            spacing: '20dp'
            MDSlider:
                min: 0
                max: 100
                value: 50
                hint: True
                hint_bg_color: "red"
                hint_text_color: "white"
                hint_radius: [6, 0, 6, 0]
                on_value: print(f'Slider value is {int(self.value)}')
            MDSlider:
                min: 0
                max: 100
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
                md_bg_color: get_color_from_hex('404040')
                line_color: get_color_from_hex('404040')
                text_color: get_color_from_hex('FFFFFF')

            MDRoundFlatButton:
                text: 'b2'
                md_bg_color: get_color_from_hex('404040')
                line_color: get_color_from_hex('404040')
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
'''

class CanvasCvIn(MDWidget):
    pass

class CanvasLed(MDWidget):
    pass

class Display(MDWidget):
    pass

class EuroApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_slider_value(self, widget):
        print(f'EuroApp Slider value is {int(widget.value)}')

    # def on_start(self):
    #     self.fps_monitor_start()


EuroApp().run()

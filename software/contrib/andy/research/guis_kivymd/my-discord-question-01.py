from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'horizontal'
        padding: '30dp', '20dp'
        spacing: '20dp'
        MDRaisedButton:
            text: 'Exit'
            # pos_hint: {"center_x": 0.5}
        MDRaisedButton:
            text: 'test1'
        MDRaisedButton:
            text: 'test2'
'''

class EuroApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_slider_value(self, widget):
        print(f'EuroApp Slider value is {int(widget.value)}')

EuroApp().run()

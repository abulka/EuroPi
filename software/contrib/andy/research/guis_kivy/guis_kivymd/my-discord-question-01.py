from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.widget import MDWidget

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'horizontal'
        padding: '30dp', '20dp'
        spacing: '20dp'
        MDWidget:                    # add this
        MDRaisedButton:
            text: 'Exit'
        MDWidget:                    # add this
        MDRaisedButton:
            text: 'test1'
        MDWidget:                    # add this
        MDRaisedButton:
            text: 'test2'
        MDWidget:                    # add this
'''
KVx='''
MDScreen:
    MDBoxLayout:
        orientation: 'horizontal'
        padding: '30dp', '20dp'
        spacing: '20dp'
        # md_bg_color: 'gray'        # to see size
        MDBoxLayout:
            MDFloatLayout:    
                MDRaisedButton:
                    text: 'Exit'
                    pos_hint: {"center_x": 0.5, 'center_y': .5}
        MDBoxLayout:
            MDFloatLayout:
                MDRaisedButton:
                    text: 'test1'
                    pos_hint: {"center_x": 0.5, 'center_y': .5}
        MDBoxLayout:
            MDFloatLayout:
                MDRaisedButton:
                    text: 'test2'
                    pos_hint: {"center_x": 0.5, 'center_y': .5}
'''

class EuroApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_slider_value(self, widget):
        print(f'EuroApp Slider value is {int(widget.value)}')

EuroApp().run()

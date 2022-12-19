from kivy.app import App
from kivy.lang import Builder

kv = '''
#:import utils kivy.utils
<CustomWidget@RelativeLayout>:  # change base class to a Layout
    labelText: 'None'
    imageSource: ''
    
    updatedlabel:updatedlabel
    customimage:customimage
    
    background_color:(0,0,0,0)
    background_normal:''
    canvas.before:
        Color:
            rgba:(181/255,174/255,174/255,1)
        RoundedRectangle:
            size: self.size
            # pos: self.pos  # just use default of (0,0) because this is in a RelativeLayout
            radius:[28]
    GridLayout:
        rows: 2
        cols: 1
        Image:
            id:customimage
            source: root.imageSource
        Label:
            id:updatedlabel
            text: root.labelText
            size_hint_y: 0.25
            
FloatLayout:
    CustomWidget:
        pos_hint:{'x': 0.04, "top": 0.9}
        size_hint_x: 0.16
        size_hint_y: 0.3
        labelText: "I just wrote a text"
        imageSource: "round button/down.png"
'''

class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()

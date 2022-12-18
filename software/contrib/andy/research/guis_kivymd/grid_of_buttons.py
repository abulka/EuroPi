from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

KV = '''
Screen:
    name:'s'
    GridLayout:
        cols:3
        spacing:'1dp'
        id: grid
        
<RaisedButton>:
    size_hint_x: root.width
    size_hint_y: root.height
'''

class RaisedButton(MDRaisedButton):pass


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)
        
    def on_start(self):
        for i in range(12):
            self.root.ids.grid.add_widget(
        RaisedButton(text=f'{i}')
       
       )


Example().run()

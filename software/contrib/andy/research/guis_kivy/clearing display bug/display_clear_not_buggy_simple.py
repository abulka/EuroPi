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
        Display:
            id: disp
    Button:
        text: 'Draw Gradient'
        on_release: app.root.ids.disp.drawGradient()
        pos_hint: {'center_x':0.5}
    Button:
        text: 'Clear'
        on_release: app.root.ids.disp.clear()
'''

class Display(Widget):
    def clear(self):
        self.canvas.clear()  # this clears but breaks future drawing?

    def drawGradient(self):
        texture = Texture.create(size=(128, 32))
        size = 128 * 32 * 3
        buf = [int(x * 255 / size) for x in range(size)]
        print(buf)
        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=(128, 32))

class EuroApp(App):
    def build(self):
        return Builder.load_string(KV)

Window.size = (350, 200)
EuroApp().run()

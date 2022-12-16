# python '/Users/andy/.pyenv/versions/anaconda3-2022.05/envs/ldm/share/kivy-examples/widgets/colorpicker.py'  

from kivy.app import App
from kivy.uix.widget import Widget


class My(Widget):
    pass


class MyApp(App):
    def build(self):
        return My()


if __name__ == '__main__':
    MyApp().run()

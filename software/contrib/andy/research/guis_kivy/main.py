from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

class MainWidget(Widget):
    pass

class FredLayout(BoxLayout):
    pass

class EuroPiLayout(BoxLayout):
    def on_slider_value(self, widget):
        print(f'Slider value is {int(widget.value)}')

class CanvasExample(Widget):
    pass

class CanvasExample2(Widget):
    pass

class CanvasLed(Widget):
    pass

class TheLabApp(App):
    pass

TheLabApp().run()

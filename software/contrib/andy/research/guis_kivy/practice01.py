from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.core.window import Window
# Window.clearcolor = (1, 1, 1, 1)
Window.clearcolor = 'Red'

kv = '''
BoxLayout:
    # canvas.before:
    #     Color:
    #         rgba: 255, 255, 50, 1
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size
    orientation: 'vertical'
    padding: 50
    spacing: 100

    GridLayout:
        cols: 4
        padding: 50
        spacing: 20
        Label:
            text: 'Digital Input'
        CheckBox:
            id: 'din'
            height: '48dp'
            colour: 'red'
        Label:
            text: 'Analogue Input'
        CheckBox:
            id: 'ain'
            height: '48dp'
    # Canvas rectangle
    BoxLayout:
        orientation: 'horizontal'
        padding: 50
        spacing: 100        
        Slider:
            id: 'k1'
        Slider:
            id: 'k2'
    BoxLayout:
        orientation: 'horizontal'
        padding: 50
        spacing: 100        
        Button:
            text: 'b1'
        Button:
            text: 'b2'

    Label:
        text: 'Hello'+' World!'


'''

# kv = '''
# BoxLayout:
#     orientation: 'vertical'

#     Camera:
#         id: camera
#         resolution: 399, 299

#     BoxLayout:
#         orientation: 'horizontal'
#         size_hint_y: None
#         height: '48dp'
#         Button:
#             text: 'Start'
#             on_release: camera.play = True

#         Button:
#             text: 'Stop'
#             on_release: camera.play = False
# '''


class CameraApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    CameraApp().run()

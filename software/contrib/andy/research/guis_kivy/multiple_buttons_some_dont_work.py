from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder

kv = '''
BoxLayout:
    orientation: 'vertical'
    padding: 50
    spacing: 100

    Label:
        text: 'Hello'+' World!'        
    Button:
        text: 'Fred'
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        # height: '48dp'
        padding: 50
        spacing: 100        
        Button:
            text: 'Start'
            on_release: camera.play = True
            # padding: (100, 100)
            # margin: [300, 300]
        Button:
            text: 'Stop'
            on_release: camera.play = False
            # padding: [200, 200]
            # margin: [300, 300]
    GridLayout
        cols: 4
        size_hint_y: None
        height: self.minimum_height
        
        Button:
            padding: [50, 50]
            text: 'New User'
            size_hint_y: None
            height: self.texture_size[1]

        Button:
            text: 'Login'
            size_hint_y: None
            # height: self.texture_size[1]
            
        Button:
            text: 'Skip Login'
            size_hint_y: None
            # height: self.texture_size[1]
                
        Button:
            text: str(root.center_x)
            size_hint_y: None
            height: self.texture_size[1]        
<Label>
    text: 'Hello'+' World!AAAAAAAA'
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

# kv = '''
# BoxLayout:
#     size_hint: [.9, .9]
#     pos_hint: { 'top' : .95, 'right': .95}

#     # Add padding and spacing
#     orientation: 'vertical'
#     padding: 50
#     spacing: 100

#     canvas:
#         Color:
#             rgb: [.8, .8, .8]
#         Rectangle:
#             pos: self.pos
#             size: self.size

#     # Add New BoxLayout
#     BoxLayout:
#         canvas:
#             Color:
#                 rgb: [.6, .6, .6]
#             Rectangle:
#                 pos: self.pos
#                 size: self.size
#     BoxLayout:
#         canvas:
#             Color:
#                 rgb: [.6, .6, .6]
#             Rectangle:
#                 pos: self.pos
#                 size: self.size
# '''

class CameraApp(App):
    def build(self):
        return Builder.load_string(kv)


if __name__ == '__main__':
    CameraApp().run()

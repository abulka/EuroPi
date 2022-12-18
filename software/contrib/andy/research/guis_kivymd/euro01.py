from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
MDScreen:

    MDLabel:
        text: "Hello, World!"
        halign: "center"
'''

class Euro01App(MDApp):
    pass

# AHA IF YOU DON'T EXPLICITLY LOAD THE KV STRING THEN
# IT WILL BE LOADED FROM THE .kv FILE NAMED AFTER THE APP
# 
# class Euro01App(MDApp):
#     def build(self):
#         return Builder.load_string(KV)

#     def on_start(self):
#         self.fps_monitor_start()


Euro01App().run()

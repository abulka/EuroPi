# File name: main.py

import kivy
from kivy.app import App

# We're going to inherit from the Widget class, so we must import it first.
from kivy.uix.widget import Widget

# Here is the inheritance. 
class MyCustomWidget(Widget):
    # We're going to implement it in the kv file.
    pass

class Custom01App(App):
    def build(self):
        # Now we want our custom widget to be returned.
        return MyCustomWidget()

if __name__ == '__main__':
    Custom01App().run()

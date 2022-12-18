## Sample Python application demonstrating that
## how to create button corners round in kivy using .kv file
	
##################################################		
# import kivy module
import kivy

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require("1.9.1")

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# module consist the floatlayout
# to work with FloatLayout first
# you have to import it
from kivy.uix.floatlayout import FloatLayout

# creates the button in kivy
# if not imported shows the error
from kivy.uix.button import Button

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')
	
# to change the kivy default settings we use this module config
from kivy.config import Config
	
# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', True)

# creating the root widget used in .kv file
class Base(FloatLayout):
	pass

# class in which we are creating the imagebutton
# in .kv file to be named Btn.kv
class BtnApp(App):
	# defining build()
	def build(self):
		# returning the instance of root class
		return Base()

# run function runs the whole program
# i.e run() method which calls the target
# function passed to the constructor.
if __name__ == "__main__":
	BtnApp().run()

import asyncio
import random
import PySimpleGUI as sg  # pip install PySimpleGUI

# sg.theme_previewer()

# layout = [[sg.Text(text="This is a very basic PySimpleGUI layout")],
#           [sg.Input(), sg.Button()], [sg.Button(
#               button_text="Button", key="-ExampleKey-"),
#     sg.Button(button_text="Exit"), sg.ProgressBar(None),
#     sg.Button(), sg.Column([[sg.Slider()]])]]
# x = 1


import PySimpleGUI as sg

sg.theme('SystemDefaultForReal')
# ttk_style = 'default'
ttk_style = 'aqua'
layout = [[sg.T(ttk_style)],
          [sg.Text('ANCDEFG', size=(None, 1), font='Helvetica 24', k='_cvs_')],
          [sg.Button('Button 1', use_ttk_buttons=True), 
           sg.Button('Button 2', use_ttk_buttons=True)]  ]

window = sg.Window('Window Title', layout, ttk_theme=ttk_style).read(close=True)

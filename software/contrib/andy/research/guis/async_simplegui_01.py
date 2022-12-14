# Trying to integrate pysimplegui with asyncio
# https://stackoverflow.com/questions/70497095/implementing-asyncio-with-pysimplegui

import PySimpleGUI as sg
import asyncio
import time
from threading import Thread
import asyncio

# sg.theme('Light Blue 3')
# # This design pattern simulates button callbacks
# # This implementation uses a simple "Dispatch Dictionary" to store events and functions

# The callback functions
async def button1():
    print('Button 1 callback')
    return 'nothing'
    

def asyncloop(loop):
    # Set loop as the active event loop for this thread
    asyncio.set_event_loop(loop)
    # We will get our tasks from the main thread so just run an empty loop    
    loop.run_forever()

# create a new loop
loop = asyncio.new_event_loop()
# Create the new thread, giving loop as argument
t = Thread(target=asyncloop, args=(loop,))
# Start the thread
t.start()


# ORIGINAL

#  Lookup dictionary that maps button to function to call
# dispatch_dictionary = {'1':button1, '2':button2, '3':button3}
dispatch_dictionary = {'1':button1}

# Layout the design of the GUI
layout = [[sg.Text('Please click a button', auto_size_text=True)],
        [sg.Button('1'), sg.Button('2'), sg.Button('3'), sg.Quit()]]
# Show the Window to the user__TIMEOUT__
window = sg.Window('Button callback example', layout)
# Event loop. Read buttons, make callbacks
while True:
    # Read the Window
    event, values = window.read()
    if event in ('Quit', sg.WIN_CLOSED):
        break
    if event == '__TIMEOUT__':
        continue
    # Lookup event in function dictionary
    if event in dispatch_dictionary:
        func_to_call = dispatch_dictionary[event]   # get function from dispatch dictionary

        # Later in the button event code (in main thread):
        asyncio.run_coroutine_threadsafe(func_to_call(), loop)

        # print(asyncio.run(func_to_call()))
    else:
        print('Event {} not in dispatch dictionary'.format(event))

window.close()

# # stop thread t
# loop.stop()
# # Wait for thread to finish
# t.join()
# kill thread t
# stop thread t
loop.stop()
# t.kill()
# t.join()

# window.close()


# All done!
sg.popup_ok('Done')

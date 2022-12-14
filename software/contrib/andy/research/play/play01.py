# add stubs/ to sys.path
import sys
sys.path.append('stubs')

from europi import *
import machine

# from time import ticks_diff, ticks_ms  # ANDY
def ticks_diff(): return 0
def ticks_ms(): return 0

from europi_script import EuroPiScript

# ANDY
# try:
#     import uasyncio as asyncio
# except ImportError:
#     import asyncio
import asyncio

from random import randint

# outputs
cv1.on()
cv1.value(2.5)

# Pin test
pin = Pin(0, Pin.OUT)
pin.value(1)
pin_value = pin.value()
print('pin_value', pin_value)

# inputs
din_value = din.value()
ain_value = ain.read_voltage()
print('din_value', din_value, 'ain_value', ain_value)


print('done')
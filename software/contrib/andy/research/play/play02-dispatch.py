from multipledispatch import dispatch
 
# passing one parameter
 
 
@dispatch(int, int)
def product(first, second):
    result = first*second
    print(result)
 
# passing two parameters
 
 
@dispatch(int, int, int)
def product(first, second, third):
    result = first * second * third
    print(result)
 
# you can also pass data type of any value as per requirement
 
 
@dispatch(float, float, float)
def product(first, second, third):
    result = first * second * third
    print(result)
 
 
# calling product method with 2 arguments
product(2, 3)  # this will give output of 6
 
# calling product method with 3 arguments but all int
product(2, 3, 2)  # this will give output of 12
 
# calling product method with 3 arguments but all float
product(2.2, 3.4, 2.3)  # this will give output of 17.985999999999997

# ANDY
@dispatch()
def product():
    print('no arguments')
 
product()



# ANDY
from typing import overload, Union, Tuple, Optional, NoReturn, List, Callable
from typing import Sequence, ClassVar, Any

# @overload
@dispatch()
def value() -> int:
    """
    Get or set the digital logic level of the pin:

        - With no argument, return 0 or 1 depending on the logic level of the pin.
        - With ``value`` given, set the logic level of the pin.  ``value`` can be
        anything that converts to a boolean.  If it converts to ``True``, the pin
        is set high, otherwise it is set low.
    """
    return 88

# @overload
@dispatch(int)
# def value(self, value: Any, /) -> None:
def value(value: Any, /) -> None:
# def value(value: int) -> None:
    """
    Get or set the digital logic level of the pin:

        - With no argument, return 0 or 1 depending on the logic level of the pin.
        - With ``value`` given, set the logic level of the pin.  ``value`` can be
        anything that converts to a boolean.  If it converts to ``True``, the pin
        is set high, otherwise it is set low.
    """
    print('setting value', value)


value(1)
pin_value = value()
print('pin_value', pin_value)


# Try inside a class

class Pin:
    def __init__(self):
        print('init')
        self._value = 0

    @dispatch()
    def value(self) -> int:
        """
        Get or set the digital logic level of the pin:

            - With no argument, return 0 or 1 depending on the logic level of the pin.
            - With ``value`` given, set the logic level of the pin.  ``value`` can be
            anything that converts to a boolean.  If it converts to ``True``, the pin
            is set high, otherwise it is set low.
        """
        return self._value

    @dispatch(int)
    def value(self, value: Any, /) -> None:
        """
        Get or set the digital logic level of the pin:

            - With no argument, return 0 or 1 depending on the logic level of the pin.
            - With ``value`` given, set the logic level of the pin.  ``value`` can be
            anything that converts to a boolean.  If it converts to ``True``, the pin
            is set high, otherwise it is set low.
        """
        print('setting value', value)
        self._value = value

pin = Pin()
pin.value(1)

pin_value = pin.value()
print('pin_value via class', pin_value)

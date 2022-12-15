# ANDY fake display

# class SSD1306_I2C:
#     def __init__(self, *args):
#         pass

#     def contrast(self, *args):
#         pass

#     def fill(self, *args):
#         pass

#     def fill_rect(self, *args):
#         pass

#     def rect(self, *args):
#         pass

#     def text(self, *args):
#         pass

#     def show(self, *args):
#         pass

#     def blit(self, *args):
#         pass

class Logging():
    def __init__(self, *args):
        pass

    def debug(self, *args):
        print("debug: ", args)

logging = Logging()

class SSD1306_I2C(object):
    def __init__(self, width, height, i2c='dummy', addr=60):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr

        self.latest_text = 'hi from SSD1306_I2C'
        print('init SSD1306_I2C')

    def text(self, txt, x, y, colour=None):
        logging.debug('Setting text "%s" at coord %d,%d' % (txt, x, y))
        self.latest_text = txt

    def show(self):
        logging.debug('Showing on lcd')

    def fill(self, value):
        logging.debug('Fill with %s' % value)

    def invert(self, invert):
        logging.debug('Inverting pixels')

    def contrast(self, contrast):
        logging.debug('Setting contrast')

    def pixel(self, x, y, col):
        logging.debug('Setting pixel at %d.%d' % (x, y))

    def scroll(self, dx, dy):
        logging.debug('Scrolling')

    def poweroff(self):
        logging.debug('Poweroff display')

    def init_display(self):
        logging.debug('init_display')

print('imported ssd1306.py from software/contrib/andy')

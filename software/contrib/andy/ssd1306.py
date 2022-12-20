from version import __version__  # ANDY this is the EuroPython version

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
        # print("debug: ", args)
        pass

logging = Logging()

class SSD1306_I2C(object):
    def __init__(self, width, height, i2c='dummy', addr=60):
        self.width = width
        self.height = height
        self.i2c = i2c
        self.addr = addr

        # ANDY
        self.commands = [] # tuple of (cmd, params)
        self.flush_to_ui = False

    def text(self, txt, x, y, colour=None):
        logging.debug('Setting text "%s" at coord %d,%d' % (txt, x, y))

        # Hack to show version number in green along with the bootsplash logo
        version_str = str(__version__)
        if txt == version_str:
            colour = 88  # ANDY just my convention for green, I don't know what the real colour values are
        self.commands.append(('text', (txt, x, y, colour)))
        if (len(self.commands) > 50):
            raise Exception(f'Too many commands {len(self.commands)}')

    def show(self):
        logging.debug('Showing on lcd')
        self.flush_to_ui = True

    def fill(self, value):
        logging.debug('Fill with %s' % value)

        # Extra optimisation: if we have a fill command, we can remove all the other previous commands
        self.commands = [] # tuple of (cmd, params)

        self.commands.append(('fill', (value,)))
        # print('At time of fill, commands are', len(self.commands))
        
        # self.flush_to_ui = False

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

    def blit(self, frame_buffer, x, y):
        logging.debug('blit')
        self.commands.append(('blit', (frame_buffer, x, y)))

print('imported ssd1306.py from software/contrib/andy')

# ANDY 
"""
The FrameBuffer class provides a pixel buffer which can be drawn upon with
pixels, lines, rectangles, ellipses, polygons, text and even other FrameBuffers.
It is useful when generating output for displays.

For example:

    import framebuf

    # FrameBuffer needs 2 bytes for every RGB565 pixel
    fbuf = framebuf.FrameBuffer(bytearray(100 * 10 * 2), 100, 10, framebuf.RGB565)

    fbuf.fill(0)
    fbuf.text('MicroPython!', 0, 0, 0xffff)
    fbuf.hline(0, 9, 96, 0xffff)

"""
class FrameBuffer:
    def __init__(self, buffer, width, height, format, stride=None, /):
        if stride is None:
            stride = width
        # print(f'FrameBuffer', 'buffer', buffer, 'width', width, 'height', height, 'format', format, 'stride', stride)
        self.buffer = buffer
        self.width = width
        self.height = height
        self.format = format
        self.stride = stride

    def blit(self, fbuf, x, y, key=- 1, palette=None):
        """
        https://docs.micropython.org/en/latest/library/framebuf.html

        Draw another FrameBuffer on top of the current one at the given coordinates. If
        key is specified then it should be a color integer and the corresponding color
        will be considered transparent: all pixels with that color value will not be
        drawn. (If the palette is specified then the key is compared to the value from
        palette, not to the value directly from fbuf.)

        The palette argument enables blitting between FrameBuffers with differing
        formats. Typical usage is to render a monochrome or grayscale glyph/icon to a
        color display. The palette is a FrameBuffer instance whose format is that of the
        current FrameBuffer. The palette height is one pixel and its pixel width is the
        number of colors in the source FrameBuffer. The palette for an N-bit source
        needs 2**N pixels; the palette for a monochrome source would have 2 pixels
        representing background and foreground colors. The application assigns a color
        to each pixel in the palette. The color of the current pixel will be that of
        that palette pixel whose x position is the color of the corresponding source
        pixel.

        """
        print(f'blit', 'fbuf', fbuf, 'x', x, 'y', y, 'key', key, 'palette', palette)


"""
framebuf.MONO_HLSB
https://docs.micropython.org/en/latest/library/framebuf.html#constants

Monochrome (1-bit) color format This defines a mapping where
the bits in a byte are horizontally mapped. Each byte occupies 8 horizontal
pixels with bit 7 being the leftmost. Subsequent bytes appear at successive
horizontal locations until the rightmost edge is reached. Further bytes are
rendered on the next row, one pixel lower.
"""
MONO_HLSB = 3

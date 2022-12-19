# Util

def convert_to_xbm(frame_buffer, filename):
    msg = f'#define im_width {frame_buffer.width}\n#define im_height {frame_buffer.height}\nstatic char im_bits[] = {{\n'
    idx = 0
    for byte in frame_buffer.buffer:

        # change byte endian
        byte = (byte & 0xF0) >> 4 | (byte & 0x0F) << 4
        byte = (byte & 0xCC) >> 2 | (byte & 0x33) << 2
        byte = (byte & 0xAA) >> 1 | (byte & 0x55) << 1

        msg += '0x{:02x}'.format(byte) + ','
        idx += 1
        if idx % 8 == 0:
            msg += '\n'
    msg += '};'
    # write to file
    with open(filename, 'w') as f:
        f.write(msg)


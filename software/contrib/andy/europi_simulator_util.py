from europi import cvs, ticks_ms

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



# Displaying of LEDS

cvs_snapshot_msg = ''
cvs_snapshot_msg_last_tick = ''
cvs_last_tick = 0
cvs_snapshot = []
cvs_snapshot_time = 0

def get_cvs_snapshot_msg():
    return cvs_snapshot_msg

def get_cvs_snapshot():
    return cvs_snapshot
def get_cvs_snapshot_time():
    return cvs_snapshot_time

def display(tick=0):
    """We get a number of calls here with the same tick value, so we only print when the tick changes.
    """
    global cvs_snapshot_msg
    global cvs_last_tick
    global cvs_snapshot_msg_last_tick
    global cvs_snapshot, cvs_snapshot_time
    same_line_print = True

    # pure
    cvs_snapshot = [1 if cv.pin._pin.value() else 0 for cv in cvs]  # for display
    cvs_snapshot_time = ticks_ms()

    cvs_snapshot_msg = f'tick:{tick:0>2} time:{ticks_ms():0>6} '
    for index, value in enumerate(cvs):
        cvs_snapshot_msg += f'{index+1 if value.pin._pin.value() else " "}'

    if tick != cvs_last_tick and cvs_snapshot_msg_last_tick != '':
        if same_line_print:
            print(f'\r{cvs_snapshot_msg_last_tick}', end='', flush=True)
        else:
            print(cvs_snapshot_msg_last_tick)
    
    cvs_last_tick = tick
    cvs_snapshot_msg_last_tick = cvs_snapshot_msg   

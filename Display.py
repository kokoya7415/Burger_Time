import board
from digitalio import DigitalInOut
from adafruit_rgb_display import st7789

def setup_display():
    spi = board.SPI()
    cs_pin = DigitalInOut(board.CE0)
    dc_pin = DigitalInOut(board.D25)
    reset_pin = DigitalInOut(board.D24)
    BAUDRATE = 24000000

    disp = st7789.ST7789(
        spi,
        height=240,
        y_offset=80,
        rotation=180,
        cs=cs_pin,
        dc=dc_pin,
        rst=reset_pin,
        baudrate=BAUDRATE,
    )
    return disp

def setup_backlight():
    backlight = DigitalInOut(board.D26)
    backlight.switch_to_output(value=True)
    return backlight

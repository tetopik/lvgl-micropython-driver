# LOLIN S3 Pro MicroPython Helper Library

from micropython import const
from machine import Pin, ADC, I2C
from neopixel import NeoPixel

# Pin Assignments

# UART
UART_RX = const(44)
UART_TX = const(43)

# SPI
SPI_MOSI = const(11)
SPI_MISO = const(13)
SPI_CLK = const(12)

# TF/MicroSD
TF_CS = const(46)

# Display(TFT)
TS_CS = const(45)
TFT_CS = const(48)
TFT_DC = const(47)
TFT_RST = const(21)
TFT_LED = const(14)

# I2C
I2C_SDA = const(9)
I2C_SCL = const(10)
i2c = I2C(sda=I2C_SDA, scl=I2C_SCL)

# RGB_LED
RGB_DATA = const(38)
_rgb_led = NeoPixel(Pin(RGB_DATA), 1)

def rgb_led(r=0, g=0, b=0):
    _rgb_led[0] = (g, r, b)
    _rgb_led.write()

# Battery Voltage
V_BATT = const(3)
vbatt = ADC(V_BATT)
def get_vbatt():
    return (vbatt.read_uv() * 2) / 1000_000

# BUTTON
BUTTON = const(0)
button = Pin(BUTTON, Pin.IN, Pin.PULL_UP)
def driver():
    from micropython import const, alloc_emergency_exception_buf as aeeb
    from esp import osdebug
    from gc import collect
    from machine import SPI, Pin, freq
    from lcd_bus import SPIBus

    osdebug(None)
    freq(240_000_000)
    aeeb(100)
    collect()

    _HOST = const(1)
    _SCK  = const(16)
    _MISO = const(-1)
    _MOSI = const(18)
    _DC   = const(33)
    _CS   = const(35)
    _RST  = const(37)

    _FREQ     = const(80_000_000) # default: 40 MHz
    _WIDTH    = const(240)
    _HEIGHT   = const(240)
    _DURATION = const(1) # default: 33

    spi_bus = SPI.Bus(host=_HOST, mosi=_MOSI, miso=_MISO, sck=_SCK)
    dsp_bus = SPIBus(spi_bus=spi_bus, dc=_DC, cs=_CS, freq=_FREQ)

    import lvgl as lv
    from gc9a01 import GC9A01, BYTE_ORDER_BGR, STATE_LOW
    display = GC9A01(
        data_bus=dsp_bus,
        display_width=_WIDTH,
        display_height=_HEIGHT,
        reset_pin=_RST,
        reset_state=STATE_LOW,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=BYTE_ORDER_BGR,
        rgb565_byte_swap=True)
    display.init()

    from task_handler import TaskHandler
    th = TaskHandler(duration=_DURATION)
    
    return lv

if __main__ == '__main__':
    lv = driver()
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0xFF0000), 0)
    
    spinner = lv.spinner(scrn)
    spinner.align(lv.ALIGN.TOP_MID, 0, 15)
    spinner.set_size(50, 50)
    
    label = lv.label(scrn)
    label.center()
    label.set_text('Hi, Welcome!')

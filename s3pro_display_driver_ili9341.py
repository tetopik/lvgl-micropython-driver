def config():
    from gc import collect
    collect()

    from micropython import const, alloc_emergency_exception_buf as aeeb
    aeeb(100)

    from machine import freq
    freq(240_000_000)

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
    
    import lvgl as lv
    from os import uname
    version = f'LVGL {lv.version_major()}.{lv.version_minor()}.{lv.version_patch()} on MPY {uname().release}'

    from machine import SPI
    spi_bus = SPI.Bus(host=1, mosi=SPI_MOSI, miso=SPI_MISO, sck=SPI_CLK)
    
    from lcd_bus import SPIBus as LCDBus
    dsp_bus = LCDBus(spi_bus=spi_bus, dc=TFT_DC, cs=TFT_CS, freq=40_000_000)
    tch_bus = SPI.Device(spi_bus=spi_bus, freq=2_500_000, cs=TS_CS)
    
    from ili9341 import ILI9341 as Driver, STATE_PWM, BYTE_ORDER_BGR, STATE_LOW
    display = Driver(
        data_bus=dsp_bus,
        display_width=240,
        display_height=320,
        backlight_pin=TFT_LED,
        backlight_on_state=STATE_PWM,
        reset_pin=TFT_RST,
        reset_state=STATE_LOW,
        color_space=lv.COLOR_FORMAT.RGB565,
        color_byte_order=BYTE_ORDER_BGR,
        rgb565_byte_swap=True)
    display.init(1)
    
    from xpt2046 import XPT2046
    indev = XPT2046(tch_bus)
    indev.enable_input_priority()
    if not indev.is_calibrated:
        # display.set_backlight(100)
        # indev.calibrate()
        indev._cal.mirrorX = True
        indev._cal.mirrorY = True
        indev._cal.alphaX  = 1.1392084
        indev._cal.betaX   = 0.0050631488
        indev._cal.deltaX  = -15.851874
        indev._cal.alphaY  = 0.007313437
        indev._cal.betaY   = -1.1555231
        indev._cal.deltaY  = 354.41676
        indev._cal.save()
    display.set_rotation(lv.DISPLAY_ROTATION._90)
    display.set_backlight(75)
    
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0x8f0000), 0)

    from task_handler import TaskHandler
    th = TaskHandler()
    
    return version, display, indev

version, display, indev = config()
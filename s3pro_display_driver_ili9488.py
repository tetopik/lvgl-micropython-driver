def config():
    from gc import collect
    collect()
    
    from esp import osdebug
    osdebug(None)
    
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

    from machine import SPI, SDCard
    spi_bus = SPI.Bus(host=1, mosi=SPI_MOSI, miso=SPI_MISO, sck=SPI_CLK)
    
    from lcd_bus import SPIBus as LCDBus
    dsp_bus = LCDBus(spi_bus=spi_bus, dc=TFT_DC, cs=TFT_CS, freq=32_000_000)
    tch_bus = SPI.Device(spi_bus=spi_bus, freq=2_000_000, cs=TS_CS)
    
    from ili9488 import ILI9488 as Driver, STATE_PWM, BYTE_ORDER_RGB, STATE_LOW
    display = Driver(
        data_bus=dsp_bus,
        display_width=320,
        display_height=480,
        backlight_pin=TFT_LED,
        backlight_on_state=STATE_PWM,
        reset_pin=TFT_RST,
        reset_state=STATE_LOW,
        color_space=lv.COLOR_FORMAT.RGB888,
        color_byte_order=BYTE_ORDER_RGB,
        rgb565_byte_swap=True)
    display.init()
    
    from xpt2046 import XPT2046
    indev = XPT2046(tch_bus)
    # indev.enable_input_priority()
    if not indev.is_calibrated:
        # display.set_backlight(100)
        # indev.calibrate()
        indev._cal.mirrorX = False
        indev._cal.mirrorY = False
        indev._cal.alphaX  = 1.0878899
        indev._cal.betaX   = -0.0028478794
        indev._cal.deltaX  = -12.27677
        indev._cal.alphaY  = 0.009200841
        indev._cal.betaY   = -1.0995005
        indev._cal.deltaY  = 507.9147
        indev._cal.save()
    display.set_rotation(lv.DISPLAY_ROTATION._180)
    display.set_backlight(100)
    
    scrn = lv.screen_active()
    scrn.set_style_bg_color(lv.color_hex(0xef0000), 0)

    from task_handler import TaskHandler
    th = TaskHandler()
    
    from time import sleep
    for i in range(1, 101):
        display.set_backlight(i)
        sleep(0.02)
    
    try:
        from os import mount, listdir
        sd = SDCard(spi_bus=spi_bus, cs=TF_CS, freq=20_000_000)
        mount(sd, '/sd')
        print('SDCard Mounted')
        print(listdir('/sd'))
    except Exception as e:
        print(f'SDCard Error: {e}')
        
    return version, display, indev

def drive_letter():
    '''
    How to convert font files refer here: https://github.com/lvgl/lv_font_conv
    lv_font_conv --size 20 --format bin --bpp 1 --font Alibaba-PuHuiTi-Medium.subset.ttf --range 0x20-0x7f --no-compress -o font-PHT-en-20.bin

    font12 = lv.binfont_create(f'S:{path}/ui_font12.bin')

    with open(f'{path}/background.png', 'rb') as f: png_data = f.read()
    png_image_dsc = lv.image_dsc_t({
        'data_size': len(png_data),
        'data': png_data})
    '''
    
    from fs_driver import fs_register
    fs_drv = lv.fs_drv_t()
    fs_register(fs_drv, 'S')
    
    import sys
    sys.path.append('')
    try:
        path = __file__[:__file__.rfind('/')] if __file__.find('/') >= 0 else '.'
    except NameError:
        path = ''
    return path

version, display, indev = config()

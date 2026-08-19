import display_driver
import lvgl as lv

scrn = lv.screen_active()
cb0 = lv.checkbox(scrn)
cb1 = lv.checkbox(scrn)
sld = lv.slider(scrn)
spn = lv.spinner(scrn)
drd = lv.dropdown(scrn)
txt = lv.label(scrn)

def sld_cb(e):
    if e.get_code() == lv.EVENT.VALUE_CHANGED:
        txt.set_text(str(sld.get_value()))

drd.set_align(lv.ALIGN.TOP_MID)
drd.set_pos(0, 50)
cb0.set_align(lv.ALIGN.TOP_RIGHT)
cb1.set_align(lv.ALIGN.BOTTOM_LEFT)
spn.set_size(35, 35)
txt.center()
txt.set_pos(0, 25)
txt.set_text(str(sld.get_value()))
sld.center()
sld.add_event_cb(sld_cb, lv.EVENT.VALUE_CHANGED, None)

import time
from machine import Pin
import neopixel
import _thread

Pin12 = Pin(12,Pin.OUT)
Pin13 = Pin(13,Pin.OUT)
Pin14 = Pin(14,Pin.OUT)
Pin12.off()
Pin13.off()
Pin14.on()

# 初始化WS2812B灯带
np1 = neopixel.NeoPixel(Pin(2, Pin.OUT), 300)
np1[0] = (140,100,120)
np1.write()
def show():
    time.sleep(1)
    np1[0] = (0,0,0)
    np1.write()
    time.sleep(0.25)
    np1[0] = (255,0,0)
    np1.write()
    time.sleep(0.25)
    np1[0] = (0,0,0)
    np1.write()
    time.sleep(0.25)
    np1[0] = (0,255,0)
    np1.write()
    time.sleep(0.25)
    np1[0] = (0,0,0)
    np1.write()
    time.sleep(0.25)
    np1[0] = (0,0,255)
    np1.write()
    time.sleep(0.25)
    np1[0] = (0,0,0)
    np1.write()
    time.sleep(0.25)
    np1[0] = (255,255,255)
    np1.write()
    time.sleep(1)
    while(0):
        for i in range(100):
            np1[0] = (20+i*2,60,220-i*2)
            np1.write()
            time.sleep(0.02)
        for i in range(100):
            np1[0] = (220-i*2,60,20+i*2)
            np1.write()
            time.sleep(0.02)
_thread.start_new_thread(show,())

import time
from machine import Pin
import neopixel
import _thread
import esp32

def setup_stable_pins(v12=1,v13=0,v14=0):
    """
    P12 P13 P14 PD_VBUS
     1   -   -    5v
     0   0   0    9v
     0   0   1    12v
     0   1   1    15v
     0   1   0    20v
    """
    # 配置GPIO13和14为输出，并设置初始值
    pin12 = Pin(12, Pin.OUT, value=v12)
    pin13 = Pin(13, Pin.OUT, value=v13)
    pin14 = Pin(14, Pin.OUT, value=v14)
    
    # 使用esp32模块的GPIO保持功能（如果支持）
    try:
        # 锁定引脚电平，防止被其他功能影响
        esp32.gpio_hold_en(pin12)
        esp32.gpio_hold_en(pin13)
        esp32.gpio_hold_en(pin14)
        print("Pins locked with gpio_hold")
    except:
        print("gpio_hold not supported, using alternative method")
        # 备用方案：定期刷新电平
        return pin12, pin13, pin14

# 在程序开始时调用
pin12, pin13, pin14 = setup_stable_pins(0,0,1)

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
    time.sleep(0)
    while(True):
        for i in range(100):
            np1[0] = (20+i*2,60,220-i*2)
            np1.write()
            time.sleep(0.02)
        for i in range(100):
            np1[0] = (220-i*2,60,20+i*2)
            np1.write()
            time.sleep(0.02)
_thread.start_new_thread(show,())

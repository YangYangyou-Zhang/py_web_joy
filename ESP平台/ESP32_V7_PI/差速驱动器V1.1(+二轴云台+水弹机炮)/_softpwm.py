import _thread
import time
from machine import Pin

class SoftPWM:
    def __init__(self, pin, freq=50, duty_u16=0):
        """
        基于多线程的SoftPWM实现
        
        :param pin: PWM输出引脚
        :param freq: PWM频率(Hz)，默认为50Hz
        :param duty_u16: 初始占空比(0-65535)
        """
        self._pin = Pin(pin, Pin.OUT)
        self._freq = freq
        self._period = 1.0 / freq
        self._duty_u16 = 0
        self._running = False
        self._lock = _thread.allocate_lock()
        
        # 启动PWM线程
        self._thread_id = _thread.start_new_thread(self._pwm_thread, ())
        self.duty_u16(duty_u16)  # 设置初始占空比
        
    def _pwm_thread(self):
        """PWM生成线程"""
        while True:
            with self._lock:
                if not self._running:
                    time.sleep(0.1)  # 不运行时降低CPU占用
                    continue
                    
                duty_cycle = self._duty_u16 / 65535.0
                on_time = self._period * duty_cycle
                off_time = self._period - on_time
                
            if on_time > 0:
                self._pin.on()
                time.sleep(on_time)
            if off_time > 0:
                self._pin.off()
                time.sleep(off_time)
                
    def duty_u16(self, value=None):
        """设置或获取占空比(0-65535)"""
        with self._lock:
            if value is None:
                return self._duty_u16
                
            value = max(0, min(65535, int(value)))
            self._duty_u16 = value
            self._running = (value != 0 and value != 65535)
            
            # 特殊处理0%和100%占空比
            if value == 0:
                self._pin.off()
            elif value == 65535:
                self._pin.on()
    
    def deinit(self):
        """释放资源"""
        with self._lock:
            self._running = False
            self._pin.off()
    
    def __del__(self):
        """对象销毁时自动释放资源"""
        self.deinit()
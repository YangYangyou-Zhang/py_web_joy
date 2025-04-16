from microdot import Microdot
import _thread
from machine import freq,Pin,PWM
import network
import os
freq(240000000)

with open('index.html', 'r') as f:
    html = f.read()

o4 = PWM(Pin(4),freq=100,duty_u16=0)
o5 = PWM(Pin(5),freq=100,duty_u16=0)
o6 = PWM(Pin(6),freq=100,duty_u16=0)
o7 = PWM(Pin(7),freq=100,duty_u16=0)
o8 = PWM(Pin(8),freq=100,duty_u16=0)
o9 = PWM(Pin(9),freq=100,duty_u16=0)
o10 = PWM(Pin(10),freq=100,duty_u16=0)
o11 = PWM(Pin(11),freq=100,duty_u16=0)
global is_running
is_running = False
def set_speed(x1=0,y1=0,x2=0,y2=0):
    global is_running
    if is_running and (x1!=0 and y1!=0 and x2!=0 and y2!=0):
        return
    is_running = True
    if(x2==0 and y2==0):
        l = min(max(x1+y1,-1),1)
        r = min(max(x1-y1,-1),1)
    else:
        l = min(max(x2+y2,-1),1)
        r = min(max(x2-y2,-1),1)
    if l>=0:
        o4.duty_u16(int(l*65535*0.4))
        o5.duty_u16(0)
    else:
        o4.duty_u16(0)
        o5.duty_u16(int(abs(l)*65535*0.4))
    if r>=0:
        o6.duty_u16(int(r*65535*0.4))
        o7.duty_u16(0)
    else:
        o6.duty_u16(0)
        o7.duty_u16(int(abs(r)*65535*0.4))
    is_running = False



def connect(SSID,PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            pass
        print('network config: ', wlan.ifconfig())
def hotspot(SSID="ESP32_V7_PI", PASSWORD="12345678"):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    # 设置接入点参数
    ap.config(essid=SSID, authmode=network.AUTH_WPA_WPA2_PSK, password=PASSWORD)
    print('AP IP address:', ap.ifconfig()[0])

hotspot()
#connect("TP_LINK_407","xamdlgxy")

app = Microdot()
# 存储摇杆数据的全局变量
joystick_data = {'joy1': {'x':0, 'y':0}, 'joy2': {'x':0, 'y':0}}


@app.route('/')
def index(request):
    return html, 200, {'Content-Type': 'text/html'}

@app.route('/get_joystick_data', methods=['POST'])
def handle_joystick(request):
    global joystick_data
    data = request.json
    
    # 处理摇杆1数据
    if 'x1' in data and 'y1' in data:
        joystick_data['joy1']['x'] = float(data['x1'])
        joystick_data['joy1']['y'] = float(data['y1'])
    
    # 处理摇杆2数据
    if 'x2' in data and 'y2' in data:
        joystick_data['joy2']['x'] = float(data['x2'])
        joystick_data['joy2']['y'] = float(data['y2'])

    """
    print(f"Joy1: ({joystick_data['joy1']['x']:.2f}, {joystick_data['joy1']['y']:.2f}) | "
          f"Joy2: ({joystick_data['joy2']['x']:.2f}, {joystick_data['joy2']['y']:.2f})")
    """
    _thread.start_new_thread(set_speed, (joystick_data['joy1']['x'], joystick_data['joy1']['y'], joystick_data['joy2']['x'], joystick_data['joy2']['y']))
    return {'status': 'updated'}



if __name__ == '__main__':
    app.run(debug=False,port=80)


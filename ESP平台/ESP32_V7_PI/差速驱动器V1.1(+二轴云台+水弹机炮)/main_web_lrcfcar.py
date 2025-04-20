from microdot import Microdot
import _thread
from _softpwm import SoftPWM
from machine import freq,Pin,PWM
import network
freq(240000000)

with open('index.html', 'r') as f:
    html = f.read()

# 创建实例: 输入引脚4-7控制输出引脚8-11的PWM

o4 = PWM(4, freq=50, duty_u16=0)
o5 = PWM(5, freq=50, duty_u16=0)
o6 = PWM(6, freq=50, duty_u16=0)
o7 = PWM(7, freq=50, duty_u16=0)
o8 = PWM(8, freq=50, duty_u16=0)
o9 = SoftPWM(9, freq=20, duty_u16=0)
o10 = PWM(10, freq=50, duty_u16=0)
o11 = SoftPWM(11, freq=20, duty_u16=0)


no1 = Pin(1,Pin.OUT)
#io39 = PWM(Pin(39),freq=50,duty_u16=int(65535*(1500/20000)))
#io40 = PWM(Pin(40),freq=50,duty_u16=int(65535*(1500/20000)))
io41 = PWM(Pin(41),freq=50,duty_u16=int(65535*(1500/20000)))
io42 = PWM(Pin(42),freq=50,duty_u16=int(65535*(1500/20000)))


global is_running
is_running = False
def set_speed(x1=0,y1=0,x2=0,y2=0,x3=0,y3=0):

    global is_running
    if is_running and (x1!=0 and y1!=0 and x2!=0 and y2!=0 and x3!=0):
        return
    is_running = True

    x1 = x1*0.25
    y1 = y1*0.25
    x2 = x2*0.25
    y2 = y2*0.25
    x3 = x3*1

    if(True):
        #io39.duty_u16(int((1500+x1*1000)*65535/2000))
        #io40.duty_u16(int((1500+y1*1000)*65535/2000))
        l = min(max(y1+x1,-1),1)
        r = min(max(y1-x1,-1),1)
        if l>=0:
            o4.duty_u16(int(l*65535))
            o5.duty_u16(0)
            o8.duty_u16(int(l*65535))
            o9.duty_u16(0)
        else:
            o4.duty_u16(0)
            o5.duty_u16(int(abs(l)*65535))
            o8.duty_u16(0)
            o9.duty_u16(int(abs(l)*65535))
        if r>=0:
            o6.duty_u16(int(r*65535))
            o7.duty_u16(0)
            o10.duty_u16(int(r*65535))
            o11.duty_u16(0)
        else:
            o6.duty_u16(0)
            o7.duty_u16(int(abs(r)*65535))
            o10.duty_u16(0)
            o11.duty_u16(int(abs(r)*65535))
    if(True):
        io41.duty_u16(int((1500+x2*1000)*65535/20000))
        io42.duty_u16(int((1500+y2*1000)*65535/20000))
    if(x3>0.5 or x3<-0.5):
        no1.on()
    else:
        no1.off()

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
joystick_data = {'joy1': {'x':0, 'y':0}, 'joy2': {'x':0, 'y':0}, 'joy3': {'x':0, 'y':0}}


@app.route('/')
def index(request):
    return html, 200, {'Content-Type': 'text/html'}

@app.route('/get_joystick_data', methods=['POST'])
def handle_joystick(request_data=None):
    if request_data:
        data = request_data.json
    #else:
    #    data = request.json
    global joystick_data
    
    # 处理摇杆1数据
    if 'x1' in data and 'y1' in data:
        joystick_data['joy1']['x'] = float(data['x1'])
        joystick_data['joy1']['y'] = float(data['y1'])
    
    # 处理摇杆2数据
    if 'x2' in data and 'y2' in data:
        joystick_data['joy2']['x'] = float(data['x2'])
        joystick_data['joy2']['y'] = float(data['y2'])

    # 处理摇杆3数据
    if 'x3' in data and 'y3' in data:
        joystick_data['joy3']['x'] = float(data['x3'])
        joystick_data['joy3']['y'] = float(data['y3'])

    """
    print(f"Joy1: ({joystick_data['joy1']['x']:.2f}, {joystick_data['joy1']['y']:.2f}) | "
          f"Joy2: ({joystick_data['joy2']['x']:.2f}, {joystick_data['joy2']['y']:.2f}) | "
          f"Joy3: ({joystick_data['joy3']['x']:.2f}, {joystick_data['joy3']['y']:.2f})")
    """
    _thread.start_new_thread(set_speed, (joystick_data['joy1']['x'], joystick_data['joy1']['y'], joystick_data['joy2']['x'], joystick_data['joy2']['y'], joystick_data['joy3']['x'], joystick_data['joy3']['y']))
    return {'status': 'updated'}



if __name__ == '__main__':
    app.run(debug=False,port=80)



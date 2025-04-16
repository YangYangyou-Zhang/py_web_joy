import network
import socket
import time
from machine import Pin
import neopixel
Pin12 = Pin(12,Pin.OUT)
Pin13 = Pin(13,Pin.OUT)
Pin14 = Pin(14,Pin.OUT)
Pin12.off()
Pin13.on()
Pin14.on()
# 网络配置
ssid = 'ESP_WS2812B_BY_YYY'
password = '12345678'

# 初始化WS2812B灯带
global r, g, b
r = g = b = 0  # 初始颜色为黑色
num_leds = 300  # 每组灯珠数量
pin1 = Pin(2, Pin.OUT)  # GPIO2 控制第一组灯

np1 = neopixel.NeoPixel(pin1, num_leds)
np1[0] = (140,100,120)
np1.write()

# 启动AP模式
ap = network.WLAN(network.AP_IF)  # 创建AP接口
def start_ap(ssid, password):
    ap.active(True)  # 激活AP接口
    ap.config(essid=ssid, password=password)  # 配置AP的SSID和密码

    # 等待AP接口激活
    start_time = time.time()
    while not ap.active():
        if time.time() - start_time > 10:  # 超时检测（10秒）
            print("AP模式启动失败，请检查配置")
            return
        time.sleep(0.5)

    # 获取AP的IP地址
    ip_address = ap.ifconfig()[0]
    print(f'AP模式启动成功，SSID: {ssid}, IP地址: {ip_address}')

# 创建网页
def web_page():
    html = """<!DOCTYPE html>
    <html>
    <head>
        <title>WS2812B控制</title>
        <style>
            body { text-align: center; margin-top: 50px; }
            input[type="color"] { width: 100px; }
        </style>
    </head>
    <body>
        <h1>WS2812B 呼吸灯控制 技术支持:cn洋洋柚</h1>
        <button onclick="toggleLight()">打开/关闭灯</button>
        <br><br>
        <input type="color" id="colorPicker" value="#000000" onchange="changeColor(this.value)">
        <script>
            function toggleLight() {
                var xhr = new XMLHttpRequest();
                xhr.open("GET", "/toggle", true);
                xhr.send();
            }

            function changeColor(color) {
                var xhr = new XMLHttpRequest();
                xhr.open("GET", "/color?value=" + encodeURIComponent(color), true);  // 编码颜色值
                xhr.send();
            }
        </script>
    </body>
    </html>"""
    return html

# 启动Web服务器
def web_server():
    addr = socket.getaddrinfo('192.168.4.1', 80)[0][-1]  # 监听所有IP地址
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Web服务器运行在:', addr)

    while True:
        cl, addr = s.accept()
        print('接受来自', addr)
        request = cl.recv(1024)
        request = str(request)
        print('请求:', request)

        if '/toggle' in request:
            toggle_light()
        if '/color?value=' in request:
            color = request.split('value=')[1].split(' ')[0]  # 提取颜色值
            color = color.replace('%23', '#')  # 将 %23 替换为 #
            print("接收到的颜色值:", color)
            set_color(color)

        response = web_page()
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

# 控制灯光
light_on = False

def toggle_light():
    global light_on
    light_on = not light_on
    if light_on:
        breathe_light()
    else:
        np1.fill((0, 0, 0))  # 关闭第一组灯
        np1.write()

def set_color(color):
    global r, g, b
    try:
        # 确保颜色值是6位16进制格式
        if len(color) == 7 and color[0] == '#':
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            for i in range(75):
                np1[i] = (r, g, b)  # 第1组灯渐变
                np1[i+75] = (r, g, b)  # 第2组灯渐变
                np1[i+150] = (r, g, b)  # 第3组灯渐变
                np1[i+225] = (r, g, b)  # 第4组灯渐变
                np1.write()
                time.sleep(0.02)
            print(f"设置颜色成功: R={r}, G={g}, B={b}")
        else:
            print("颜色值格式错误:", color)
    except ValueError as e:
        print("颜色值解析失败:", e)

def breathe_light():
    global r, g, b
        
    while light_on:
        for i in range(255):
            if not light_on:
                break
            np1.fill((int(i*r/255), int(i*g/255), int(i*b/255)))  # 第一组灯渐变
            np1.write()
            time.sleep(0.01)
        for i in range(255, 0, -1):
            if not light_on:
                break
            np1.fill((int(i*r/255), int(i*g/255), int(i*b/255)))  # 第一组灯渐变
            np1.write()
            time.sleep(0.01)

# 主程序
start_ap(ssid, password)
web_server()
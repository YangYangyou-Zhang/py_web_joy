项目简介：

web_joy_ros是一个基于ROS的web控制系统的linux_ros迁移版本，可以让用户通过浏览器控制机器人或者小车。

项目结构：
```
web_joy_ros
├── flask_test.py
├── index.html
├── README.md
```

关于配置文件的修改：
#在flask_test.py中，第15行订阅速度控制话题'/cmd_vel'，可在此处修改。
```python
# 初始化ROS发布者
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
```

#在flask_test.py中，在41到47行，修改此处*1系数来修改两个摇杆对应的摇杆量。
```python
    if 'x1' in data and 'y1' in data:
        joystick_data['joy1']['x'] = float(data['x1'])*1
        joystick_data['joy1']['y'] = float(data['y1'])*1

    # 处理摇杆2数据
    if 'x2' in data and 'y2' in data:
        joystick_data['joy2']['x'] = float(data['x2'])*1
        joystick_data['joy2']['y'] = float(data['y2'])*1
```

#在flask_test.py中，第70行为用于浏览器访问的端口号。
```python
app.run(debug=True, host='0.0.0.0', port=18848)
```

#在index.html中，第145行"http://192.168.12.1:8080/stream?topic=/camera/rgb/image_raw"修改为可用视频流的地址。
```html
<img src="http://192.168.12.1:8080/stream?topic=/camera/rgb/image_raw" width="430" height="320">
```

使用方法：
1. 启动ROS，并运行web_joy_ros。记得先cd到文件夹目录下。
```
cd web_joy_ros
python flask_test.py
```
或者python3运行：
```
cd web_joy_ros
python3 flask_test.py
```
2. 打开浏览器，输入http://localhost:18848/，即可看到摇杆控制页面。
如果使用手机或者其他客户端访问，请将"http://localhost:18848/"替换为"http://实际IP地址:实际的端口号/"。


常见问题及处理办法：
1. 运行flask_test.py时，出现报错：
```
找不到index.html文件。
```
解决办法：请将index.html文件放在flask_test.py同级目录下。或者修改'index.html'为'./index.html'或者绝对路径。
```python
def index():
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except:
        with open('index.html', 'r') as f:
            html = f.read().decode('utf-8')
    return html
```

2. 运行flask_test.py时，出现报错：
```
AttributeError: 'NoneType' object has no attribute 'publish'
```
解决办法：请检查ROS是否正常运行。

3. 运行flask_test.py时，出现报错：
```
ModuleNotFoundError: No module named 'rospy'
```
解决办法：请安装ROS及使用pip安装rospy模块。（最好不要在windows下运行，因为ROS在windows下运行有很多问题）

4. 遇到其他疑难杂症
解决方法：使用AI工具查询报错。
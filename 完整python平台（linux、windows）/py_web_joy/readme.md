项目简介：

web_joy_ros是一个基于ROS的web控制系统的linux_ros迁移版本，可以让用户通过浏览器控制机器人或者小车。

项目结构：
```
py_web_joy
├── example_nav_导航调用例程
│   ├── callback NAV.py
│   └── callback.py
├── launch
│   ├── webman_ctrl.launch
│   └── webnav_ctrl.launch
├── src
├── script
│   ├── flask_test.py
│   ├── index.html
│   └── joymanctrl_flask.py
├── CMakeLists.txt
├── package.xml
└── README.md
```

关于配置文件的修改：
#在flask_test.py中，第18行订阅速度控制话题'/cmd_vel'，可在此处修改。
```python
# 初始化ROS发布者
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
```

#在flask_test.py中，在42到56行，修改此处*1系数来修改三个摇杆对应的摇杆量，加正负可以取反。
```python
    # 处理摇杆1数据
    if 'x1' in data and 'y1' in data:
        joystick_data['joy1']['x'] = float(data['x1'])*1.0
        joystick_data['joy1']['y'] = float(data['y1'])*1.0

    # 处理摇杆2数据
    if 'x2' in data and 'y2' in data:
        joystick_data['joy2']['x'] = float(data['x2'])*1.0
        joystick_data['joy2']['y'] = float(data['y2'])*1.0

    # 处理摇杆3数据
    if 'x3' in data and 'y3' in data:
        joystick_data['joy3']['x'] = float(data['x3'])*1.0
        joystick_data['joy3']['y'] = float(data['y3'])*1.0
```

#在flask_test.py中，在59到85行，提供了四种操作方式，通过注释使能其中的一种，默认为阿克曼差速底盘。
```python
#差速/阿克曼小车控制
twist_msg.linear.x = joystick_data['joy2']['y']  # 假设y2控制速度
twist_msg.angular.z = joystick_data['joy2']['x']  # 假设x2控制转向角

"""
#全向底盘/麦克纳姆轮小车控制
twist_msg.linear.x = joystick_data['joy2']['y']  # 假设y2控制前后速度
twist_msg.linear.y = joystick_data['joy2']['x']  # 假设x2控制左右速度
twist_msg.angular.z = joystick_data['joy1']['x']  # 假设x1控制转向角
"""
"""
#线速度控制无人机（多旋翼/垂直起降飞行器）(美国手)
twist_msg.linear.x = joystick_data['joy2']['y']  # 假设y2控制前后速度
twist_msg.linear.y = joystick_data['joy2']['x']  # 假设x2控制左右速度
twist_msg.linear.z = joystick_data['joy1']['y']  # 假设x1控制上下速度
twist_msg.angular.z = joystick_data['joy1']['x']  # 假设x1控制转向角
"""
"""
#角速度控制无人机（手动多旋翼/FPV）(美国手)
twist_msg.linear.x = joystick_data['joy2']['y']  # 假设y2控制前后速度
twist_msg.linear.y = joystick_data['joy2']['x']  # 假设x2控制左右速度
twist_msg.linear.z = joystick_data['joy1']['y']  # 假设x1控制上下速度
twist_msg.angular.z = joystick_data['joy1']['x']  # 假设x1控制转向角
"""
```

#在flask_test.py中，第101行为用于浏览器访问的端口号。
```python
app.run(debug=True, host='0.0.0.0', port=18848)
```

#在index.html中，第145行"http://192.168.12.1:8080/stream?topic=/camera/rgb/image_raw"修改为可用视频流的地址。
```html
<img src="http://192.168.12.1:8080/stream?topic=/camera/rgb/image_raw" width="430" height="320">
```

#在nav_flask.py中，第14行设置运动信息输出目标节点('move_base')。第38行修改为实际机器人tf坐标("base_link")。第67行修改为实际机器人tf坐标("base_link")。第85行为ip与端口号设置(host='0.0.0.0', port=13399)。
```python
ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)###14
```
```python
goal.target_pose.header.frame_id = "map"###38
```
```python
goal.target_pose.header.frame_id = "base_link"###67
```
```python
app.run(debug=True, host='0.0.0.0', port=13399)###85
```



使用方法：
1.将py_web_joy文件夹拷贝到ROS工作区的src目录下，随后使用chmod命令提权，最后编译工作空间。
```
cd ~/catkin_ws（请以实际路径为准）
sudo chmod -R 777 py_web_joy
***（这里要输入密码一次）
catkin_make
```
2. 启动ROS，并运行webman_ctrl（手动控制模式）或者webnav_ctrl（导航控制模式）。记得先加载环境变量source devel/setup.bash（请以实际路径为准）。
```
roslaunch web_joy_ros webman_ctrl.launch
```
或者（启动导航节点）
```
roslaunch web_joy_ros webnav_ctrl.launch
```
3. 打开浏览器，输入http://localhost:18848/，即可看到摇杆控制页面。
如果使用手机或者其他客户端访问，请将"http://localhost:18848/"替换为"http://实际IP地址:实际的端口号/"。
（导航控制请参考"example_nav_导航调用例程"）

常见问题及处理办法：
1. 运行flask_test.py时，出现报错：
```
importError: No module named 'flask'找不到flask文件。
```
解决办法：请安装flask模块。
```
pip3 install flask
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
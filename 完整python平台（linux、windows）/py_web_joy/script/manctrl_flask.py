#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import flask
import rospy
from flask import request
from geometry_msgs.msg import Twist

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

app = flask.Flask(__name__)
# 存储摇杆数据的全局变量
joystick_data = {'joy1': {'x': 0, 'y': 0}, 'joy2': {'x': 0, 'y': 0}, 'joy3': {'x': 0, 'y': 0}}

# 初始化ROS发布者
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

# 初始化ROS节点
rospy.init_node('flask_test_node', anonymous=True)

@app.route('/')
def index():
    try:
        with open(os.path.join(current_dir, 'index.html'), 'r', encoding='utf-8') as f:
            html = f.read()
    except:
        with open('index.html', 'r') as f:
            html = f.read().decode('utf-8')
    return html


@app.route('/get_joystick_data', methods=['POST'])
def handle_joystick(request_data=None):
    if request_data:
        data = request_data.json
    else:
        data = request.json
    global joystick_data

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


    # 创建Twist消息
    if 'joy2' in joystick_data or 'joy1' in joystick_data:
        twist_msg = Twist()

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


        # 发布速度和转向命令
        cmd_vel_pub.publish(twist_msg)
    
    """print(f"Joy1: ({joystick_data['joy1']['x']:.2f}, {joystick_data['joy1']['y']:.2f}) | "
          f"Joy2: ({joystick_data['joy2']['x']:.2f}, {joystick_data['joy2']['y']:.2f}) | "
          f"Joy3: ({joystick_data['joy3']['x']:.2f}, {joystick_data['joy3']['y']:.2f})")"""

    return flask.jsonify({'status': 'updated'})


if __name__ == '__main__':
    try:
        print(f"文件目录: {current_dir}")
        app.run(debug=True, host='0.0.0.0', port=18848)
    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        print("Flask应用已关闭")

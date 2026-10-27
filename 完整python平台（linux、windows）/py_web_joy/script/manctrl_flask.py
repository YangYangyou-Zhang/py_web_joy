#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import flask
import rospy
import cv2
import threading
import time
from flask import request, Response
from geometry_msgs.msg import Twist

# 全局变量定义
video = True
encode_param = [cv2.IMWRITE_JPEG_QUALITY, 20] # JPEG编码参数，压缩率越小越节约带宽
if video:
    try:
        video_capture = cv2.VideoCapture(0)
        def generate_frames():
            while True:
                # 读取视频流中的帧
                success, frame = video_capture.read()
                if not success:
                    break
                else:
                    # 将帧转换为JPEG格式
                    ret, buffer = cv2.imencode('.jpg', frame, encode_param)
                    frame = buffer.tobytes()
                    # 使用yield生成帧
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except:
        def generate_frames():
            return b'--frame\r\n'
        video = False

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

app = flask.Flask(__name__)

# 存储摇杆数据的全局变量
joystick_data = {'joy1': {'x': 0, 'y': 0}, 'joy2': {'x': 0, 'y': 0}, 'joy3': {'x': 0, 'y': 0}}

# 当前实际速度和目标速度
current_vel = {'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}}
target_vel = {'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}}

# 速度控制参数
ACCELERATION_LINEAR = 0.25  # 加速度值 (m/s²)，速度绝对值增大时用
ACCELERATION_ANGULAR = 0.2  # 加速度值 (rad/s²)，速度绝对值增大时用
DECELERATION_LINEAR = 0.5  # 减速度值 (m/s²)，速度绝对值减小时用（比加速大，停得更快）
DECELERATION_ANGULAR = 0.4  # 减速度值 (rad/s²)，速度绝对值减小时用（比加速大，停得更快）
MAX_LINEAR_VEL = 0.4  # 最大线速度
MAX_ANGULAR_VEL = 0.3  # 最大角速度
NO_INPUT_TIMEOUT = 0.1  # 无输入超时时间（秒）
SMOOTHING_INTERVAL = 0.02  # 平滑更新间隔（秒），约50Hz

# 转向死区：油门大于1/4油门值时生效，抑制虚拟摇杆漂移导致的误转向
THROTTLE_STEER_GATE = 0.25  # 启用转向死区的油门阈值（归一化摇杆值，1.0为满油门）
STEER_DEADZONE = 0.1  # 转向死区阈值（归一化摇杆值），超过后输出=转向值-阈值

# 时间记录
last_input_time = time.time()
last_update_time = time.time()

# 初始化ROS发布者
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

# 初始化ROS节点
rospy.init_node('flask_test_node', anonymous=True)

# 线程锁
data_lock = threading.Lock()

def _ramp_component(target, current, accel_rate, decel_rate, dt):
    """按加速/减速不同速率将 current 平滑逼近 target。

    速度绝对值在增大视为加速（用 accel_rate）；在减小或穿越零点视为减速（用 decel_rate）。
    """
    diff = target - current
    if diff == 0:
        return current
    accelerating = (current == 0) or (target * current > 0 and abs(target) > abs(current))
    rate = accel_rate if accelerating else decel_rate
    max_change = rate * dt
    if abs(diff) <= max_change:
        return target
    return current + (max_change if diff > 0 else -max_change)

def apply_steer_deadzone(value, deadzone):
    """转向死区：|value| 未超过阈值时输出0，超过后按 value 减去阈值（保留符号）。"""
    if value > deadzone:
        return value - deadzone
    if value < -deadzone:
        return value + deadzone
    return 0.0

def smooth_velocity_control():
    """平滑速度控制线程"""
    global current_vel, target_vel, last_input_time, last_update_time

    last_twist_msg = None
    while not rospy.is_shutdown():
        with data_lock:
            current_time = time.time()
            dt = current_time - last_update_time
            last_update_time = current_time

            # 检查是否超时无输入
            if current_time - last_input_time > NO_INPUT_TIMEOUT:
                # 超时，将目标速度设为0
                target_vel = {'linear': {'x': 0, 'y': 0, 'z': 0}, 'angular': {'x': 0, 'y': 0, 'z': 0}}

            # 对每个速度分量进行平滑处理（加速/减速采用不同速率）
            for vel_type in ['angular']:
                for axis in ['x', 'y', 'z']:
                    current_vel[vel_type][axis] = _ramp_component(
                        target_vel[vel_type][axis],
                        current_vel[vel_type][axis],
                        ACCELERATION_ANGULAR,
                        DECELERATION_ANGULAR,
                        dt)
            for vel_type in ['linear']:
                for axis in ['x', 'y', 'z']:
                    current_vel[vel_type][axis] = _ramp_component(
                        target_vel[vel_type][axis],
                        current_vel[vel_type][axis],
                        ACCELERATION_LINEAR,
                        DECELERATION_LINEAR,
                        dt)

            # 创建并发布Twist消息
            twist_msg = Twist()
            twist_msg.linear.x = current_vel['linear']['x']
            twist_msg.linear.y = current_vel['linear']['y']
            twist_msg.linear.z = current_vel['linear']['z']
            twist_msg.angular.x = current_vel['angular']['x']
            twist_msg.angular.y = current_vel['angular']['y']
            twist_msg.angular.z = current_vel['angular']['z']

            if twist_msg != last_twist_msg:
                cmd_vel_pub.publish(twist_msg)
                last_twist_msg = twist_msg

            """print(f"Target: L({target_vel['linear']['x']:.2f},{target_vel['linear']['y']:.2f},{target_vel['linear']['z']:.2f}) "
                  f"A({target_vel['angular']['x']:.2f},{target_vel['angular']['y']:.2f},{target_vel['angular']['z']:.2f}) | "
                  f"Current: L({current_vel['linear']['x']:.2f},{current_vel['linear']['y']:.2f},{current_vel['linear']['z']:.2f}) "
                  f"A({current_vel['angular']['x']:.2f},{current_vel['angular']['y']:.2f},{current_vel['angular']['z']:.2f})")"""

        # 控制更新频率
        time.sleep(SMOOTHING_INTERVAL)

@app.route('/')
def index():
    try:
        with open(os.path.join(current_dir, 'index.html'), 'r', encoding='utf-8') as f:
            html = f.read()
    except:
        with open('index.html', 'r') as f:
            html = f.read().decode('utf-8')
    return html

@app.route('/video_feed')
def video_feed():
    if video:
        return Response(generate_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return None

@app.route('/get_joystick_data', methods=['POST'])
def handle_joystick(request_data=None):
    if request_data:
        data = request_data.json
    else:
        data = request.json
    global joystick_data, target_vel, last_input_time

    with data_lock:
        # 更新最后输入时间
        last_input_time = time.time()

        # 处理摇杆数据
        if 'x1' in data and 'y1' in data:
            joystick_data['joy1']['x'] = float(data['x1'])
            joystick_data['joy1']['y'] = float(data['y1'])

        if 'x2' in data and 'y2' in data:
            joystick_data['joy2']['x'] = -float(data['x2'])
            joystick_data['joy2']['y'] = float(data['y2'])

        if 'x3' in data and 'y3' in data:
            joystick_data['joy3']['x'] = float(data['x3'])
            joystick_data['joy3']['y'] = float(data['y3'])

        # 根据控制模式更新目标速度
        # 这里以差速/阿克曼小车控制为例，其他模式请根据需要取消注释

        # 差速/阿克曼小车控制
        throttle = joystick_data['joy2']['y']  # 油门（前后速度）
        steer = joystick_data['joy2']['x']  # 转向

        # 油门大于1/4油门值时启用转向死区，抑制虚拟摇杆漂移导致的误转向
        if abs(throttle) > THROTTLE_STEER_GATE:
            steer = apply_steer_deadzone(steer, STEER_DEADZONE)

        target_vel['linear']['x'] = throttle * MAX_LINEAR_VEL  # 假设y2控制速度
        target_vel['angular']['z'] = steer * MAX_ANGULAR_VEL  # 假设x2控制转向角

        """
        # 全向底盘/麦克纳姆轮小车控制
        target_vel['linear']['x'] = joystick_data['joy2']['y'] * MAX_LINEAR_VEL  # 假设y2控制前后速度
        target_vel['linear']['y'] = joystick_data['joy2']['x'] * MAX_LINEAR_VEL  # 假设x2控制左右速度
        target_vel['angular']['z'] = joystick_data['joy1']['x'] * MAX_ANGULAR_VEL  # 假设x1控制转向角
        """
        """
        # 控制无人机（多旋翼/垂直起降飞行器）(美国手)
        target_vel['linear']['x'] = joystick_data['joy2']['y'] * MAX_LINEAR_VEL  # 假设y2控制前后速度
        target_vel['linear']['y'] = joystick_data['joy2']['x'] * MAX_LINEAR_VEL  # 假设x2控制左右速度
        target_vel['linear']['z'] = joystick_data['joy1']['y'] * MAX_LINEAR_VEL  # 假设x1控制上下速度
        target_vel['angular']['z'] = joystick_data['joy1']['x'] * MAX_ANGULAR_VEL  # 假设x1控制转向角
        """
        """
        # 控制无人机（多旋翼/垂直起降飞行器）(日本手)
        target_vel['linear']['x'] = joystick_data['joy1']['y'] * MAX_LINEAR_VEL  # 假设y1控制前后速度
        target_vel['linear']['y'] = joystick_data['joy1']['x'] * MAX_LINEAR_VEL  # 假设x1控制左右速度
        target_vel['linear']['z'] = joystick_data['joy2']['y'] * MAX_LINEAR_VEL  # 假设x2控制上下速度
        target_vel['angular']['z'] = joystick_data['joy2']['x'] * MAX_ANGULAR_VEL  # 假设x2控制转向角
        """

    return flask.jsonify({'status': 'updated'})

if __name__ == '__main__':
    try:
        print(f"文件目录: {current_dir}")
        print(f"加速度值(线/角): {ACCELERATION_LINEAR}/{ACCELERATION_ANGULAR}, "
              f"减速度值(线/角): {DECELERATION_LINEAR}/{DECELERATION_ANGULAR}")
        print(f"转向死区: 油门>{THROTTLE_STEER_GATE}时启用, 阈值={STEER_DEADZONE}")
        print(f"无输入超时时间: {NO_INPUT_TIMEOUT}秒")

        # 启动平滑速度控制线程
        smooth_thread = threading.Thread(target=smooth_velocity_control, daemon=True)
        smooth_thread.start()

        # 启动Flask应用
        app.run(debug=True, host='0.0.0.0', port=18848, use_reloader=False)
    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        print("Flask应用已关闭")

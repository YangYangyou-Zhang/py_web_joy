#!/usr/bin/env python3
# encoding= utf-8  

import flask
import rospy
from flask import request, jsonify
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

app = flask.Flask(__name__)

# 初始化ROS节点
rospy.init_node('nav_flask_node', anonymous=True)
ac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
ac.wait_for_server()
goal = MoveBaseGoal()

@app.route('/')
def index():
    return '点击访问导航状态：<a href="/nav_status">Check Navigation Status</a>'
@app.route('/nav_status')
def nav_status():
    return jsonify({'state': ac.get_state()}), 200

@app.route('/nav_to_map', methods=['POST'])
def nav_to_map():
    # 获取请求参数
    data = request.json
    x = float(data.get('x', 0.0))
    y = float(data.get('y', 0.0))
    z = float(data.get('z', 0.0))  # 通常不需要设置
    ox = float(data.get('ox', 0.0))  # 通常不需要设置
    oy = float(data.get('oy', 0.0))  # 通常不需要设置
    oz = float(data.get('oz', 0.0))  # 通常不需要设置
    ow = float(data.get('ow', 1.0))  # 默认值为1.0

    # 设置目标点
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = z
    goal.target_pose.pose.orientation.x = ox
    goal.target_pose.pose.orientation.y = oy
    goal.target_pose.pose.orientation.z = oz
    goal.target_pose.pose.orientation.w = ow

    # 发送目标点
    ac.send_goal(goal)
    #ac.wait_for_result()

    return jsonify({'status': 'Goal reached!'}), 200

@app.route('/nav_to_base_link', methods=['POST'])
def nav_to_base_link():
    # 获取请求参数
    data = request.json
    x = float(data.get('x', 0.0))
    y = float(data.get('y', 0.0))
    z = float(data.get('z', 0.0))  # 通常不需要设置
    ox = float(data.get('ox', 0.0))  # 通常不需要设置
    oy = float(data.get('oy', 0.0))  # 通常不需要设置
    oz = float(data.get('oz', 0.0))  # 通常不需要设置
    ow = float(data.get('ow', 1.0))  # 默认值为1.0

    # 设置目标点
    goal.target_pose.header.frame_id = "base_link"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.position.z = z
    goal.target_pose.pose.orientation.x = ox
    goal.target_pose.pose.orientation.y = oy
    goal.target_pose.pose.orientation.z = oz
    goal.target_pose.pose.orientation.w = ow

    # 发送目标点
    ac.send_goal(goal)
    #ac.wait_for_result()

    return jsonify({'status': 'Goal reached!'}), 200

if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=13399)
    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        print("Flask应用已关闭")

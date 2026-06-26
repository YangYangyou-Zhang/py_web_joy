# py_web_joy

#### 介绍
基于flask、microdot等等框架，使得在树莓派香橙派等等python的Linux平台或者是micropython嵌入式平台提供一个web服务器，使得用户可以通过手机或者电脑打开网页使用虚拟摇杆操纵设备，例如机器人、无人车、无人机等等设备。在不久的将来，将会完成linux嵌入式端（完整python环境）和在esp平台（micropython环境）的全部开发工作。后续工作顺利的话，除了esp32系列开发项目外还会将esp无人机项目一同接入到次项目的子项目。
Based on frameworks such as Flask and MicroDot, a web server is provided on Linux platforms such as Raspberry Pi and Orange Pi, or embedded platforms such as Micropython, allowing users to open web pages and use virtual joysticks to manipulate devices such as robots, unmanned vehicles, drones, etc. through their mobile phones or computers. In the near future, all development work for the Linux embedded version (complete Python environment) and the ESP platform (micropython environment) will be completed. If the follow-up work goes smoothly, in addition to the ESP32 series development project, the ESP drone project will also be integrated into the sub projects of this project.

#### 软件架构
python3&micropthon

#### 开发日志
```
2025_4_16 micropython代码测试完成，已经成功上传至开源平台
2025_4_17 开源ESP32S3_V7_PI电路图原理图等等全部资料至立创开源平台（主控是esp32s3的开发板均兼容本程序，仅需按照实际修改引脚即可）
2025_4_20 开源差速驱动器V1.1的开源代码 包含4组H桥差速底盘网页控制、2轴云台控制、水弹波箱启动器控制（主控是esp32s3的开发板均兼容本程序，仅需按照实际修改引脚即可）
2025_7_22 开源linux下ros控制的版本支持，完成web_joy_ros文件的编辑修改整理与代码运行测试工作。
2026_6_26 新增linux下ros控制的版本功能：1.内置图像视频流2.图像视频流压缩3.启停平滑控制4.控制端断联保护。
```

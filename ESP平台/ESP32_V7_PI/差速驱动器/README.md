### 用于micropython环境下esp32平台的网页遥控差速小车

main_web_lrcar为两轮差速驱动车辆驱动器代码，修改4、5、6、7的gpio为实际gpio即可直接重命名为main.py上传到esp32板卡内部使用（4为左侧驱动器向前运动、5为左侧驱动器向后运动、6为右侧驱动器向前运动、7为左侧驱动器向后运动）（gpio8、9、10、11为为了后续项目保留接口，在此代码中可以删去）。
index.html是控制用的网页，需要上传到eso32板卡的内部。
index_o.html是linux版本的网页，暂时保留不需要使用。
boot.py为ws2812b指示灯驱动，可选则上传使用，非必选。
microdot.py为micropython环境下esp32平台模拟flask功能插件，需要上传到eso32板卡的内部。
由于micropython固件本身JATG调试接口无法禁用，如果需要使用PD12v、15v、20v电压请手动调整频率为freq(40000000)#4MHz，否则电压容易跳变。
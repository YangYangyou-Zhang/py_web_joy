import requests

# 定义目标URL
urlmap = 'http://192.168.12.1:13399/nav_to_map'
urlbase_link = 'http://192.168.12.1:13399/nav_to_base_link'

#re=1运行，re=3运行
# 定义POST请求的参数
payloadC = {
    'x': 1.15,
    'y': 2.0,
    'z': 0.0,  # 通常不需要设置
    'ox': 0.0,  # 通常不需要设置
    'oy': 0.0,  # 通常不需要设置
    'oz': 1.0,  # 通常不需要设置
    'ow': 1.0   # 默认值为1.0
}
payload00 = {
    'x': 1.00,
    'y': 0.0,
    'z': 0.0,  # 通常不需要设置
    'ox': 0.0,  # 通常不需要设置
    'oy': 0.0,  # 通常不需要设置
    'oz': 0.0,  # 通常不需要设置
    'ow': 1.0   # 默认值为1.0
}

payload01 = {
    'x': -0.5,
    'y': 3.70,
    'z': 0.0,  # 通常不需要设置
    'ox': 0.0,  # 通常不需要设置
    'oy': 0.0,  # 通常不需要设置
    'oz': 1.0,  # 通常不需要设置
    'ow': 0.0   # 默认值为1.0
}

payload1 = {
    'x': -1.5,
    'y': 0.70,
    'z': 0.0,  # 通常不需要设置
    'ox': 0.0,  # 通常不需要设置
    'oy': 0.0,  # 通常不需要设置
    'oz': 1.0,  # 通常不需要设置
    'ow': 0.0   # 默认值为1.0
}

# 发送POST请求
response = requests.post(urlmap, json=payload00)

# 打印响应
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")

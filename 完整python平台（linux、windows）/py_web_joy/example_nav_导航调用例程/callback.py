import requests

# 定义目标URL
urlmap = 'http://192.168.12.1:13399/nav_to_map'
urlbase_link = 'http://192.168.12.1:13399/nav_to_base_link'

#re=1运行，re=3运行
# 定义POST请求的参数
payload = {
    'x': 1.25,
    'y': 2.1,
    'z': 0.0,  # 通常不需要设置
    'ox': 0.0,  # 通常不需要设置
    'oy': 0.0,  # 通常不需要设置
    'oz': 0.0,  # 通常不需要设置
    'ow': 1.0   # 默认值为1.0
}

# 发送POST请求
response = requests.post(urlmap, json=payload)

# 打印响应
print(f"Status Code: {response.status_code}")
print(f"Response JSON: {response.json()}")

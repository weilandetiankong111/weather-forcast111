import sys

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080
DEBUG = True

# 爬虫请求间隔
REQUEST_INTERVAL = 0

# 进度条长度
PROGRESS_BAR_LENGTH = 30

# MYSQL相关
MYSQL_HOST = '0.0.0.0'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Admin@123'
MYSQL_DATABASE = 'weather_show'
# 连接失败重试次数
MYSQL_CONNECT_ATTEMPTS = 5
# 连接失败重试间隔 单位秒
MYSQL_CONNECT_ATTEMPT_INTERVAL = 5

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Host": "weather.cma.cn",
}

REQUEST_BASE_URL = "https://weather.cma.cn/"

for arg in sys.argv:
    split = arg.split('=')
    if len(split) != 2 or split[1].strip() == '':
        continue
    value = split[1]
    if arg.startswith('--server.host='):
        SERVER_HOST = value
    elif arg.startswith('--server.port='):
        SERVER_PORT = int(value)
    elif arg.startswith('--mysql.host'):
        MYSQL_HOST = value
    elif arg.startswith('--mysql.port'):
        MYSQL_PORT = int(value)
    elif arg.startswith('--mysql.user'):
        MYSQL_USER = value
    elif arg.startswith('--mysql.password'):
        MYSQL_PASSWORD = value
    elif arg.startswith('--mysql.db'):
        MYSQL_DATABASE = value

# Weather Forcast

Weather Forcast是一个查询天气的的平台，使用Python通过爬虫的方式获取各个城市的天气信息，用户可以查看各个城市的天气信息和近七天的天气信息。

技术栈：Python+Flask+Vue+ElementUI+MySQL

- Python 3.11.4

- Flask 3.0.0

- Vue 2

- ElementUI

- MySQL 8

### How to start ?

首先需要安装依赖

```shell
pip install -r requirement.txt
```

然后在MySQL建立数据库，导入表结构，可使用提供的[SQL文件](https://gitee.com/Wshape1/ppyy-weather-show/tree/master/sql)进行创建数据库表

最后启动命令如下

```shell
python app.py \
--server.host=127.0.0.1 \
--server.port=8080 \
--mysql.host=127.0.0.1\
--mysql.port=3306 \
--mysql.user=root \
--mysql.password=123456 \
--mysql.db=weather_show
```

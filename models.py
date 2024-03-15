import dataclasses
import decimal
import json
import sys
import time
import uuid
from datetime import date, datetime
from json import JSONEncoder
from typing import Any

import pymysql
from werkzeug.http import http_date

import settings
from utils import DataBaseUtil, ColumnUtil

HOST = settings.MYSQL_HOST
PORT = settings.MYSQL_PORT
USER = settings.MYSQL_USER
PASSWORD = settings.MYSQL_PASSWORD
DATABASE = settings.MYSQL_DATABASE
CONNECT_ATTEMPTS = settings.MYSQL_CONNECT_ATTEMPTS
CONNECT_ATTEMPTS_INTERVAL = settings.MYSQL_CONNECT_ATTEMPT_INTERVAL


class MyJSONEncoder(JSONEncoder):

    def __init__(self, *, skipkeys=..., ensure_ascii=..., check_circular=..., allow_nan=..., sort_keys=..., indent=...,
                 separators=..., default=...):
        super().__init__(skipkeys=skipkeys, ensure_ascii=False, check_circular=check_circular,
                         allow_nan=allow_nan, sort_keys=sort_keys, indent=indent, separators=separators,
                         default=default)

    def default(self, o):

        # if isinstance(o, numpy.ndarray):
        #     return o.tolist()
        if isinstance(o, bytes):
            return str(o, encoding='utf-8');

        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        if isinstance(o, date):
            return o.strftime("%Y-%m-%d")

        if isinstance(o, date):
            return http_date(o)

        if isinstance(o, (decimal.Decimal, uuid.UUID)):
            return str(o)

        if dataclasses and dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)

        if hasattr(o, "__html__"):
            return str(o.__html__())

        if hasattr(o, "__dict__"):
            return o.__dict__

        if isinstance(o, list):
            newList = []
            for item in o:
                if hasattr(item, "__dict__"):
                    newList.append(item.__dict__)
                else:
                    newList.append(item)
            return newList

        return JSONEncoder.default(self, o)


class CommonEntity:
    """
    公共实体
    """

    def set(self, params: dict):
        """
        设置属性
        :param params: 属性值
        :return:
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)


class Province(CommonEntity):
    """
    省份
    """

    @staticmethod
    def table_id() -> str:
        return 'id'

    @staticmethod
    def table_name() -> str:
        return 't_province'

    @staticmethod
    def columns() -> list:
        return ['`id`', '`name`']

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    @property
    def tableIdValue(self) -> Any:
        return self.id

    def __str__(self):
        return "Province [id=" + str(self.id) + ", name=" + str(self.name) + "]"


class City(CommonEntity):
    """
    城市
    """

    @staticmethod
    def table_id() -> str:
        return 'id'

    @staticmethod
    def table_name() -> str:
        return 't_city'

    @staticmethod
    def columns() -> list:
        return ['`id`', '`name`', '`province_id`']

    def __init__(self, id=None, name=None, provinceId=None):
        self.id = id
        self.name = name
        self.provinceId = provinceId

    @property
    def tableIdValue(self) -> Any:
        return self.id

    def __str__(self):
        return "City [id=" + str(self.id) + ", name=" + str(self.name) + ", provinceId=" + str(
            self.provinceId) + "]"


class RealTimeWeather(CommonEntity):
    """
    实时天气
    """

    @staticmethod
    def table_id() -> str:
        return 'id'

    @staticmethod
    def table_name() -> str:
        return 't_realtime_weather'

    @staticmethod
    def columns() -> list:
        return ['`id`', '`temperature`', '`weather`', '`night_weather`', '`pressure`', '`humidness`', '`precipitation`',
                '`wind`', '`update_time`']

    def __init__(self, id=None, temperature=None, weather=None, nightWeather=None, pressure=None, humidness=None,
                 precipitation=None, wind=None, updateTime=None):
        self.id = id
        self.temperature = temperature
        self.weather = weather
        self.nightWeather = nightWeather
        self.pressure = pressure
        self.humidness = humidness
        self.precipitation = precipitation
        self.wind = wind
        self.updateTime = updateTime

    @property
    def tableIdValue(self) -> Any:
        return self.id

    def __str__(self):
        return "RealTimeWeather [id=" + str(self.id) + ", temperature=" + str(
            self.temperature) + ", weather=" + str(self.weather) + ", nightWeather=" + str(
            self.nightWeather) + ", pressure=" + str(self.pressure) + ", humidness=" + str(
            self.humidness) + ", precipitation=" + str(self.precipitation) + ", wind=" + str(
            self.wind) + ", updateTime=" + str(
            self.updateTime) + "]"


class WeeklyWeather(CommonEntity):
    """
    每周天气
    """

    @staticmethod
    def table_id() -> str:
        return 'id'

    @staticmethod
    def table_name() -> str:
        return 't_weekly_weather'

    @staticmethod
    def columns() -> list:
        return ['`id`', '`city_id`', '`date`', '`weather`', '`wind_direction`', '`wind_power`', '`min_temp`',
                '`max_temp`', '`night_weather`', '`night_wind_direction`', '`night_wind_power`', '`update_time`']

    def __init__(self, id=None, cityId=None, date=None, weather=None, windDirection=None, windPower=None, minTemp=None,
                 maxTemp=None, nightWeather=None,
                 nightWindDirection=None, nightWindPower=None, updateTime=None):
        self.id = id
        self.cityId = cityId
        self.date = date
        self.weather = weather
        self.windDirection = windDirection
        self.windPower = windPower
        self.minTemp = minTemp
        self.maxTemp = maxTemp
        self.nightWeather = nightWeather
        self.nightWindDirection = nightWindDirection
        self.nightWindPower = nightWindPower
        self.updateTime = updateTime

    @property
    def tableIdValue(self) -> Any:
        return self.id

    def __str__(self):
        return "weeklyWeather [id=" + str(self.id) + ", cityId=" + str(self.cityId) + ", date=" + str(
            self.date) + ", weather=" + str(self.weather) + ", windDirection=" + str(
            self.windDirection) + ", windPower=" + str(self.windPower) + ", minTemp=" + str(
            self.minTemp) + ", maxTemp=" + str(self.maxTemp) + ", nightWeather=" + str(
            self.nightWeather) + ", nightWindDirection=" + str(
            self.nightWindDirection) + ", nightWindPower=" + str(
            self.nightWindPower) + ", updateTime=" + str(
            self.updateTime) + "]"


class DataBase:

    def __init__(self, host, port, user, password, database):
        self.db = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    # 析构函数关闭连接
    def __del__(self):
        self.closeConnection()

    def init_connection(self):
        attempts = 0
        max_attempts = CONNECT_ATTEMPTS

        while attempts < max_attempts:
            try:
                print(" * Trying to connect to MySQL")
                # 尝试连接 MySQL
                self.getConnection().ping()
                print(' * Connected to MySQL')
                break
            except pymysql.Error as e:
                print(f" * Failed to connect to MySQL: {e}")
                attempts += 1
                time.sleep(CONNECT_ATTEMPTS_INTERVAL)
        if attempts >= max_attempts:
            print(" * Failed to connect to MySQL after multiple attempts.")
            print(" * Exiting")
            sys.exit(1)

    def getConnection(self):
        if self.db is None:
            # 设置连接超时时间
            self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password,
                                      database=self.database, charset='utf8')
        return self.db

    def closeConnection(self):
        if self.db is not None and self.db.open:
            self.db.close()

    def updateById(self, data: Province | City | RealTimeWeather | WeeklyWeather) -> int:
        """
        根据id更新数据, 会忽略掉None的字段
        :param data: 要更新的数据
        :return: 更新的行数
        """
        clazz = type(data)
        table = clazz.table_name()
        dataDict = data.__dict__

        paramsColumns = []
        paramsValues = []

        # 循环字典dataDict
        for key, value in dataDict.items():
            if key != 'id' and value is not None:
                paramsColumns.append(ColumnUtil.camelcase_to_underscore(key))
                paramsValues.append(value)
        rowCount = DataBaseUtil.update(self.getConnection(), table,
                                       paramsColumns,
                                       paramsValues,
                                       [clazz.table_id()],
                                       [data.tableIdValue])
        return rowCount

    def update(self, clazz, paramsColumns, paramsValues, whereColumns, whereValues) -> int:
        """
        根据条件更新数据
        :param clazz: 类，clazz.table_name
        :param paramsColumns: 要更新的字段
        :param paramsValues: 要更新的值
        :param whereColumns: 条件字段
        :param whereValues: 条件值
        :return: 更新的行数
        """
        return DataBaseUtil.update(self.getConnection(),
                                   clazz.table_name(),
                                   paramsColumns,
                                   paramsValues,
                                   whereColumns,
                                   whereValues)

    def insert(self, data: Province | City | RealTimeWeather | WeeklyWeather) -> int:
        """
        插入数据
        :param data: 要插入的数据
        :return: 插入的行数
        """
        clazz = type(data)
        table = clazz.table_name()
        dataDict = data.__dict__
        paramsColumns = []
        paramsValues = []
        for key, value in dataDict.items():
            if value is not None:
                paramsColumns.append(ColumnUtil.camelcase_to_underscore(key))
                paramsValues.append(value)
        rowCount = DataBaseUtil.insert(self.getConnection(), table, paramsColumns, paramsValues)
        return rowCount

    def select(self, clazz, columns=None, whereColumns=None, whereValues=None) -> tuple[tuple[Any, ...], ...]:
        """
        根据条件查询数据
        :param clazz: 类，clazz.table_name clazz.columns
        :param columns: 查询的字段
        :param whereColumns: 条件字段
        :param whereValues: 条件值
        :return: 查询的数据
        """
        if columns is None:
            columns = clazz.columns()
        return DataBaseUtil.select(self.getConnection(), clazz.table_name(), columns, whereColumns, whereValues)

    def selectOne(self, clazz, columns=None, whereColumns=None, whereValues=None) -> tuple[Any, ...]:
        """
        根据条件查询一条数据
        :param clazz: 类，clazz.table_name clazz.columns
        :param columns: 查询的字段
        :param whereColumns: 条件字段
        :param whereValues: 条件值
        :return: 查询的数据
        """
        if columns is None:
            columns = clazz.columns()
        data = DataBaseUtil.select(self.getConnection(), clazz.table_name(), columns, whereColumns, whereValues)
        if data is None or len(data) == 0:
            return ()
        return data[0]

    def selectSql(self, clazz, columns=None, whereSql=None, whereValues=None):
        """
        根据sql查询数据
        :param clazz: 类，clazz.table_name
        :param columns: 查询的字段
        :param whereSql: 条件sql
        :param whereValues: 条件值
        :return: 查询的数据
        """
        if columns is None:
            columns = clazz.columns()

        sql = "select " + ",".join(columns) + " from " + clazz.table_name()
        if whereSql is not None:
            sql += " where " + whereSql
        return DataBaseUtil.execute(self.getConnection(), sql, whereValues)

    def delete(self, clazz, whereColumns, whereValues) -> int:
        """
        根据条件删除数据
        :param clazz: 类，clazz.table_name
        :param whereColumns: 条件字段
        :param whereValues: 条件值
        :return: 删除的行数
        """
        return DataBaseUtil.delete(self.getConnection(), clazz.table_name(), whereColumns, whereValues)

    def deleteById(self, clazz, id) -> int:
        """
        根据id删除数据
        :param clazz: 类，clazz.table_name,clazz.table_id
        :param id: id
        :return: 删除的行数
        """
        return DataBaseUtil.delete(self.getConnection(), clazz.table_name(), [clazz.table_id()], [id])

    def deleteSql(self, table, whereSql, whereValues=None):
        """
        根据sql删除数据
        :param table: 表名
        :param whereSql: 条件sql
        :param whereValues: 条件值
        :return: 查询的数据
        """
        sql = "delete from " + table
        if whereSql is not None:
            sql += " where " + whereSql
        return DataBaseUtil.execute(self.getConnection(), sql, whereValues)

    def count(self, clazz, whereColumns=None, whereValues=None) -> int:
        """
        根据条件查询数据条数
        :param clazz: 类，clazz.table_name
        :param whereColumns: 条件字段
        :param whereValues: 条件值
        :return: 查询的数据条数
        """
        return DataBaseUtil.count(self.getConnection(), clazz.table_name(), whereColumns, whereValues)

    def begin(self):
        """
        开启事务
        :return:
        """
        DataBaseUtil.begin(self.getConnection())

    def commit(self):
        """
        提交事务
        :return:
        """
        DataBaseUtil.commit(self.getConnection())

    def rollback(self):
        """
        回滚事务
        :return:
        """
        DataBaseUtil.rollback(self.getConnection())

    def end(self):
        """
        结束事务
        :return:
        """
        DataBaseUtil.end(self.getConnection())


# 数据库对象
dataBase = DataBase(HOST, PORT, USER, PASSWORD, DATABASE)


class R:
    """
    响应对象
    """

    def __init__(self, code: int, msg: str, data: Any = None):
        self.code = code
        self.msg = msg
        self.data = data

    @staticmethod
    def success(msg: str = "success", data: Any = None):
        return R(0, msg, data)

    @staticmethod
    def error(msg: str = "error", data: Any = None):
        return R(1, msg, data)

    def json(self):
        return json.dumps(self.__dict__, cls=MyJSONEncoder)

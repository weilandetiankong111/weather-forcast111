import datetime
from typing import Any

import pymysql
import requests
from bs4 import BeautifulSoup

import settings

headers = settings.REQUEST_HEADERS

baseUrl = settings.REQUEST_BASE_URL

getProvinceUrl = baseUrl + "web/text/HB/ABJ.html"

getCityBaseUrl = baseUrl + "web/text/"

weatherBaseUrl = baseUrl + "web/weather/"

weatherBaseApi = baseUrl + "api/now/"


class WeatherUtil:
    """
    天气工具类
    """

    @staticmethod
    def getHtml(url) -> str:
        """
        获取网页的html文本
        :param url: 链接
        :return: HtmlText
        """
        resp = requests.get(url, "lxml", headers=headers)
        resp.encoding = resp.apparent_encoding
        return resp.text

    @staticmethod
    def getJson(url, method="get", data=None, content_type="application/json") -> dict:
        """
        获取json数据
        :param url:
        :param method:
        :param data:
        :param content_type:
        :return:
        """
        resp = requests.request(
            method, url, data=data, headers={"Content-Type": content_type}
        )
        resp.encoding = resp.apparent_encoding
        return resp.json()

    @staticmethod
    def getProvinces() -> list[tuple]:
        """
        获取省份列表
        :return: (id, name) in a list
        """
        bs = BeautifulSoup(WeatherUtil.getHtml(getProvinceUrl), "lxml")
        bs.find_all("a", class_="province-item")
        provinceList = []
        for province in bs.find_all("a", class_="province-item"):
            urlsParts = province.get("href").split("/")
            provinceId = urlsParts[-2] + "/" + urlsParts[-1].split(".")[0]
            provinceName = province.get_text()
            provinceList.append((provinceId, provinceName))
        return provinceList

    @staticmethod
    def getCities(provinceId) -> list[tuple]:
        """
        获取某个省份的城市列表
        :param provinceId: 省份id  XX/XXX
        :return: (id, name) in a list
        """
        bs = BeautifulSoup(
            WeatherUtil.getHtml(getCityBaseUrl + provinceId + ".html"), "lxml"
        )
        cityList = []
        tbody = bs.find("div", class_="city-list").find("tbody")
        for tr in tbody.find_all("tr"):
            a = tr.find("a")
            cityId = a.get("href").split("/")[-1]
            if not cityId[0].isdigit():
                cityId = str(ord(cityId[0])) + cityId[1:]
            cityName = a.get_text()
            cityList.append((cityId, cityName))
        return cityList

    @staticmethod
    def getRealTimeWeather(cityId) -> dict:
        """
        获取实时天气
        :param cityId: 城市id
        :return: {
            "id": "城市id",
            "city": "城市名称",
            "temperature": "温度",
            "weather": "气象现象",
            "nightWeather": "夜间气象现象"
            "pressure": "大气压",
            "humidness": "湿度",
            "precipitation": "降水量",
            "wind": "风向风力",
            "updateTime": "更新时间"
        }
        """
        realTimeWeather = None
        respJson = WeatherUtil.getJson(weatherBaseApi + str(cityId))
        if respJson.get("code") == 0:
            bs = BeautifulSoup(
                WeatherUtil.getHtml(weatherBaseUrl + str(cityId)), "lxml"
            )

            today = bs.find("div", id="dayList").find_all("div", class_="day-item")

            weather = today[2].get_text()
            nightWeather = today[7].get_text()

            respJson = respJson["data"]
            realTimeWeather = {
                "id": respJson["location"]["id"],
                "city": respJson["location"]["name"],
                "temperature": respJson["now"]["temperature"],
                "weather": weather,
                "nightWeather": nightWeather,
                "pressure": respJson["now"]["pressure"],
                "humidness": respJson["now"]["humidity"],
                "precipitation": respJson["now"]["precipitation"],
                "wind": respJson["now"]["windDirection"]
                        + " "
                        + respJson["now"]["windScale"],
                "updateTime": respJson["lastUpdate"],
            }
        return realTimeWeather

    @staticmethod
    def getWeeklyWeather(cityId) -> list[dict]:
        """
        获取每周天气
        :param cityId:
        :return:
        """
        weeklyWeathers = []
        bs = BeautifulSoup(WeatherUtil.getHtml(weatherBaseUrl + str(cityId)), "lxml")

        updateTime = bs.find("div", class_="hd").get_text().split("（")[-1][:-3]

        for div in bs.find("div", id="dayList").find_all("div", class_="pull-left"):
            infos = div.find_all("div", class_="day-item")
            date = str(datetime.datetime.now().year) + "/" + infos[0].get_text()[3:]
            dateSplit = date.split("/")
            wid = int(str(cityId) + dateSplit[0][2:] + dateSplit[1] + dateSplit[2])
            weeklyWeathers.append(
                {
                    "id": wid,
                    "cityId": cityId,
                    "date": date,
                    "weather": infos[2].get_text(),
                    "windDirection": infos[3].get_text(),
                    "windPower": infos[4].get_text(),
                    "minTemp": infos[5].find("div", class_="low").get_text()[:-1],
                    "maxTemp": infos[5].find("div", class_="high").get_text()[:-1],
                    "nightWeather": infos[7].get_text(),
                    "nightWindDirection": infos[8].get_text(),
                    "nightWindPower": infos[9].get_text(),
                    "updateTime": updateTime,
                }
            )

        return weeklyWeathers

    # @staticmethod
    # def getWeather(cityId) -> tuple[dict, list[dict]]:
    #     """
    #     获取天气信息
    #     :param cityId:
    #     :return: (realTimeWeather, weeklyWeatherList)
    #     """
    #     weeklyWeathers = []
    #     realTimeWeather = None
    #     bs = BeautifulSoup(WeatherUtil.getHtml(weatherBaseUrl + str(cityId)), "lxml")
    #
    #     # realtime
    #     respJson = WeatherUtil.getJson(weatherBaseApi + str(cityId))
    #     if respJson.get("code") == 0:
    #         today = bs.find("div", id="dayList").find_all("div", class_="day-item")
    #
    #         weather = today[2].get_text()
    #         nightWeather = today[7].get_text()
    #
    #         respJson = respJson["data"]
    #         realTimeWeather = {
    #             "id": respJson["location"]["id"],
    #             "city": respJson["location"]["name"],
    #             "temperature": respJson["now"]["temperature"],
    #             "weather": weather,
    #             "nightWeather": nightWeather,
    #             "pressure": respJson["now"]["pressure"],
    #             "humidness": respJson["now"]["humidity"],
    #             "precipitation": respJson["now"]["precipitation"],
    #             "wind": respJson["now"]["windDirection"]
    #                     + " "
    #                     + respJson["now"]["windScale"],
    #             "updateTime": respJson["lastUpdate"],
    #         }
    #
    #     # weekly
    #     updateTime = bs.find("div", class_="hd").get_text().split("（")[-1][:-3]
    #
    #     for div in bs.find("div", id="dayList").find_all("div", class_="pull-left"):
    #         infos = div.find_all("div", class_="day-item")
    #         date = str(datetime.datetime.now().year) + "/" + infos[0].get_text()[3:]
    #         dateSplit = date.split("/")
    #         wid = int(str(cityId) + dateSplit[0][2:] + dateSplit[1] + dateSplit[2])
    #         weeklyWeathers.append(
    #             {
    #                 "id": wid,
    #                 "cityId": cityId,
    #                 "date": date,
    #                 "weather": infos[2].get_text(),
    #                 "windDirection": infos[3].get_text(),
    #                 "windPower": infos[4].get_text(),
    #                 "minTemp": infos[5].find("div", class_="low").get_text()[:-1],
    #                 "maxTemp": infos[5].find("div", class_="high").get_text()[:-1],
    #                 "nightWeather": infos[7].get_text(),
    #                 "nightWindDirection": infos[8].get_text(),
    #                 "nightWindPower": infos[9].get_text(),
    #                 "updateTime": updateTime,
    #             }
    #         )
    #
    #     return (realTimeWeather, weeklyWeathers)


class DataBaseUtil:
    """
    数据库工具类
    """

    @staticmethod
    def count(
            db: pymysql.Connection,
            table: str,
            whereColumns: list = None,
            whereValues: list = None,
    ) -> int:
        """
        查询数据量
        :param db: 数据库连接
        :param table: 表名
        :param whereColumns: 要查询的列
        :param whereValues: 要查询的值
        :return: 影响行数
        """
        cursor = db.cursor()
        sql = "SELECT COUNT(*) FROM {}".format(table)
        if whereColumns is not None:
            sql += " WHERE " + " AND ".join(
                [column + " = %s " for column in whereColumns]
            )
        db.ping(reconnect=True)
        cursor.execute(sql, whereValues)
        return cursor.fetchone()[0]

    @staticmethod
    def insert(
            db: pymysql.Connection, table: str, paramColumns: list, paramValues: list
    ) -> int:
        """
        插入数据
        :param db: 数据库连接
        :param table: 表名
        :param paramColumns: 要插入的列
        :param paramValues: 要插入的值
        :return: 影响行数
        """
        cursor = db.cursor()
        sql = (
                "INSERT INTO "
                + table
                + " ("
                + ",".join(paramColumns)
                + ") VALUES ("
                + ",".join(["%s"] * len(paramColumns))
                + ")"
        )
        try:
            db.ping(reconnect=True)
            cursor.execute(sql, paramValues)
            db.commit()
            return cursor.rowcount
        except Exception as e:
            db.rollback()
            print(e)

    @staticmethod
    def update(
            db: pymysql.Connection,
            table: str,
            paramColumns: list,
            paramValues: list,
            whereColumns: list,
            whereValues: list,
    ) -> int:
        """
        更新数据
        :param db: 数据库连接
        :param table: 表名
        :param paramColumns: 要更新的列
        :param paramValues: 要更新的值
        :param whereColumns: 要更新的条件列
        :param whereValues: 要更新的条件值
        :return: 影响行数
        """
        cursor = db.cursor()
        sql = (
                "UPDATE "
                + table
                + " SET "
                + ",".join([paramColumns[i] + " = %s" for i in range(len(paramColumns))])
                + " WHERE "
                + " AND ".join(
            [whereColumns[i] + " = %s" for i in range(len(whereColumns))]
        )
        )
        try:
            db.ping(reconnect=True)
            cursor.execute(sql, paramValues + whereValues)
            db.commit()
            return cursor.rowcount
        except Exception as e:
            db.rollback()
            print(e)

    @staticmethod
    def delete(
            db: pymysql.Connection, table: str, whereColumns: list, whereValues: list
    ) -> int:
        """
        删除数据
        :param db: 数据库连接
        :param table: 表名
        :param whereColumns: 要删除的条件列
        :param whereValues: 要删除的条件值
        :return: 影响行数
        """
        cursor = db.cursor()
        sql = (
                "DELETE FROM "
                + table
                + " WHERE "
                + " AND ".join(
            [whereColumns[i] + " = %s" for i in range(len(whereColumns))]
        )
        )
        try:
            db.ping(reconnect=True)
            cursor.execute(sql, whereValues)
            db.commit()
            return cursor.rowcount
        except Exception as e:
            db.rollback()
            print(e)

    @staticmethod
    def select(
            db: pymysql.Connection,
            table: str,
            columns: list,
            whereColumns: list = None,
            whereValues: list = None,
    ) -> tuple[tuple[Any, ...], ...]:
        """
        查询数据
        :param db: 数据库连接
        :param table: 表名
        :param columns: 查询的列
        :param whereColumns: 要查询的条件列
        :param whereValues: 要查询的条件值
        :return: 查询结果
        """
        curorsor = db.cursor()
        sql = "SELECT " + ",".join(columns) + " FROM " + table
        if whereColumns is not None:
            sql += " WHERE " + " AND ".join(
                [whereColumns[i] + " = %s " for i in range(len(whereColumns))]
            )
        try:
            db.ping(reconnect=True)
            curorsor.execute(sql, whereValues)
            return curorsor.fetchall()
        except Exception as e:
            print(e)

    @staticmethod
    def selectOne(
            db: pymysql.Connection,
            table: str,
            columns: list,
            whereColumns: list,
            whereValues: list,
    ) -> tuple[Any, ...]:
        """
        查询单条数据
        :param db: 数据库连接
        :param table: 表名
        :param columns: 查询的列
        :param whereColumns: 要查询的条件列
        :param whereValues: 要查询的条件值
        :return: 查询结果
        """
        curorsor = db.cursor()
        sql = (
                "SELECT "
                + ",".join(columns)
                + " FROM "
                + table
                + " WHERE "
                + " AND ".join(
            [whereColumns[i] + " = %s" for i in range(len(whereColumns))]
        )
        )
        try:
            db.ping(reconnect=True)
            curorsor.execute(sql, whereValues)
            return curorsor.fetchone()
        except Exception as e:
            print(e)

    @staticmethod
    def begin(db: pymysql.Connection):
        """
        开启事务
        :param db: 数据库连接
        :return:
        """
        db.ping(reconnect=True)
        db.autocommit(False)

    @staticmethod
    def commit(db: pymysql.Connection):
        """
        提交事务
        :param db: 数据库连接
        :return:
        """
        db.ping(reconnect=True)
        db.commit()

    @staticmethod
    def rollback(db: pymysql.Connection):
        """
        回滚事务
        :param db: 数据库连接
        :return:
        """
        db.ping(reconnect=True)
        db.rollback()

    @staticmethod
    def end(db: pymysql.Connection):
        """
        结束事务
        :param db: 数据库连接
        :return:
        """
        db.ping(reconnect=True)
        db.autocommit(True)

    @staticmethod
    def execute(db: pymysql.Connection, sql: str, values: list = None) -> tuple[tuple[Any, ...], ...] | int:
        """
        执行sql语句
        :param db: 数据库连接
        :param sql: sql语句
        :param values: sql语句中的参数
        :return: 影响行数或数据
        """
        cursor = db.cursor()
        try:
            db.ping(reconnect=True)
            cursor.execute(sql, values)
            db.commit()
            if sql.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            return cursor.rowcount
        except Exception as e:
            db.rollback()
            print(e)


class ColumnUtil:
    """
    数据库列名转换工具类
    """

    @staticmethod
    def camelcase_to_underscore(string: str) -> str:
        result = ""
        for char in string:
            if char.isupper():
                result += "_" + char.lower()
            else:
                result += char
        return result[1:] if result.startswith("_") else result

    @staticmethod
    def underscore_to_camelcase(string: str) -> str:
        result = ""
        upper = False
        for i, char in enumerate(string):
            if char == "_":
                upper = True
            else:
                if upper:
                    result += char.upper()
                    upper = False
                else:
                    result += char
        return result

    @staticmethod
    def remove_backticks(string):
        if string.startswith("`"):
            string = string[1:]

        if string.endswith("`"):
            string = string[:-1]

        return string

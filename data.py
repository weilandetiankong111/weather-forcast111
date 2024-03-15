import time
from datetime import datetime, timedelta

import settings
from models import Province, City, RealTimeWeather, WeeklyWeather, dataBase
from services import provinceService, cityService, realTimeWeatherService, weeklyWeatherService
from utils import WeatherUtil

REQUEST_INTERVAL = settings.REQUEST_INTERVAL
PROGRESS_BAR_LENGTH = settings.PROGRESS_BAR_LENGTH


def printProgress(nowProgress, maxProgress, newline=False):
    """
    打印进度条
    :param newline:
    :param nowProgress: 当前进度
    :param maxProgress: 最大进度
    :return
    """
    rate = nowProgress / maxProgress
    progress = round(rate * PROGRESS_BAR_LENGTH)
    print(f"\r\t[{'=' * progress}{'-' * (PROGRESS_BAR_LENGTH - progress)}] {rate * 100:.2f}% ",
          end='')
    if newline:
        print(end='\n')


def init_province_data() -> list[Province]:
    """
    初始化省份数据
    :return: 省份列表
    """

    printProgress(0, 1)

    provinceTupleList = WeatherUtil.getProvinces()
    ret = []

    try:
        dataBase.begin()
        length = len(provinceTupleList)
        for i, provinceTuple in enumerate(provinceTupleList):
            time.sleep(REQUEST_INTERVAL)
            printProgress(i, length)

            province = Province(provinceTuple[0], provinceTuple[1])
            ret.append(province)
            provinceService.save(province)
        dataBase.commit()
        printProgress(1, 1, True)
        return ret
    except Exception as e:
        dataBase.rollback()
        print(e)


def init_city_data(provinces: list[Province]) -> list[City]:
    """
    初始化城市数据
    :param provinces: 省份列表
    :return: 城市列表
    """
    printProgress(0, 1)
    i = 0
    length = 2428

    ret = []
    for province in provinces:
        cityTupleList = WeatherUtil.getCities(province.id)

        try:
            dataBase.begin()
            for cityTuple in cityTupleList:
                time.sleep(REQUEST_INTERVAL)
                printProgress(i, length)
                i += 1

                city = City(cityTuple[0], cityTuple[1], province.id)
                ret.append(city)
                cityService.save(city)
            dataBase.commit()
        except Exception as e:
            dataBase.rollback()
            print(e)
    printProgress(1, 1, True)
    return ret


def init_realtime_weather_data(citys: list[City]):
    """
    初始化实时天气数据
    :param citys: 城市列表
    :return:
    """

    printProgress(0, 1)

    try:
        dataBase.begin()
        length = len(citys)
        for i, city in enumerate(citys):
            time.sleep(REQUEST_INTERVAL)
            printProgress(i, length)

            json = WeatherUtil.getRealTimeWeather(city.id)
            rtw = RealTimeWeather(city.id, json['temperature'], json['weather'], json['nightWeather'], json['pressure'],
                                  json['humidness'], json['precipitation'], json['wind'], json['updateTime'])
            realTimeWeatherService.save(rtw)
        dataBase.commit()
        printProgress(1, 1, True)
    except Exception as e:
        dataBase.rollback()
        print(e)


def init_weekly_weather_data(citys: list[City]):
    """
    初始化每周天气数据
    :param citys: 城市列表
    :return:
    """

    printProgress(0, 1)
    i = 0
    length = 2428 * 7

    for city in citys:
        weeklyWeathers = WeatherUtil.getWeeklyWeather(city.id)
        try:
            dataBase.begin()
            for weeklyWeather in weeklyWeathers:
                time.sleep(REQUEST_INTERVAL)
                printProgress(i, length)
                i += 1

                ww = WeeklyWeather(weeklyWeather['id'], weeklyWeather['cityId'], weeklyWeather['date'],
                                   weeklyWeather['weather'],
                                   weeklyWeather['windDirection'], weeklyWeather['windPower'], weeklyWeather['minTemp'],
                                   weeklyWeather['maxTemp'], weeklyWeather['nightWeather'],
                                   weeklyWeather['nightWindDirection'],
                                   weeklyWeather['nightWindPower'], weeklyWeather['updateTime'])
                weeklyWeatherService.save(ww)
            dataBase.commit()
        except Exception as e:
            dataBase.rollback()
            print(e)
    printProgress(1, 1, True)


def init_data():
    print("begin data init...")

    print(" * 1/2 Init Province Data: ")
    provinces = provinceService.list()
    provinces = init_province_data() if provinces is None or len(provinces) < 34 else provinces
    print('Done!')

    print(" * 2/2 Init City Data: ")
    citys = cityService.list()
    citys = init_city_data(provinces) if citys is None or len(citys) < 2428 else citys
    print('Done!')

    # print(" * 3/4 Init RealTimeWeather Data: ")
    # init_realtime_weather_data(citys)
    # print('Done!')
    #
    # print(" * 4/4 Init WeeklyWeather Data: ")
    # init_weekly_weather_data(citys)
    # print('Done!')

    print("data init finished.")


def getRealTimeWeather(cityId) -> RealTimeWeather:
    """
    获取实时天气,并按计划更新
    :param cityId: 城市ID
    :return:
    """

    # 获取实时天气
    rtw = realTimeWeatherService.getById(cityId)
    # 如果实时天气不存在，则从网络获取，并保存
    if rtw is None:
        rtw = RealTimeWeather()
        rtw.set(WeatherUtil.getRealTimeWeather(cityId))
        realTimeWeatherService.save(rtw)
    else:
        # 如果实时天气更新时间超过2小时，则从网络获取，并保存
        if rtw.updateTime is not None and datetime.now() - rtw.updateTime > timedelta(hours=2):
            rtw = RealTimeWeather()
            rtw.set(WeatherUtil.getRealTimeWeather(cityId))
            realTimeWeatherService.updateById(rtw)
    return rtw


def getWeeklyWeather(cityId) -> list[WeeklyWeather]:
    """
    获取每周天气，并按计划更新
    :param cityId: 城市ID
    :return:
    """
    weeklyWeathers = weeklyWeatherService.list7Day(cityId)

    # 如果数量小于7，直接更新这7天的数据；或者如果更新时间超过4小时，则更新
    if len(weeklyWeathers) < 7 or (
            weeklyWeathers[0].updateTime is not None and datetime.now() - weeklyWeathers[0].updateTime > timedelta(
            hours=4)):
        # 开启事物
        dataBase.begin()
        # 删除 7天的
        weeklyWeatherService.remove7Day(cityId)
        newWeeklyWeathers = []
        # 再保存7天的
        for wwDict in WeatherUtil.getWeeklyWeather(cityId):
            ww = WeeklyWeather()
            ww.set(wwDict)
            newWeeklyWeathers.append(ww)
            weeklyWeatherService.save(ww)
        dataBase.commit()
        dataBase.end()
        weeklyWeathers = newWeeklyWeathers

    return weeklyWeathers

from models import DataBase, dataBase, Province, City, RealTimeWeather, WeeklyWeather
from utils import ColumnUtil


class CommonService:
    def __init__(self, db: DataBase, clazz):
        self.__db = db
        self.__clazz = clazz
        self.__underscoreColumns = [ColumnUtil.remove_backticks(column) for column in self.__clazz.columns()]
        self.__camelcaseColumns = [ColumnUtil.underscore_to_camelcase(column) for column in self.__underscoreColumns]

    @property
    def thisClass(self):
        return self.__clazz

    @property
    def db(self) -> DataBase:
        return self.__db

    def package(self, values: tuple) -> thisClass:
        """
        将数据库查询结果转换为对象
        :param values: 数据库查询结果
        :return: 对象
        """
        if values is None:
            return None
        obj = self.thisClass()
        for i, value in enumerate(values):
            obj.__dict__[self.__camelcaseColumns[i]] = value
        return obj

    def save(self, data: Province | City | RealTimeWeather | WeeklyWeather) -> int:
        """
        保存数据
        :param data: 要保存的数据
        :return: 保存成功返回1，否则返回0
        """
        return self.db.insert(data)

    def updateById(self, data: Province | City | RealTimeWeather | WeeklyWeather) -> int:
        """
        根据id更新数据
        :param data: 要更新的数据
        :return: 更新成功返回1，否则返回0
        """
        return self.db.updateById(data)

    def saveOrUpdate(self, data: Province | City | RealTimeWeather | WeeklyWeather) -> int:
        """
        无ID保存或有ID更新数据
        :param data: 要保存或更新的数据
        :return: 保存或更新成功返回1，否则返回0
        """
        if data.tableIdValue is None:
            return self.save(data)
        else:
            return self.updateById(data)

    def getById(self, id: int) -> thisClass:
        """
        根据id获取
        :param id: id
        :return:
        """
        one = self.db.selectOne(self.thisClass, whereColumns=[self.thisClass.table_id()], whereValues=[id])
        if one is None or len(one) == 0:
            return None
        return self.package(one)

    def list(self, whereColumns=None, whereValues=None) -> list[thisClass]:
        """
        获取列表
        :param whereColumns: 查询条件
        :param whereValues: 查询条件值
        :return: 列表
        """
        dataList = self.db.select(self.thisClass, whereColumns=whereColumns, whereValues=whereValues)
        if dataList is None:
            return []
        return [self.package(one) for one in dataList]

    def removeById(self, id: int) -> int:
        """
        根据id删除
        :param id: id
        :return: 删除成功返回1，否则返回0
        """
        return self.db.deleteById(self.thisClass, id)

    def remove(self, whereColumns=None, whereValues=None) -> int:
        """
        根据条件删除
        :param whereColumns: 查询条件
        :param whereValues: 查询条件值
        :return: 删除成功返回1，否则返回0
        """
        return self.db.delete(self.thisClass, whereColumns, whereValues)

    def update(self, paramsColumns, paramsValues, whereColumns, whereValues) -> int:
        """
        根据条件更新数据
        :param paramsColumns: 要更新的字段
        :param paramsValues: 要更新的值
        :param whereColumns: 条件字段
        :param whereValues: 条件值
        :return: 更新的行数
        """
        return self.db.update(self.thisClass, paramsColumns, paramsValues, whereColumns, whereValues)

    def count(self, whereColumns=None, whereValues=None) -> int:
        """
        根据条件获取数量
        :param whereColumns: 查询条件
        :param whereValues: 查询条件值
        :return: 数量
        """
        return self.db.count(self.thisClass, whereColumns, whereValues)


class ProvinceService(CommonService):
    """
    省份服务
    """

    def __init__(self, db: DataBase):
        super().__init__(db, Province)


class CityService(CommonService):
    """
    城市服务
    """

    def __init__(self, db: DataBase):
        super().__init__(db, City)


class RealTimeWeatherService(CommonService):
    """
    实时天气服务
    """

    def __init__(self, db: DataBase):
        super().__init__(db, RealTimeWeather)


class WeeklyWeatherService(CommonService):
    """
    每周天气服务
    """

    def __init__(self, db: DataBase):
        super().__init__(db, WeeklyWeather)

    def list7Day(self, cityId: int) -> list[WeeklyWeather]:
        """
        获取今天起7天的天气
        :param cityId: 城市id
        :return: 天气列表
        """
        whereSql = " `city_id` = %s and `date` >= CURDATE() AND `date` <= DATE_ADD(CURDATE(), INTERVAL 6 DAY) ORDER BY date ASC"
        whereValues = [cityId]
        data = self.db.selectSql(self.thisClass, self.thisClass.columns(), whereSql, whereValues)
        if data is None:
            return []
        return [self.package(one) for one in data]

    def remove7Day(self, cityId: int) -> int:
        """
        删除今天起7天的天气
        :param cityId: 城市id
        :return: 删除的行数
        """
        whereSql = " `city_id` = %s and `date` >= CURDATE() AND `date` <= DATE_ADD(CURDATE(), INTERVAL 6 DAY) "
        whereValues = [cityId]
        return self.db.deleteSql(self.thisClass.table_name(), whereSql, whereValues)


# 实例化服务
provinceService = ProvinceService(dataBase)
cityService = CityService(dataBase)
realTimeWeatherService = RealTimeWeatherService(dataBase)
weeklyWeatherService = WeeklyWeatherService(dataBase)

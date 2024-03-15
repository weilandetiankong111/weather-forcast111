# TEST

import datetime
import json
import time

from models import Province, City, MyJSONEncoder
from services import cityService
from utils import WeatherUtil
import data


def test_common_entity():
    p = Province()
    print(p)
    p.set({'id': 1, 'name': '北京', 'citys': [1, 2, 3]})
    print(p)


if __name__ == '__main__':
    # test_common_entity()
    c = City(id=1, name='北京', provinceId=1)
    # print(json.dumps(c.__dict__, cls=MyJSONEncoder))
    # print(json.dumps([123, 312, 'asd', {'a': 1}, c], cls=MyJSONEncoder))

    l = cityService.list(['province_id'], ["HN/AGD"])
    print(l)
    print(type(l))
    print(json.dumps(l, cls=MyJSONEncoder))

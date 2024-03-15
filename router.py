import os

from flask import Blueprint, render_template, send_from_directory, request

import data
from models import R
from services import provinceService, cityService

router = Blueprint('router', __name__)


@router.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(router.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@router.route('/')
def index():
    # 北京ID 54511
    cityId = 54511
    return render_template('index.html',
                           realtimeWeather=data.getRealTimeWeather(cityId),
                           provinceList=provinceService.list(),
                           cityList=cityService.list(),
                           cityName=cityService.getById(cityId).name)


@router.route('/weather/city/<cityId>')
def weather(cityId):
    city = cityService.getById(cityId)
    if city is None:
        return render_template('error/404.html')
    return render_template('weather.html',
                           cityName=city.name,
                           realtimeWeather=data.getRealTimeWeather(cityId),
                           weeklyWeatherList=data.getWeeklyWeather(cityId)
                           )


@router.route('/api/city')
def city():
    # 获取链接参数provinceId
    provinceId = request.args.get('provinceId')
    return R.success(data=cityService.list(['province_id'], [provinceId])).json()


@router.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html')

@router.errorhandler(400)
def bad_request(e):
    return render_template('error/400.html')

@router.errorhandler(403)
def forbidden(e):
    return render_template('error/403.html')

@router.errorhandler(405)
def method_not_allowed(e):
    return render_template('error/405.html')

@router.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html')

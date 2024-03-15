from flask import Flask
from gevent import pywsgi

import data
import settings
from logo import LOGO
from models import dataBase
from router import router

app = Flask(__name__)

app.register_blueprint(router, url_prefix='/')

app.jinja_env.block_start_string = '(%'  # 修改块开始符号
app.jinja_env.block_end_string = '%)'  # 修改块结束符号
app.jinja_env.variable_start_string = '(('  # 修改变量开始符号
app.jinja_env.variable_end_string = '))'  # 修改变量结束符号
app.jinja_env.comment_start_string = '(#'  # 修改注释开始符号
app.jinja_env.comment_end_string = '#)'  # 修改注释结束符号

host = settings.SERVER_HOST
port = settings.SERVER_PORT
debug = settings.DEBUG

if __name__ == '__main__':
    print(LOGO)
    dataBase.init_connection()
    data.init_data()
    # app.run(host=host, port=port, debug=debug)
    print(' * Server running on http://' + host + ':' + str(port))
    pywsgi.WSGIServer((host, port), app).serve_forever()

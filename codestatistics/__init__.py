from flask import Flask
from .views.account import account
from .views.index import ind


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')
    # 注册的是蓝图对象
    app.register_blueprint(account)
    app.register_blueprint(ind)
    # app.register_blueprint(sd)
    # app.register_blueprint(ind)
    # app.register_blueprint(up)
    return app
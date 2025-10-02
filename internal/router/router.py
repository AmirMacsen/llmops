from  dataclasses import dataclass

from flask import Flask, Blueprint

from internal.handler import AppHandler
from injector import inject


@inject
@dataclass
class Router:
    app_handler: AppHandler

    def register_router(self, app:Flask):
        """注册路由"""

        # 1. 创建蓝图
        bp = Blueprint('llmops', __name__, url_prefix='')

        # 2. 把url与对应的控制器方法绑定
        bp.add_url_rule('/ping', view_func=self.app_handler.ping)
        bp.add_url_rule('/completion', view_func=self.app_handler.completion, methods=['POST'])

        # 3. 注册蓝图
        app.register_blueprint(bp)

import os

from flask import Flask

from internal.exception import CustomException
from internal.router import Router
from config import Config
from pkg.response import Response, json, HttpCode
from internal.model.app import App
from pkg.sqlalchemy import SQLAlchemy



class Http(Flask):
    """http服务器"""
    def __init__(self, *args,config: Config, db:SQLAlchemy,router:Router, **kwargs):
        super(Http, self).__init__(*args, **kwargs)

        # 加载配置
        self.config.from_object(config)

        # 异常处理
        self.register_error_handler(Exception, self._register_error_handler)

        # 初始化数据库
        db.init_app(self)
        with self.app_context():
            _ = App()
            db.create_all()

        # 注册路由
        router.register_router(self)


    def _register_error_handler(self, error:Exception):
        """注册异常处理函数"""
        # 判断异常信息是否是自定义异常
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if hasattr(error, 'data') else None,
            ))
        # 如果不是自定义，比如数据库异常等，提取信息，返回FAIL状态
        if self.debug or os.environ.get('DEBUG'):
            raise error
        return json(Response(
            code=HttpCode.FAIL,
            message=str(error),
            data={}
        ))

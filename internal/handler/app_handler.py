import dataclasses
import os
import uuid

from flask import request
from injector import inject
from openai import OpenAI

from internal.model import App
from internal.schema.app_schema import CompletionRequest
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message

@inject
@dataclasses.dataclass
class AppHandler(object):
    """应用处理类"""

    app_service: AppService

    def create_app(self):
        """
        创建应用
        :return:
        """
        app = self.app_service.create_app()
        return success_message(f"应用已经成功创建，id为{app.id}")

    def get_app(self, app_id:uuid.UUID):
        """
        获取应用
        :param app_id: 应用id
        :return:
        """
        if not app_id:
            return validate_error_json(errors={'app_id': '应用id不能为空'})

        app = self.app_service.get_app(app_id)
        return success_message(f"应用已经成功找到，名字为{app.name}")


    def update_app(self, app_id:uuid.UUID) -> App:
        """
        更新应用
        :param app_id: 应用id
        :return:
        """
        app = self.app_service.update_app(app_id)
        return success_message(f"应用已经成功更新，名字为{app.name}")


    def delete_app(self, app_id:uuid.UUID):
        self.app_service.delete_app(app_id)
        return success_message(f"应用已经成功删除")

    def  completion(self):
        """
        聊天接口
        :return:
        """
        req = CompletionRequest()
        if not req.validate():
            return validate_error_json(errors=req.errors)
        query = request.json.get('query')

        client = OpenAI(
            base_url=os.getenv('OPENAI_API_BASE_URL'),
            api_key=os.getenv('OPENAI_API_KEY'),
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是OpenAI开发的助手."},
                {"role": "user", "content": query},
            ],
        )

        return success_json(response.choices[0].message.content)

    def ping(self):
        """测试方法"""
        return "pong"

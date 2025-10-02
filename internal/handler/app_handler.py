import os

from flask import request
from openai import OpenAI
from internal.schema.app_schema import CompletionRequest


class AppHandler(object):
    """应用处理类"""

    def  completion(self):
        """
        聊天接口
        :return:
        """
        req = CompletionRequest()
        if not req.validate():
            return req.errors
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

        return response.choices[0].message.content

    def ping(self):
        """测试方法"""
        return "pong"

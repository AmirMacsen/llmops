import os

from flask import request
from flask.cli import load_dotenv
from openai import OpenAI


class AppHandler(object):
    """应用处理类"""

    def completion(self):
        """
        聊天接口
        :return:
        """
        load_dotenv()
        query = request.json.get('query')

        client = OpenAI(
            base_url=os.getenv('OPENAI_API_URL'),
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是OpenAI开发的助手."},
                {"role": "user", "content": query},
            ],
        )

        print(response)
        return response.choices[0].message.content

    def ping(self):
        """测试方法"""
        return "pong"

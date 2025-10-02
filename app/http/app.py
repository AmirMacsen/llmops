from dotenv import load_dotenv
from injector import Injector

from internal.router import Router
from internal.server import Http
from config import Config



load_dotenv(dotenv_path='.env')

config = Config()
injector = Injector()

app = Http(__name__, config=config, router=injector.get(Router))

if __name__ == '__main__':
    app.run(debug=True)

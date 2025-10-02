from dotenv import load_dotenv
from injector import Injector

from internal.router import Router
from internal.server import Http

load_dotenv()

injector = Injector()

app = Http(__name__, router=injector.get(Router))

if __name__ == '__main__':
    app.run(debug=True)

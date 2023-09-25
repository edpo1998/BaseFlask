# Utils
from colorama import Fore
from  dotenv import load_dotenv

# Flask
from flask import Flask
from flask_cors import CORS 

def make_app():
    from core import db, migrate, jwt, conf
    from apis import api
    app = Flask(__name__)
    print(Fore.CYAN, '* ENVIRONMENT: ', conf.ENV_NAME, Fore.RESET)
    app.config.from_object(conf)
    cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    api.init_app(app)
    return app

if __name__ == '__main__':
    load_dotenv('.env')
    app = make_app()
    app.run(port=8000 )
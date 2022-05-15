from flask import Flask

from .common import DATABASE_PATH
from .database.db_session import global_init

global_init(DATABASE_PATH)

from . import skin_api

app = Flask(__name__)


def main():
    app.register_blueprint(skin_api.blueprint)
    app.run()


if __name__ == "__main__":
    main()

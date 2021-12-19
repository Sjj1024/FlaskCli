from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object(Config)

# 初始化数据库
db = SQLAlchemy()
db.init_app(app)


@app.route("/")
def index():
    return "首页"


if __name__ == '__main__':
    app.run()
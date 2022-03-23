from datetime import datetime

from . import db


class User(db.Model):
    """用户"""
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称

    def __repr__(self):
        return '<User %r>' % self.nick_name
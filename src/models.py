from . import db


class User(db.Model):
    """用户"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称

    def __repr__(self):
        """
        格式化输出
        """
        return '<User %r>' % self.nick_name

    def to_json(self):
        """
        为了转json提供的方法
        """
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict

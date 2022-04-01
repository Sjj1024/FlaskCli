import datetime

from . import db


class BaseModel(object):
    __tablename__ = "users"

    def __repr__(self):
        """
        格式化输出
        """
        return f"{self.__tablename__}: {self.to_json()}"

    def to_json(self):
        """
        为了转json提供的方法
        """
        _dict = self.__dict__
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class User(db.Model, BaseModel):
    """用户"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    user_name = db.Column(db.String(255), unique=True, nullable=False)  # 用户名
    password = db.Column(db.String(255), unique=False, nullable=True)  # 用户密码
    nick_name = db.Column(db.String(255), unique=False, nullable=True)  # 用户昵称
    email = db.Column(db.String(255), unique=False, nullable=True)  # 用户邮箱
    phone = db.Column(db.String(255), unique=False, nullable=True)  # 用户手机号
    gender = db.Column(db.String(255), unique=False, nullable=True)  # 用户性别
    signature = db.Column(db.String(255), unique=False, nullable=True)  # 用户签名
    head_img = db.Column(db.String(255), unique=False, nullable=True)  # 用户头像链接
    creat_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 用户创建时间
    role_id = db.Column(db.Integer, unique=True, nullable=False)  # 角色id


class Categorys(db.Model, BaseModel):
    """文章分类"""
    __tablename__ = "categorys"
    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    category = db.Column(db.String(255), unique=True, nullable=False)  # 分类名称
    parent_id = db.Column(db.Integer, nullable=True)  # 父分类id
    creat_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 创建时间


class Roles(db.Model, BaseModel):
    """角色权限管理"""
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)  # 角色编号
    role = db.Column(db.String(255), unique=True, nullable=False)  # 角色名称
    authority = db.Column(db.ARRAY(db.String(255)), nullable=True)  # 角色权限

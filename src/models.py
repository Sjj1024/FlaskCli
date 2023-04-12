import datetime
from copy import deepcopy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
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
        _dict = deepcopy(self.__dict__)
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        # 将创建时间和更新时间格式化
        for (key, value) in _dict.items():
            if isinstance(value, datetime.date):
                # _dict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                _dict[key] = value.strftime("%Y-%m-%d %H:%M")
        return _dict

    def to_dict(self):
        """
        为了转json提供的方法
        """
        _dict = deepcopy(self.__dict__)
        if "_sa_instance_state" in _dict:
            del _dict["_sa_instance_state"]
        return _dict


class User(db.Model, BaseModel):
    """用户"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    user_name = db.Column(db.String(255), unique=True, nullable=False)  # 用户名
    password_hash = db.Column(db.String(255), unique=False, nullable=True, name="password")  # 用户密码
    nick_name = db.Column(db.String(255), unique=False, nullable=True)  # 用户昵称
    email = db.Column(db.String(255), unique=False, nullable=True)  # 用户邮箱
    phone = db.Column(db.String(255), unique=False, nullable=True)  # 用户手机号
    gender = db.Column(db.String(255), unique=False, nullable=True)  # 用户性别
    signature = db.Column(db.String(255), unique=False, nullable=True)  # 用户签名
    head_img = db.Column(db.String(255), unique=False, nullable=True)  # 用户头像链接
    creat_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 用户创建时间
    role_id = db.Column(db.Integer, unique=True, nullable=False)  # 角色id

    @property
    def password(self):
        # 一定要有这个属性，即便这个属性不允许访问
        raise Exception("密码不能被访问")

    # 赋值password，则自动加密存储。
    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    # 使用check_password,进行密码校验，返回True False。
    def check_password(self, pasword):
        return check_password_hash(self.password_hash, pasword)


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


class Collector(db.Model, BaseModel):
    """表信息记录"""
    __tablename__ = "collector"
    id = db.Column(db.Integer, primary_key=True)  # 序号
    uuid = db.Column(db.String(255), unique=True, nullable=False)  # 唯一id
    table_name = db.Column(db.String(255), unique=False, nullable=True)  # 表名称
    extra = db.Column(db.JSON, unique=False, nullable=True)  # jsonschema
    enable = db.Column(db.Boolean, unique=False, nullable=True)  # 是否可用
    description = db.Column(db.String(255), unique=False, nullable=True)  # 描述信息
    count = db.Column(db.Integer, unique=False, nullable=True)  # 所有数量统计
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 创建时间
    update_time = db.Column(db.DateTime, default=datetime.datetime.now)  # 更新时间
    account_id = db.Column(db.Integer, unique=True, nullable=False)  # 拥有者id


class CaoliuUsers(db.Model, BaseModel):
    """表信息记录"""
    __tablename__ = "caoliu_users"
    id = db.Column(db.Integer, primary_key=True)  # 序号
    user_name = db.Column(db.String(255), unique=True, nullable=False)  # 唯一id
    user_id = db.Column(db.Integer, unique=False, nullable=True)  # 所有数量统计
    password = db.Column(db.String(255), unique=False, nullable=True)  # 表名称
    grade = db.Column(db.String(255), unique=False, nullable=True)  # jsonschema
    email = db.Column(db.String(255), unique=False, nullable=True)  # 是否可用
    weiwang = db.Column(db.String(255), unique=False, nullable=True)  # 描述信息
    article_number = db.Column(db.Integer, unique=False, nullable=True)
    contribute = db.Column(db.String(255), unique=False, nullable=True)
    desc = db.Column(db.String(255), unique=False, nullable=True)
    creat_time = db.Column(db.DateTime(), default=datetime.datetime.now())  # 添加时间
    regist_time = db.Column(db.DateTime(), default=datetime.datetime.now())  # 账号注册时间
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now())  # 更新时间
    money = db.Column(db.Integer, unique=True, nullable=False)  # 拥有的金钱
    cookie = db.Column(db.String(500), unique=False, nullable=True)
    user_agent = db.Column(db.String(255), unique=False, nullable=True)
    current_money = db.Column(db.Integer, unique=False, nullable=True)  # 活期
    regular_money = db.Column(db.Integer, unique=False, nullable=True)  # 定期
    able_invate = db.Column(db.String(255), unique=False, nullable=True)
    lease = db.Column(db.String(255), unique=False, nullable=True)
    authentication = db.Column(db.String(255), unique=False, nullable=True)
    contribute_link = db.Column(db.String(255), unique=False, nullable=True)
    task_link = db.Column(db.String(255), unique=False, nullable=True)
    task_file_sha = db.Column(db.String(255), unique=False, nullable=True)
    check_link = db.Column(db.String(255), unique=False, nullable=True)
    check_file_sha = db.Column(db.String(255), unique=False, nullable=True)
    new_passwd = db.Column(db.String(255), unique=False, nullable=True)
    task_status = db.Column(db.String(255), unique=False, nullable=True)
    check_status = db.Column(db.String(255), unique=False, nullable=True)
    isDeleted = db.Column(db.Boolean, unique=False, nullable=True)
    important = db.Column(db.Integer, unique=False, nullable=True)
    original = db.Column(db.JSON, unique=False, nullable=True)
    sign_task_id = db.Column(db.String(255), unique=False, nullable=True)
    sign_task_status = db.Column(db.String(255), unique=False, nullable=True)


class Tang98Users(db.Model, BaseModel):
    """表信息记录"""
    __tablename__ = "tang_users"
    id = db.Column(db.Integer, primary_key=True)  # 序号
    user_name = db.Column(db.String(255), unique=True, nullable=False)  # 唯一id
    user_id = db.Column(db.Integer, unique=False, nullable=True)  # 所有数量统计
    password = db.Column(db.String(255), unique=False, nullable=True)  # 表名称
    grade = db.Column(db.String(255), unique=False, nullable=True)  # jsonschema
    email = db.Column(db.String(255), unique=False, nullable=True)  # 是否可用
    weiwang = db.Column(db.String(255), unique=False, nullable=True)  # 描述信息
    article_number = db.Column(db.Integer, unique=False, nullable=True)
    contribute = db.Column(db.String(255), unique=False, nullable=True)
    desc = db.Column(db.String(255), unique=False, nullable=True)
    creat_time = db.Column(db.DateTime(), default=datetime.datetime.now())  # 添加时间
    regist_time = db.Column(db.DateTime(), default=datetime.datetime.now())  # 账号注册时间
    update_time = db.Column(db.DateTime(), default=datetime.datetime.now())  # 更新时间
    money = db.Column(db.Integer, unique=True, nullable=False)  # 拥有的金钱
    cookie = db.Column(db.String(5000), unique=False, nullable=True)
    user_agent = db.Column(db.String(255), unique=False, nullable=True)
    current_money = db.Column(db.Integer, unique=False, nullable=True)
    regular_money = db.Column(db.Integer, unique=False, nullable=True)
    able_invate = db.Column(db.String(255), unique=False, nullable=True)
    lease = db.Column(db.String(255), unique=False, nullable=True)
    authentication = db.Column(db.String(255), unique=False, nullable=True)
    contribute_link = db.Column(db.String(255), unique=False, nullable=True)
    task_link = db.Column(db.String(255), unique=False, nullable=True)
    task_file_sha = db.Column(db.String(255), unique=False, nullable=True)
    check_link = db.Column(db.String(255), unique=False, nullable=True)
    check_file_sha = db.Column(db.String(255), unique=False, nullable=True)
    new_passwd = db.Column(db.String(255), unique=False, nullable=True)
    task_status = db.Column(db.String(255), unique=False, nullable=True)
    check_status = db.Column(db.String(255), unique=False, nullable=True)
    isDeleted = db.Column(db.Boolean, unique=False, nullable=True)
    important = db.Column(db.Integer, unique=False, nullable=True)
    original = db.Column(db.JSON, unique=False, nullable=True)
    sign_task_id = db.Column(db.String(255), unique=False, nullable=True)
    sign_task_status = db.Column(db.String(255), unique=False, nullable=True)


class CaoliuUpdate(db.Model, BaseModel):
    """表信息记录"""
    __tablename__ = "caoliu_update"
    id = db.Column(db.Integer, primary_key=True)  # 序号
    user_name = db.Column(db.String(255), unique=True, nullable=False)  # 唯一id
    user_id = db.Column(db.Integer, unique=False, nullable=True)  # 所有数量统计
    password = db.Column(db.String(255), unique=False, nullable=True)  # 表名称
    grade = db.Column(db.String(255), unique=False, nullable=True)  # jsonschema
    email = db.Column(db.String(255), unique=False, nullable=True)  # 是否可用
    weiwang = db.Column(db.String(255), unique=False, nullable=True)  # 描述信息
    contribute = db.Column(db.String(255), unique=False, nullable=True)
    desc = db.Column(db.String(255), unique=False, nullable=True)
    target_weiwang = db.Column(db.String(255), unique=True, nullable=False)  # 创建时间
    creat_time = db.Column(db.DateTime(), default=datetime.datetime.now)  # 更新时间
    money = db.Column(db.Integer, unique=True, nullable=False)  # 拥有者id
    cookie = db.Column(db.String(255), unique=False, nullable=True)
    user_agent = db.Column(db.String(255), unique=False, nullable=True)
    current_money = db.Column(db.Integer, unique=False, nullable=True)
    able_invate = db.Column(db.Boolean, unique=False, nullable=True)
    lease = db.Column(db.Boolean, unique=False, nullable=True)
    task_status = db.Column(db.String(255), unique=False, nullable=True)
    task_link = db.Column(db.String(255), unique=False, nullable=True)
    commit = db.Column(db.Integer, unique=False, nullable=True)
    article_num = db.Column(db.Integer, unique=False, nullable=True)
    py_file_sha = db.Column(db.String(255), unique=False, nullable=True)
    yml_file_sha = db.Column(db.String(255), unique=False, nullable=True)


if __name__ == '__main__':
    update = CaoliuUpdate()
    print(update)

import logging
import smtplib
from email.mime.text import MIMEText
from urllib import parse
import requests
# 导入依赖包
from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from jsonschema import validate
# 在上面的基础上导入
import functools
from src import config_obj
from src.models import User
import hashlib
from urllib.parse import urlencode, unquote


def send_weixin(title, msg):
    content = str(msg)
    server_key = config_obj.SERVER_KEY
    url = f"https://sctapi.ftqq.com/{server_key}.send"
    title_encode = parse.quote(title)
    msg_encode = parse.quote(content)
    payload = f"title={title_encode}&desp={msg_encode}"
    headers = {
        'authority': 'sctapi.ftqq.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'origin': 'https://sct.ftqq.com',
        'referer': 'https://sct.ftqq.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"server_send:{response.json()}")


# 发送邮件
def send_email(title: str, content: str, email=""):
    # 邮件发送方邮箱地址
    sender = config_obj.MAIL_USER
    # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ["648133599@qq.com"] if email == "" else [email]
    # 邮件内容设置
    message = MIMEText(content, 'plain', 'utf-8')
    # 邮件主题
    message['Subject'] = title
    # 发送方信息
    message['From'] = sender
    # 接受方信息
    message['To'] = receivers[0]
    # 登录并发送邮件
    try:
        # 在阿里云上就要改为下面这种，本地和服务器都友好：
        smtpObj = smtplib.SMTP_SSL(config_obj.MAIL_HOST, 465)
        # 登录到服务器
        smtpObj.login(config_obj.MAIL_USER, config_obj.MAIL_PASS)
        # 发送
        smtpObj.sendmail(sender, receivers, message.as_string())
        # 退出
        smtpObj.quit()
    except smtplib.SMTPException as e:
        logging.error(f"发送邮件失败:{e}")


# 编写校验函数
def check_metadata(json_data, schema):
    """
    正确返回True 错误返回异常的日志
    """
    try:
        validate(instance=json_data, schema=schema)
        return True
    except Exception as e:
        return e


def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''
    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    # 接收用户id转换与编码
    token = s.dumps({"id": api_user}).decode("ascii")
    return token


def verify_token(token):
    '''
    校验token
    :param token:
    :return: 用户信息 or None
    '''
    # 参数为私有秘钥，跟上面方法的秘钥保持一致
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        data = s.loads(token)
    except Exception:
        return None
    # 拿到转换后的数据，根据模型类去数据库查询用户信息
    user = User.query.get(data["id"])
    return user


# 构造签名函数
def pay_sign(attributes, key):
    attributes_list = list(attributes)
    for a in attributes_list:
        if attributes[a] == '':
            attributes.pop(a)
    attributes_new = {k: attributes[k] for k in sorted(attributes.keys())}
    return hashlib.md5((unquote(urlencode(attributes_new)) + '&key=' + key)
                       .encode(encoding='utf-8')).hexdigest().upper()


def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            # 这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            return jsonify(code=4103, msg='缺少参数token')
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            s.loads(token)
        except Exception:
            return jsonify(code=4101, msg="登录已过期")
        return view_func(*args, **kwargs)

    return verify_token

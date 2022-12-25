import logging
import time
from urllib.parse import urlencode
from flask import jsonify, request
from src.moduls.pay import pay_blu
from src.utils.common_util import pay_sign


@pay_blu.route("/getPayLink", methods=["POST"])
def get_pay_link():
    paylod = request.json
    logging.info("获取支付连接")
    mchid = '1593541201'  # PAYJS 商户号
    key = 'YiQtLvcisq1Fjzo5'  # 通信密钥
    # 构造订单参数
    money = paylod.get("money")
    pay_type = paylod.get("payType", None)
    time_str = str(int(time.time()))
    # 1024小神支付使用的就是这种方式，然后将url生成二维码，即可支付
    # 默认微信支付，如果是支付宝需要添加："type":"alipay"
    order = {
        'mchid': mchid,
        'body': '我是一个测试订单标题',  # 订单标题
        'total_fee': money,  # 金额,单位:分
        'out_trade_no': 'payjs_jspay_demo_' + time_str,  # 订单号
        "auto": 1,
        "hide": 1,
        "type": pay_type  # 微信支付无需填写
    }
    # 添加数据签名
    order['sign'] = pay_sign(order, key)
    # 浏览器跳转到收银台
    url = 'https://payjs.cn/api/cashier?' + str(urlencode(order))
    # web.open(url,new=0,autoraise=True)
    print(url)
    return jsonify(code=200, message="success", data={"link": url})


@pay_blu.route("/receive", methods=["GET", "POST"])
def query_sql():
    logging.info("接收通知回调：")
    if request.method == 'POST':
        data = request.form
        print(f"data---{data}")
    else:
        print(request.data)
    return 'success!'

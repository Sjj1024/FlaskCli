from flask import Flask
from flask import request
import logging
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route('/',methods=['GET','POST'])
def index():
    return '欢迎来到我的主页'


@app.route('/receive',methods=['GET','POST'])
def receive():
    if request.method == 'POST':
        data = request.form
        print(f"receive---{data}")
        return f'success! {data}'
    return 'fail!'


if __name__ == '__main__':
    app.run(port=8888)
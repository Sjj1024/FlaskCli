import base64
import json

import requests

from src.moduls.table.template import get_caoliu_commit_py, get_caoliu_task_yml
from src.utils.github.config import *


def login():
    headers = {"Authorization": "token %s" % token, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    login = requests.get(f"{base_url}/user", headers=headers)
    print(login.json())


def get_progect(id):
    headers = {"Authorization": "token %s" % token, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    login = requests.get(f"{base_url}/projects/{id}", headers=headers)
    print(login.json())


def add_file(path, content, message):
    url = f"{base_url}/repos/{username}/{repos}/contents/{path}"
    headers = {"Authorization": "token %s" % token, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    base64_content = base64.b64encode("print(''11111)".encode())
    print(base64_content)
    payload = json.dumps({
        "message": message,
        "content": "aW1wb3J0IHJlcXVlc3RzCmZyb20gc3JjLnV0aWxzLmdpdGh1Yi5jb25maWcgaW1wb3J0ICoKCgpkZWYgbG9naW4oKToKICAgIGhlYWRlcnMgPSB7IkF1dGhvcml6YXRpb24iOiAidG9rZW4gJXMiICUgdG9rZW4sICdBY2NlcHQnOiAnYXBwbGljYXRpb24vdm5kLmdpdGh1Yi52Mytqc29uJywKICAgICAgICAgICAgICAgJ0NvbnRlbnQtVHlwZSc6ICdhcHBsaWNhdGlvbi9qc29uJ30KICAgIGxvZ2luID0gcmVxdWVzdHMuZ2V0KGYie2Jhc2VfdXJsfS91c2VyIiwgaGVhZGVycz1oZWFkZXJzKQogICAgcHJpbnQobG9naW4uanNvbigpKQoKCmRlZiBnZXRfcHJvZ2VjdChpZCk6CiAgICBoZWFkZXJzID0geyJBdXRob3JpemF0aW9uIjogInRva2VuICVzIiAlIHRva2VuLCAnQWNjZXB0JzogJ2FwcGxpY2F0aW9uL3ZuZC5naXRodWIudjMranNvbicsCiAgICAgICAgICAgICAgICdDb250ZW50LVR5cGUnOiAnYXBwbGljYXRpb24vanNvbid9CiAgICBsb2dpbiA9IHJlcXVlc3RzLmdldChmIntiYXNlX3VybH0vcHJvamVjdHMve2lkfSIsIGhlYWRlcnM9aGVhZGVycykKICAgIHByaW50KGxvZ2luLmpzb24oKSkKCgppZiBfX25hbWVfXyA9PSAnX19tYWluX18nOgogICAgZ2V0X3Byb2dlY3QoKQ=="
    })
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)


def add_caoliu_task_py(file_name, user_info):
    print("创建一个草榴py文件")
    url = f"{base_url}/repos/{username}/{repos}/contents/src/tasks/{file_name}"
    headers = {"Authorization": "token %s" % token, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    base64_content = get_caoliu_commit_py(user_info)
    print(base64_content)
    payload = json.dumps({
        "message": "add:caoliu.py",
        "content": base64_content
    })
    response = requests.request("PUT", url, headers=headers, data=payload).json()
    if response.get("content", None):
        message = "py:创建成功"
        print(message)
        return True, message
    elif "Bad credentials" in response.get("message"):
        message = "py:Github.Token已失效，请更换token"
        print(message)
        return False, message
    elif "supplied" in response.get("message"):
        message = "py:存在重名的文件，请修改或更改文件名"
        print("存在重名的文件，请修改或更改文件名")
        return False, message


def add_caoliu_task_yml(file_name, py_name):
    print("添加一个caoliu.yml文件")
    url = f"{base_url}/repos/{username}/{repos}/contents/.github/workflows/{file_name}"
    headers = {"Authorization": "token %s" % token, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    base64_content = get_caoliu_task_yml(file_name, py_name)
    print(base64_content)
    payload = json.dumps({
        "message": "add:caoliu.yml",
        "content": base64_content
    })
    response = requests.request("PUT", url, headers=headers, data=payload).json()
    if response.get("content", None):
        message = "yml:创建成功"
        print("创建成功")
        return True, message
    elif "Bad credentials" in response.get("message"):
        message = "yml:Token已失效，请更换token"
        print(message)
        return False, message
    elif "supplied" in response.get("message"):
        message = "yml:存在重名的文件，请修改或更改文件名"
        print(message)
        return False, message


if __name__ == '__main__':
    get_progect("")

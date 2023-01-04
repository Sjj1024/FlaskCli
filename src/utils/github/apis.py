import base64
import json
import requests
from src import config_obj
from src.moduls.table.template import get_caoliu_commit_py, get_caoliu_task_yml, get_caoliu_check_yml


def login():
    headers = {"Authorization": "Bearer %s" % config_obj.GIT_TOKEN, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    login = requests.get(f"{config_obj.GIT_API_URL}/user", headers=headers)
    print(login.json())


def get_progect(id):
    headers = {"Authorization": "Bearer %s" % config_obj.GIT_TOKEN, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    login = requests.get(f"{config_obj.GIT_API_URL}/projects/{id}", headers=headers)
    print(login.json())


def add_file(path, content, message):
    url = f"{config_obj.GIT_API_URL}/repos/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/contents/{path}"
    headers = {"Authorization": "Bearer %s" % config_obj.GIT_TOKEN, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    base64_content = base64.b64encode("print(''11111)".encode())
    print(base64_content)
    payload = json.dumps({
        "message": message,
        "content": "aW1wb3J0IHJlcXVlc3RzCmZyb20gc3JjLnV0aWxzLmdpdGh1Yi5jb25maWcgaW1wb3J0ICoKCgpkZWYgbG9naW4oKToKICAgIGhlYWRlcnMgPSB7IkF1dGhvcml6YXRpb24iOiAidG9rZW4gJXMiICUgdG9rZW4sICdBY2NlcHQnOiAnYXBwbGljYXRpb24vdm5kLmdpdGh1Yi52Mytqc29uJywKICAgICAgICAgICAgICAgJ0NvbnRlbnQtVHlwZSc6ICdhcHBsaWNhdGlvbi9qc29uJ30KICAgIGxvZ2luID0gcmVxdWVzdHMuZ2V0KGYie2Jhc2VfdXJsfS91c2VyIiwgaGVhZGVycz1oZWFkZXJzKQogICAgcHJpbnQobG9naW4uanNvbigpKQoKCmRlZiBnZXRfcHJvZ2VjdChpZCk6CiAgICBoZWFkZXJzID0geyJBdXRob3JpemF0aW9uIjogInRva2VuICVzIiAlIHRva2VuLCAnQWNjZXB0JzogJ2FwcGxpY2F0aW9uL3ZuZC5naXRodWIudjMranNvbicsCiAgICAgICAgICAgICAgICdDb250ZW50LVR5cGUnOiAnYXBwbGljYXRpb24vanNvbid9CiAgICBsb2dpbiA9IHJlcXVlc3RzLmdldChmIntiYXNlX3VybH0vcHJvamVjdHMve2lkfSIsIGhlYWRlcnM9aGVhZGVycykKICAgIHByaW50KGxvZ2luLmpzb24oKSkKCgppZiBfX25hbWVfXyA9PSAnX19tYWluX18nOgogICAgZ2V0X3Byb2dlY3QoKQ=="
    })
    response = requests.request("PUT", url, headers=headers, data=payload)
    print(response.text)


def add_caoliu_task_file(file_name, user_info, file_type="task"):
    print("创建一个caoliuTask文件")
    url = f"{config_obj.GIT_API_URL}/repos/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/contents/{file_name}"
    headers = {"Authorization": "Bearer %s" % config_obj.GIT_TOKEN, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    if file_type == "py":
        base64_content = get_caoliu_commit_py(user_info)
    elif file_type == "task":
        base64_content = get_caoliu_task_yml(f"{user_info.get('username')}", user_info)
    elif file_type == "check":
        base64_content = get_caoliu_check_yml(f"{user_info.get('username')}", user_info)
    else:
        return False, f"file类型错误:{file_name}"
    print(base64_content)
    payload = json.dumps({
        "message": "add:caoliu Task File",
        "content": base64_content
    })
    response = requests.request("PUT", url, headers=headers, data=payload).json()
    if response.get("content", None):
        sha = response.get("content").get("sha")
        return True, sha
    elif "Bad credentials" in response.get("message"):
        message = "py:Github.Token已失效，请更换token"
        print(message)
        return False, message
    elif "supplied" in response.get("message"):
        message = "py:存在重名的文件，请修改或更改文件名"
        print("存在重名的文件，请修改或更改文件名")
        return False, message


def get_repo_action(user_name):
    print("获取仓库workflowId")
    url = f"{config_obj.GIT_API_URL}/repos/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/workflows"
    headers = {"Authorization": "Bearer %s" % config_obj.GIT_TOKEN, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers).json()
    workflows = response.get("workflows")
    for work in workflows:
        if user_name in work.get("name"):
            return work
    return {}


def dispatches_workflow_run(user_name):
    print(f"触发一个工作流运行{user_name}")
    workflow = get_repo_action(user_name)
    if workflow:
        workflow_id = workflow.get("id")
        url = f"{config_obj.GIT_API_URL}/repos/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/workflows/{workflow_id}/dispatches"
        headers = {"Authorization": "Bearer %s" % config_obj.GIT_TOKEN, 'Accept': 'application/vnd.github.v3+json',
                   'Content-Type': 'application/json'}
        payload = json.dumps({"ref": "master", "inputs": {"tags": "sunmanage dispatch"}})
        response = requests.request("POST", url, headers=headers, data=payload)
        print(f"dispatches_workflow_run-{response.text}")
        if not response.text:
            return True
    return True


def del_caoliu_task_file(file_name, user_info):
    print("删除一个草榴文件")
    url = f"{config_obj.GIT_API_URL}/repos/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/contents/{file_name}"
    headers = {"Authorization": "Bearer %s" % config_obj.GIT_TOKEN, 'Accept': 'application/vnd.github.v3+json',
               'Content-Type': 'application/json'}
    payload = json.dumps({
        "message": "del caoliu task",
        "sha": user_info.get("py_sha") if 'py' in file_name else user_info.get("yml_sha")
    })
    response = requests.request("DELETE", url, headers=headers, data=payload).json()
    if response.get("commit", None):
        sha = response.get("commit").get("sha")
        return True, sha
    elif "Bad credentials" in response.get("message"):
        message = "py:Github.Token已失效，请更换token"
        print(message)
        return False, message
    elif "Not Found" in response.get("message"):
        message = f"del:未发现这个文件: {file_name}"
        print(message)
        return True, message
    else:
        message = "py:未知异常"
        print(f"删除文件未知异常：{response}")
        return False, message


if __name__ == '__main__':
    dispatches_workflow_run("CreatArticle")

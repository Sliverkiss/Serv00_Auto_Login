import os
import json
import paramiko
import requests

# 从环境变量中读取 ACCOUNTS_JSON
accounts_json = os.getenv('ACCOUNTS')
accounts = json.loads(accounts_json)

# 尝试通过SSH连接的函数，并执行指定命令
def ssh_connect(host, username, password, bark, command):
    client = None
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        stdin, stdout, stderr = client.exec_command(command)

        # 获取命令执行的输出
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')

        if error:
            ssh_status = f"命令执行失败，错误信息: {error}"
            print(ssh_status)
            if bark:
                url = f"https://api.day.app/{bark}/Serv00自动登录/账号 {username} 命令执行失败，错误信息: {error}"
                response = requests.get(url)
        else:
            ssh_status = f"命令执行成功，输出: {output}"
            print(ssh_status)
            if bark:
                url = f"https://api.day.app/{bark}/Serv00自动登录/账号 {username} 命令执行成功。"
                response = requests.get(url)

    except Exception as e:
        ssh_status = f"SSH连接失败，错误信息: {e}"
        print(ssh_status)

        if bark:
            url = f"https://api.day.app/{bark}/Serv00自动登录/账号 {username} SSH连接失败，请检查账号和密码是否正确。"
            response = requests.get(url)
    finally:
        if client is not None:
            client.close()

# 循环执行任务
for account in accounts:
    ssh_connect(account['host'], account['username'], account['password'], account["bark"], ''cd domains/cxz.dns-dynamic.net && screen node index.js')

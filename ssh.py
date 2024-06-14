import os
import json
import paramiko

# 从环境变量中读取 ACCOUNTS_JSON
accounts_json = os.getenv('ACCOUNTS')
accounts = json.loads(accounts_json)

# 尝试通过SSH连接的函数
def ssh_connect(host, username, password):
    transport = None
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        ssh_status = "SSH连接成功"
        print(f"SSH连接成功。")
    except Exception as e:
        ssh_status = f"SSH连接失败，错误信息: {e}"
        print(f"SSH连接失败: {e}")
    finally:
        if transport is not None:
            transport.close()

# 循环执行任务
for account in accounts:
    ssh_connect(account['host'], account['username'], account['password'])

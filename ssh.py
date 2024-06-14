import os
import paramiko

# 从环境变量中读取 Secrets
ssh_host = os.getenv('HOST')
ssh_username = os.getenv('USERNAME')
ssh_password = os.getenv('PASSWORD')

ssh_info = {  
    'host': ssh_host,
    'port': 22,  
    'username': ssh_username,
    'password': ssh_password
}

# 尝试通过SSH连接的函数
def ssh_connect():
    transport = None
    try:
        transport = paramiko.Transport((ssh_info['host'], ssh_info['port']))
        transport.connect(username=ssh_info['username'], password=ssh_info['password'])
        ssh_status = "SSH连接成功"
        print("SSH连接成功。")
    except Exception as e:
        ssh_status = f"SSH连接失败，错误信息: {e}"
        print(f"SSH连接失败: {e}")
    finally:
        if transport is not None:
            transport.close()

if __name__ == '__main__':
    # 这里可以放你的主程序逻辑
    ssh_connect()

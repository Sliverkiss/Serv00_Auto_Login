import paramiko
import time

# 需要访问的面板信息
panels = [
    {"username": "WFA77", "password": "Hnxczww86", "panel": "panel8.serv00.com"},
    {"username": "hnxpzjww", "password": "Hnxczww86", "panel": "panel8.serv00.com"},
    {"username": "hnxczjww", "password": "Hnxczww86", "panel": "panel8.serv00.com"},
    {"username": "hnxczww66", "password": "Hnxczww86", "panel": "panel8.serv00.com"},
    {"username": "hnxczwwq", "password": "Hnxczww86", "panel": "panel8.serv00.com"},
    {"username": "AWAD", "password": "Hnxczww86", "panel": "panel9.serv00.com"},
    {"username": "PAP19", "password": "Hnxczww86", "panel": "panel9.serv00.com"},
    {"username": "WKKAZZ", "password": "Hnxczww86", "panel": "panel9.serv00.com"},
    {"username": "ZKWK123", "password": "Hnxczww86", "panel": "panel9.serv00.com"},
    {"username": "Lonwm", "password": "Hnxczww86", "panel": "panel10.serv00.com"},
    {"username": "awtku", "password": "Hnxczww86", "panel": "panel10.serv00.com"}
]

# 需要执行的脚本
script_path = './gaojilingjuli.sh'

# 需要添加的 cron 作业
install_agent_cron_command = (
    'crontab -l | grep -v "nezha-agent" | '
    'cat - <(echo "*/12 * * * * pgrep -x \'\x27nezha-agent\x27\' > /dev/null || nohup /home/${USER}/.nezha-agent/start.sh >/dev/null 2>&1 &") | crontab -'
)

start_agent_command = 'nohup /home/${USER}/.nezha-agent/start.sh &'

dashboard_command = 'nohup /home/${USER}/.nezha-dashboard/start.sh &'

reboot_cron_command = 'nohup /home/${USER}/.s5/s5 -c /home/${USER}/.s5/config.json >/dev/null 2>&1 &'

# 任务函数，用于执行 pkill 命令
def kill_s5_process(ssh):
    stdin, stdout, stderr = ssh.exec_command('pkill -9 -f s5')
    time.sleep(1)  # 等待命令执行
    output, error = stdout.read().decode(), stderr.read().decode()

    if output or error:
        print(f"kill s5 process 输出来自 {hostname}: {output}\n错误: {error}")


# 逐个访问面板
for panel in panels:
    hostname = panel["panel"]
    username = panel["username"]
    password = panel["password"]

    try:
        # 创建 SSH 客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接到面板
        ssh.connect(hostname, username=username, password=password)
        print(f"成功连接到 {hostname}，用户：{username}")

        # 检查脚本文件是否存在
        stdin, stdout, stderr = ssh.exec_command(f'ls -l {script_path}')
        file_check_output = stdout.read().decode()
        if 'No such file or directory' in file_check_output:
            print(f"文件 {script_path} 不存在。")
        else:
            # 执行脚本
            stdin, stdout, stderr = ssh.exec_command(f'bash {script_path}')
            script_output = stdout.read().decode()
            script_error = stderr.read().decode()

            if script_output:
                print(f"脚本执行输出来自 {hostname}:")
                print(script_output)
            if script_error:
                print(f"脚本执行错误来自 {hostname}:")
                print(script_error)

            # 执行任务函数
            print(f"正在执行 kill s5 任务")
            kill_s5_process(ssh)

        # 执行安装代理的 cron 命令
        print(f"正在执行安装代理的 cron 命令: {install_agent_cron_command}")
        stdin, stdout, stderr = ssh.exec_command(install_agent_cron_command)
        time.sleep(1)  # 等待一秒钟以确保 cron 作业被添加
        cron_output = stdout.read().decode()
        cron_error = stderr.read().decode()

        if cron_output:
            print(f"安装代理的 cron 命令输出来自 {hostname}:")
            print(cron_output)
        if cron_error:
            print(f"安装代理的 cron 命令错误来自 {hostname}:")
            print(cron_error)

        # 启动代理
        print(f"正在启动代理: {start_agent_command}")
        stdin, stdout, stderr = ssh.exec_command(start_agent_command)
        time.sleep(1)  # 等待一秒钟以确保命令执行
        start_agent_output = stdout.read().decode()
        start_agent_error = stderr.read().decode()

        if start_agent_output:
            print(f"启动代理的输出来自 {hostname}:")
            print(start_agent_output)
        if start_agent_error:
            print(f"启动代理的错误来自 {hostname}:")
            print(start_agent_error)

        # 启动 dashboard
        print(f"正在启动 Nezha dashboard: {dashboard_command}")
        stdin, stdout, stderr = ssh.exec_command(dashboard_command)
        time.sleep(1)  # 等待一秒钟以确保命令执行
        dashboard_output = stdout.read().decode()
        dashboard_error = stderr.read().decode()

        if dashboard_output:
            print(f"启动 Nezha dashboard 的输出来自 {hostname}:")
            print(dashboard_output)
        if dashboard_error:
            print(f"启动 Nezha dashboard 的错误来自 {hostname}:")
            print(dashboard_error)

        # 执行重启时的 cron 命令
        print(f"正在执行重启时的 cron 命令: {reboot_cron_command}")
        stdin, stdout, stderr = ssh.exec_command(reboot_cron_command)
        time.sleep(1)  # 等待一秒钟以确保 cron 作业被添加
        cron_output = stdout.read().decode()
        cron_error = stderr.read().decode()

        if cron_output:
            print(f"重启时的 cron 命令输出来自 {hostname}:")
            print(cron_output)
        if cron_error:
            print(f"重启时的 cron 命令错误来自 {hostname}:")
            print(cron_error)

        # 关闭 SSH 连接
        ssh.close()
    except Exception as e:
        print(f"连接到 {hostname} 失败，用户：{username}，错误：{e}")

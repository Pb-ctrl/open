import time
import requests
import socket
import webbrowser
import threading

# 指定的网址
URL_TO_OPEN = "http://10.30.0.10/"
# 用于检查互联网连接的服务器列表
CHECK_URLS = [
    "https://www.baidu.com",
    "https://www.qq.com",
    "https://www.sina.com.cn"
]
# 用于通过 IP 地址检查互联网连接的服务器 IP 列表
CHECK_IPS = [
    "1.1.1.1",   # Cloudflare DNS
    "8.8.8.8",   # Google DNS
    "114.114.114.114"  # 114 DNS
]
# 超时时间（秒）
CHECK_TIMEOUT = 5
# 默认检查间隔时间（秒）
DEFAULT_INTERVAL = 60

def check_internet_connection(urls, timeout):
    """
    通过访问多个外部服务器检查网络连接状态。
    """
    for url in urls:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            continue
    return False

def check_dns_resolution(domain):
    """
    检查 DNS 解析是否正常。
    """
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def check_ip_connection(ips, timeout):
    """
    通过访问外部 IP 地址检查网络连接状态。
    """
    for ip in ips:
        try:
            response = requests.get(f"http://{ip}", timeout=timeout)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            continue
    return False

def get_interval(default, timeout):
    """
    获取用户输入的检查间隔时间，如果在指定时间内无输入，则使用默认值。
    """
    interval = [default]

    def get_input():
        user_input = input("请输入检查网络的时间间隔（秒），默认60秒：")
        if user_input.isdigit():
            interval[0] = int(user_input)

    input_thread = threading.Thread(target=get_input)
    input_thread.daemon = True
    input_thread.start()
    input_thread.join(timeout)

    return interval[0]

def main():
    interval = get_interval(DEFAULT_INTERVAL, 10)
    print(f"使用的检查间隔时间为：{interval}秒")

    while True:
        if not check_internet_connection(CHECK_URLS, CHECK_TIMEOUT) or \
           not check_dns_resolution("baidu.com") or \
           not check_ip_connection(CHECK_IPS, CHECK_TIMEOUT):
            print("网络断开，打开指定网址...")
            webbrowser.open(URL_TO_OPEN)
        else:
            print("网络正常")
        # 按照用户指定的时间间隔检查网络状态
        time.sleep(interval)

if __name__ == "__main__":
    main()

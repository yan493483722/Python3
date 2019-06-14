import socket
def get_ip_list(domain):  # 获取域名解析出的IP列表


    ip = socket.gethostbyname(domain)

    return ip

print(get_ip_list('www.baidu.com'))

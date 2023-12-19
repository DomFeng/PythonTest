import socket

domain = "www.ziduhaoziweizhi.com"
ip = socket.gethostbyname(domain)
print("域名 %s 的IP地址是：%s" % (domain, ip))

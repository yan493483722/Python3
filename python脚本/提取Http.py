import requests

f=open("C:\\Users\\19190\Desktop\ip.txt",'r')


url = f.readline()
url = "http://"+url
print(url)


try:
    res = requests.get(url)

    if res.status_code=="200":
        print(url)
except:
    pass


# print(res.text)

#响应状态码
## res.status_code

#响应头
#res.headers
import urllib.request
from bs4 import BeautifulSoup
url='http://stu.1000phone.net/student.php'
# send_header={
#     'POST /bWAPP/ba_pwd_attacks_2.php HTTP/1.1'
#     'Host: 101.198.190.68'
#     'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0'
#     'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
#     'Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
#     'Referer: http://101.198.190.68/bWAPP/ba_pwd_attacks_2.php'
#     'Content-Type: application/x-www-form-urlencoded'
#     'Content-Length: 49'
#     'Cookie: hibext_instdsigdipv2=1; bdshare_firstime=1537861722441; last_vtime=1537864194; last_vtime__ckMd5=fa5197021e1f37c3; last_vid=user008; last_vid__ckMd5=2e2e3e6e96465234; _ga=GA1.1.990798957.1537864249; _gid=GA1.1.288103749.1537864264; PHPSESSID=k0f51f2qpifdo387l2bivvjed0; security_level=1'
#     'Connection: close'
#     'Upgrade-Insecure-Requests: 1'
headers = {
     # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36"
    # "Content-Type": "text/html;charset=utf-8"
}


req = urllib.request.Request(url,headers =headers)
respone = urllib.request.urlopen(req)
data  = respone.read()
cs = data.content('password')
#print(data)
#print(data.title)
print(cs)

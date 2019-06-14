import requests

# 1) get
res = requests.get("https://www.baidu.com")

# 2) post
# 	res = requests.post("http://httpbin.org/post");

# 3) put
# res = requests.put("http://httpbin.org/put");

# 4) delete
# res = requests.delete("http://httpbin.org/delete");

# 5) head
# res = requests.head("http://httpbin.org/get") ;

# 6) options
# res = requests.options("http://httpbin.org/get")

# payload = {'key1':'value','key2':'value2'}
# res = requests.post("http://www.baidu.com",data=payload)
# res.url
# u'http://httpbin.org/get?key2=value2&key1=value'
print(res.text)

#响应状态码
## res.status_code

#响应头
#res.headers
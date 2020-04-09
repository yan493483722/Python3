import requests
import threading
import queue

q = queue.Queue() # Queue产生一个队列，有3种类型队列 默认用 FIFO队列
threading_num = 50 # 开启50个线程



def run(code):
    # print(code)
    while not q.empty():
        filedata = q.get()
        for i in filedata:
            url = str(i).replace("\n",'')
            # print(url)
            try:
                data = requests.get(url,timeout=0.1)
                num = data.status_code
                # print(num)
                if str(num) in code:
                    print(url)
            except:
                #print('无法访问此网站')
                pass
        #f.close()

if __name__ =="__main__":
    # 打开字典文件，
    urlfile = input('请输入测试的URL文件：')
    with open(urlfile, "r") as f:
        filedata = f.readlines()
        q.put(filedata)
        f.close() #将line传入到队列 q 中
    try:
        list2=input('请输入你想要测试返回的状态码，顿号分开(默认200):')
        if list2=='':
            list2=['200']
        list2=list2.split('、')
    except:
        list2=['200']
    # print(list2)
    print('测试开始！')
    print('以下URL可正常访问:')
    for i in range(threading_num):
        t = threading.Thread(target=run,args=(list2,))
        t.start()
        t.join()
    print('测试结束！')



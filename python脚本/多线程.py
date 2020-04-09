import threading
import time
import requests

def run(n):
    #time.sleep(3)
    #print("task:",n)
    res = requests.get("https://www.baidu.com")


start_time = time.time()
t_objs = []
thread_num = 100
for i in range(0,thread_num):
    t = threading.Thread(target=run, args=("t-{0}".format(i),))
    t.start()
    t_objs.append(t)
for t in t_objs:
    t.join()
print("cost:", time.time()-start_time)




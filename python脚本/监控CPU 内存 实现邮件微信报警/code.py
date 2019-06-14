import psutil, time,smtplib,socket
import datetime
from wechatpy import WeChatClient
from email.mime.text import MIMEText
from email.utils import formataddr
from prettytable import PrettyTable
class Monitor():

    cpu_data = []
    @classmethod  # 类方法（不需要实例化类就可以被类本身调用）
    #获取内存使用率
    def mem(cls, max=90):
        val = psutil.virtual_memory().percent  #获取内存的使用率的百分比
        #print(val)
        if val > max:
            #print(val)
            send_data ='内存使用率为'+str(round(val, 1))+'%,超过了'+str(max)+"%,请关注!"
            #print(send_data)
            cls.send_msg(str(send_data))
            time.sleep(10)

    @classmethod
    #获取cpu使用率
    def cpu(cls, max=90):
        val = psutil.cpu_percent(1)  #获取cpu使用率
        #print(val)
        cls.cpu_data.append(val)
        #print(cls.cpu_data)
        if len(cls.cpu_data) >= 3:
            avg = sum(cls.cpu_data) / len(cls.cpu_data)  #求出CPU的三次的平均值
            if avg > max:
                #print(avg)
                send_data = 'CPU使用率为' + str(round(val, 1)) + '%,超过了' + str(max) + "%,请关注!"
                #print(send_data)
                cls.send_msg(send_data)
                time.sleep(10)
            cls.cpu_data.pop(0)  #移除第0个元素的值

    @classmethod  # 类方法（不需要实例化类就可以被类本身调用）
    #调用报警函数
    def send_msg(cls, content):
        system_data = cls.get_system()
        data = '错误信息:\n'+content+'\n\n系统信息:\n'+system_data
        print(data)
        #cls.mail(data)
        #cls.wechat(content)

    #得到系统信息
    @classmethod
    def get_system(cls):
        date = ""
        # 用户信息
        now_time =time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time()))
        start_time =datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H: %M: %S")

        # CPU信息
        cpu_num = psutil.cpu_count(logical=False)
        cpu = (str(psutil.cpu_percent(1))) + '%'

        # 内存信息
        total =str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2)) + 'G'
        total_used =  str(round(psutil.virtual_memory().used / (1024.0 * 1024.0 * 1024.0), 2)) + 'G'
        total_free =str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2)) + 'G'
        memory = str(psutil.virtual_memory().percent) + '%'

        # 网卡信息
        net = psutil.net_io_counters()
        bytes_sent = '{0:.2f} Mb'.format(net.bytes_recv / 1024 / 1024)
        bytes_rcvd =  '{0:.2f} Mb'.format(net.bytes_sent / 1024 / 1024)

        date += "当前用户: " + str(psutil.users()[0][0]) + '\n'
        date += "IP 地址: " + str(psutil.users()[0][2]) + '\n\n'
        date +="系统当前时间: "+now_time+'\n'
        date +="系统开机时间: "+start_time+'\n'
        date += '\n'
        date +="CPU个数: "+str(cpu_num)+'\n'
        date +="CPU使用率: "+ cpu+'\n\n'
        date+="内存: "+total+'\n'
        date+="内存已使用: "+total_used+'\n'
        date+="剩余内存: "+ total_free+'\n'
        date+="内存使用率: "+memory+'\n\n'
        date+="网卡发送流量: "+bytes_sent+'\n'
        date+="网卡接收流量: "+ bytes_rcvd+'\n\n'
        # 磁盘信息
        io = psutil.disk_partitions()
        for i in io:
            pan = i[0][0][0] + '盘使用情况\n'
            o = psutil.disk_usage(i.device)
            disk=str(int(o.total / (1024.0 * 1024.0 * 1024.0))) + "G"
            disk_use=str(int(o.used / (1024.0 * 1024.0 * 1024.0))) + "G"
            disk_free=str(int(o.free / (1024.0 * 1024.0 * 1024.0))) + "G"
            date+=pan
            date+='总容量: '+disk+'\n'
            date+='已用容量: '+disk_use+'\n'
            date+='可用容量: '+disk_free+'\n\n'
        return date

    @classmethod
    #邮件报警
    def mail(cls, content):
        #print(content)
        nickname = '监控程序'
        # 发送者的信息
        sender = 'qianxiao996@qq.com'
        password = 'qneiazqazyyldgjj'
        # 接收方的邮箱
        receiver = 'qianxiao996@126.com'
        msg = MIMEText(content,_charset='gb2312')
        msg['From'] = formataddr([nickname, sender])
        msg['Subject'] = '自动报警'
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        try:
            server.login(sender, password)
            server.sendmail(sender, [receiver], msg.as_string())
        except Exception as ex:
            print(ex)
        finally:
            server.quit()
    @classmethod

    #微信报警
    def wechat(cls, content):
        client = WeChatClient('xxxx', 'xxxx')
        template_id = 'xxxxx'
        openid = 'xxxx'
        data = {
            'msg': {"value": content, "color": "#173177"},
            'time': {"value": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "color": "#173177"},
        }
        try:
            client.message.send_template(openid, template_id, data)
        except Exception as ex:
            print(ex)

while True:
    Monitor.mem(20)
    Monitor.cpu(3)
    time.sleep(1)

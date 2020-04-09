#!/usr/bin/python
#-*- coding: utf-8 -*
import time,os,smtplib,socket,threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#发送邮件
def sendemail(email,data,name):
    print(data)
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = "qianxiao996@qq.com"  # 用户名
    mail_pass = "qneiazfdsfdsfdsfsd"  # 口令
    emaillist = mail_user.split('@')
    senddata = '错误信息如下：'+"\n\n"+data+"\n"+"此条信息由系统自动发送！如有错误，敬请谅解！"

    me = emaillist[0] + "<" + mail_user +">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEMultipart()
    msg['Subject'] = name # 设置主题
    msg['From'] = me  # 发送者
    msg['To'] = ";".join(email)  # 接收者
    # ---邮件正文---
    part = MIMEText(senddata, _charset='utf-8')  # 将错误文件内容做为邮件正文内容
    msg.attach(part)

    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  # 连接smtp服务器
        s.login(mail_user, mail_pass)  # 登陆服务器
        s.sendmail(me, email, msg.as_string())  # 发送邮件
        s.close()
        return True
    except Exception as e:
        print(str(e).encode('gb2312').decode('utf-8'))
        return False

#检查日志文件
def checklog(accept_email,filepath,name):
    file = open(filepath, 'r', encoding='utf-8')
    file.seek(0, os.SEEK_END)  #文件的相对结束位置
    error_list=""
    ip = get_ip()
    host = '通知：'+'主机 '+ip+' 的 '+name+' 服务出现错误!'
    #print(host)
    while True:
        where = file.tell()  #返回文件的当前位置。
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
            if error_list != "":
                sendemail(accept_email, error_list,host)
                error_list=""
        else:
            error_list+=line+'\n'

        if len(error_list)>10000:
            sendemail(accept_email,error_list,host)
            error_list = ""
#得到IP
def get_ip():

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip  = s.getsockname()[0]
    s.close()
    return  ip


if __name__ == '__main__':

    accept_email = ['qianxiao996@126.com']

    middleware_name='Apache 2.4'
    middleware_path = r"C:\phpStudy\PHPTutorial\nginx\logs\error.log"

    php_name = 'PHP 2.7'
    php_path = 'C:\phpStudy\PHPTutorial\php\php\php_error.log'


    #中间件
    middleware= threading.Thread(target=checklog, args=(accept_email,middleware_path,middleware_name))
    #php
    php= threading.Thread(target=checklog, args=(accept_email,php_path,php_name))
    middleware.start()
    php.start()



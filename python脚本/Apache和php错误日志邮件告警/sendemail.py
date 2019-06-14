import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_mail(to_list, sub, content):  # to_list：收件人；sub：主题；content：邮件内容
  mail_host = "smtp.qq.com"  # 设置服务器
  mail_user = "qianxiao996@qq.com"  # 用户名
  mail_pass = "qneiazqazyyldgjj"  # 口令
  mail_postfix = "@qq.com"  # 发件箱的后缀

  me = "发送者" + "<" + mail_user + "@" + mail_postfix + ">"  # 这里的hello可以任意设置，收到信后，将按照设置显示
  msg = MIMEMultipart()
  msg['Subject'] = sub  # 设置主题
  msg['From'] = me  #发送者
  msg['To'] = ";".join(to_list) #接收者
  # ---邮件正文---
  part = MIMEText(content,_charset='gb2312')  #将错误文件内容做为邮件正文内容
  msg.attach(part)

  # # txt类型附件
  # part = MIMEApplication(open(send_file, 'rb').read())
  # part.add_header('Content-Disposition', 'attachment', filename="error_log.txt")
  # msg.attach(part)
  try:
    s = smtplib.SMTP()
    s.connect(mail_host)  # 连接smtp服务器
    s.login(mail_user, mail_pass)  # 登陆服务器
    s.sendmail(me, to_list, msg.as_string())  # 发送邮件
    s.close()
    return True
  except Exception as e:
    print(str(e))
    return False

if __name__ == '__main__':


    receive_email =['qianxiao996@126.com']
    send_mail(receive_email,'标题','zhengwen')
    #


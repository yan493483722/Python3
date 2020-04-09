#coding=utf-8
# #ssh登录+sftp下载文件。
#此程序适用于绿盟基线检查脚本。
#by qianxiao996
import paramiko
import xlrd  #引入模块
import sys,re
reload(sys)
sys.setdefaultencoding('utf-8')

def sshclient_execmd(hostname, port, username, password, execmd,savepath):
    paramiko.util.log_to_file("paramiko.log")
    try:
        #SSH
        ssh= paramiko.SSHClient()  # 创建SSH对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # 允许连接不在know_hosts文件中的主机
        ssh.connect(hostname=hostname, port=port, username=username, password=password)  # 连接服务器
        print('[*]主机连接成功！')
        print('[*]开始执行命令，请稍等。。。')
        try:
            stdin, stdout, stderr = ssh.exec_command(execmd)  # 执行命令
            stdin.write("Y")  # Generally speaking, the first connection, need a simple interaction.
            data = stdout.read().decode()+'\n'
            filename = '192.168' + (re.findall(r"192.168(.+?).xml", data)[0].decode()) + '.xml'
            print('[*]命令执行成功,保存文件名为'+filename+'\n[*]开始复制文件')
            try:
                #SFTP
                SFTP = paramiko.Transport(hostname, port)
                SFTP.connect(username=username, password=password)
                sftp = paramiko.SFTPClient.from_transport(SFTP)
                sftp.get('/tmp/'+filename, 'D:/'+filename)
                SFTP.close()  # 关闭连接
                print('[*]文件复制成功！保存路径'+savepath+filename+'\n[*]开始清空文件')
                stdin, stdout, stderr = ssh.exec_command('cd /tmp&&rm -rf /tmp/1.zip&&rm -rf /tmp/66c221be-6ab2-ef53-1589-fe16877914f4.pl&&rm -rf /tmp/66c221be-6ab2-ef53-1589-fe16877914f4.sh&&rm -rf /tmp/'+filename+'ls /tmp')  # 执行命令
                if stdout.read().decode()=='':
                    print('[*]文件清除完毕！\n')
                else:
                    print('文件未删除！\n')
                ssh.close()  # 关闭连接
            except:
                print('[*]文件下载失败！')
        except:
            print('[*]命令执行失败！')
    except:
        print('[*]用户名或密码错误，主机连接失败！')

def main():
    print "[-]脚本执行开始。"
    # 打开文件，获取excel文件的workbook（工作簿）对象
    # try:
    savepath="D:/"
    xls_filename= "ssh.xlsx"
    xls_file = xlrd.open_workbook(xls_filename,encoding_override='utf-8')  # 文件路径
    xls_sheet = xls_file.sheets()[0]  # 打开文件簿，第一个文件簿用[0]表示
    for i in range(1,xls_sheet.nrows):
        row_value = xls_sheet.row_values(i)# 遍历第i行所有的值
        hostname=row_value[0]
        port=int(row_value[3])
        username = row_value[1]
        password= row_value[2]
        execmd = r""
        print "[*]尝试连接主机"+hostname+"。"
        sshclient_execmd(hostname, port, username, password, execmd,savepath)
    # except IOError:
    #     print('Error: 没有找到文件或读取文件失败！')
    print "[-]脚本执行完成!"
if __name__ == "__main__":
    main()
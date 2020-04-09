# -*- coding:utf-8 -*-
import pdfkit
path_wk = r'E:\wkhtmltopdf\bin\wkhtmltopdf.exe' 
config = pdfkit.configuration(wkhtmltopdf = path_wk)

url_file = input('[+]请输入URL文件地址:')
try:
    f=open(url_file,'r',encoding='utf-8')
    data = f.readlines()
    f.close
    print('[+]文件读取成功,总共读取%s篇文章'%len(data))
except IOError:
    print ("[E]Error: 没有找到文件或读取文件失败")
n=0
print('[Start]开始执行任务.')

for sing in data:
    singlist=sing.replace('\n','')
    singlist=singlist.split('-----')
    filename=('['+singlist[3]+']'+singlist[0]+'---'+singlist[2]+'.pdf').replace('|','--')
    # print(filename)
    print('[*]正在保存 %s'%singlist[0])
    try:
        pdfkit.from_url(singlist[1],filename,configuration=config)
        print('[+]文件保存成功.')
        n=n+1
    except Exception as e:
        f=open('error.txt','w',encoding='utf-8')
        f.write(sing)
        f.close
        print('[+]文件%s保存失败'%singlist[0])
        # print(e)

print('[End]文件保存完毕，总共保存文件%s个'%n)
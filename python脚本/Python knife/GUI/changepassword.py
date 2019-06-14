# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'changepassword.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_changepassword(object):
    def setupUi(self, changepassword):
        changepassword.setObjectName("changepassword")
        changepassword.resize(386, 173)
        changepassword.setStyleSheet("background-color: rgb(57, 58, 60);\n"
"color: rgb(255, 0, 0);")
        self.label_2 = QtWidgets.QLabel(changepassword)
        self.label_2.setGeometry(QtCore.QRect(11, 18, 181, 16))
        self.label_2.setObjectName("label_2")
        self.listWidget = QtWidgets.QListWidget(changepassword)
        self.listWidget.setGeometry(QtCore.QRect(11, 40, 256, 91))
        self.listWidget.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.listWidget.setObjectName("listWidget")
        self.changepasswordButton = QtWidgets.QPushButton(changepassword)
        self.changepasswordButton.setGeometry(QtCore.QRect(280, 41, 93, 51))
        self.changepasswordButton.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.changepasswordButton.setObjectName("changepasswordButton")
        self.changeuserButton = QtWidgets.QPushButton(changepassword)
        self.changeuserButton.setGeometry(QtCore.QRect(280, 111, 93, 51))
        self.changeuserButton.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.changeuserButton.setObjectName("changeuserButton")
        self.changepasswordEdit = QtWidgets.QLineEdit(changepassword)
        self.changepasswordEdit.setGeometry(QtCore.QRect(116, 141, 150, 20))
        self.changepasswordEdit.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.changepasswordEdit.setObjectName("changepasswordEdit")
        self.label = QtWidgets.QLabel(changepassword)
        self.label.setGeometry(QtCore.QRect(11, 142, 105, 16))
        self.label.setObjectName("label")

        self.retranslateUi(changepassword)
        self.changepasswordButton.clicked.connect(changepassword.close)
        QtCore.QMetaObject.connectSlotsByName(changepassword)

    def retranslateUi(self, changepassword):
        _translate = QtCore.QCoreApplication.translate
        changepassword.setWindowTitle(_translate("changepassword", "修改密码"))
        self.label_2.setText(_translate("changepassword", "请选择需要修改的用户名："))
        self.changepasswordButton.setText(_translate("changepassword", "取消"))
        self.changeuserButton.setText(_translate("changepassword", "确定"))
        self.label.setText(_translate("changepassword", "请输入新密码："))


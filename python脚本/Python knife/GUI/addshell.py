# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addshell.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(300, 121)
        Form.setStyleSheet("background-color: rgb(57, 58, 60);\n"
"color: rgb(255, 0, 0);")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(49, 40, 111, 20))
        self.lineEdit_2.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(48, 12, 241, 20))
        self.lineEdit.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(8, 13, 40, 16))
        self.label.setObjectName("label")
        self.mima = QtWidgets.QLabel(Form)
        self.mima.setGeometry(QtCore.QRect(9, 42, 40, 16))
        self.mima.setObjectName("mima")
        self.leixing = QtWidgets.QLabel(Form)
        self.leixing.setGeometry(QtCore.QRect(167, 42, 40, 16))
        self.leixing.setObjectName("leixing")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(202, 40, 87, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 70, 281, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Form)
        self.pushButton_2.clicked.connect(Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit, self.lineEdit_2)
        Form.setTabOrder(self.lineEdit_2, self.comboBox)
        Form.setTabOrder(self.comboBox, self.pushButton)
        Form.setTabOrder(self.pushButton, self.pushButton_2)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "添加shell"))
        self.lineEdit.setWhatsThis(_translate("Form", "<html><head/><body><p><br/></p></body></html>"))
        self.label.setText(_translate("Form", "地址："))
        self.mima.setText(_translate("Form", "密码："))
        self.leixing.setText(_translate("Form", "类型"))
        self.comboBox.setItemText(0, _translate("Form", "PHP"))
        self.comboBox.setItemText(1, _translate("Form", "JSP"))
        self.comboBox.setItemText(2, _translate("Form", "ASP"))
        self.pushButton.setText(_translate("Form", "添加"))
        self.pushButton_2.setText(_translate("Form", "取消"))


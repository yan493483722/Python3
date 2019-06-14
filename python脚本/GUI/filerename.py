# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filerename.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_renameForm(object):
    def setupUi(self, renameForm):
        renameForm.setObjectName("renameForm")
        renameForm.resize(321, 92)
        renameForm.setStyleSheet("background-color: rgb(57, 58, 60);\n"
"color: rgb(255, 0, 0);")
        self.renameedit = QtWidgets.QLineEdit(renameForm)
        self.renameedit.setGeometry(QtCore.QRect(66, 15, 240, 20))
        self.renameedit.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.renameedit.setObjectName("renameedit")
        self.renamelabel = QtWidgets.QLabel(renameForm)
        self.renamelabel.setGeometry(QtCore.QRect(12, 17, 51, 16))
        self.renamelabel.setObjectName("renamelabel")
        self.layoutWidget = QtWidgets.QWidget(renameForm)
        self.layoutWidget.setGeometry(QtCore.QRect(112, 47, 195, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.renameButton = QtWidgets.QPushButton(self.layoutWidget)
        self.renameButton.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.renameButton.setObjectName("renameButton")
        self.horizontalLayout.addWidget(self.renameButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(renameForm)
        self.pushButton_2.clicked.connect(renameForm.close)
        QtCore.QMetaObject.connectSlotsByName(renameForm)

    def retranslateUi(self, renameForm):
        _translate = QtCore.QCoreApplication.translate
        renameForm.setWindowTitle(_translate("renameForm", "重命名"))
        self.renamelabel.setText(_translate("renameForm", "文件名："))
        self.renameButton.setText(_translate("renameForm", "确定"))
        self.pushButton_2.setText(_translate("renameForm", "取消"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'useradd.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_adduserForm(object):
    def setupUi(self, adduserForm):
        adduserForm.setObjectName("adduserForm")
        adduserForm.resize(310, 92)
        adduserForm.setStyleSheet("background-color: rgb(57, 58, 60);\n"
"color: rgb(255, 0, 0);")
        self.add0userlabel = QtWidgets.QLabel(adduserForm)
        self.add0userlabel.setGeometry(QtCore.QRect(12, 23, 51, 16))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light SemiCondensed")
        self.add0userlabel.setFont(font)
        self.add0userlabel.setObjectName("add0userlabel")
        self.addpasswordlabel = QtWidgets.QLabel(adduserForm)
        self.addpasswordlabel.setGeometry(QtCore.QRect(24, 53, 42, 16))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light SemiCondensed")
        font.setBold(False)
        font.setWeight(50)
        self.addpasswordlabel.setFont(font)
        self.addpasswordlabel.setScaledContents(False)
        self.addpasswordlabel.setObjectName("addpasswordlabel")
        self.layoutWidget = QtWidgets.QWidget(adduserForm)
        self.layoutWidget.setGeometry(QtCore.QRect(204, 13, 95, 65))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.userButton = QtWidgets.QPushButton(self.layoutWidget)
        self.userButton.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.userButton.setObjectName("userButton")
        self.verticalLayout_3.addWidget(self.userButton)
        self.passwordButton = QtWidgets.QPushButton(self.layoutWidget)
        self.passwordButton.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.passwordButton.setObjectName("passwordButton")
        self.verticalLayout_3.addWidget(self.passwordButton)
        self.layoutWidget1 = QtWidgets.QWidget(adduserForm)
        self.layoutWidget1.setGeometry(QtCore.QRect(65, 15, 135, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.userEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.userEdit.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.userEdit.setObjectName("userEdit")
        self.verticalLayout.addWidget(self.userEdit)
        self.passwordEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.passwordEdit.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.passwordEdit.setObjectName("passwordEdit")
        self.verticalLayout.addWidget(self.passwordEdit)

        self.retranslateUi(adduserForm)
        self.passwordButton.clicked.connect(adduserForm.close)
        QtCore.QMetaObject.connectSlotsByName(adduserForm)

    def retranslateUi(self, adduserForm):
        _translate = QtCore.QCoreApplication.translate
        adduserForm.setWindowTitle(_translate("adduserForm", "添加用户"))
        self.add0userlabel.setText(_translate("adduserForm", "用户名："))
        self.addpasswordlabel.setText(_translate("adduserForm", " 密码："))
        self.userButton.setText(_translate("adduserForm", "确定"))
        self.passwordButton.setText(_translate("adduserForm", "取消"))


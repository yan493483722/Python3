# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sqlpeizhi.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_sql_peizhi(object):
    def setupUi(self, sql_peizhi):
        sql_peizhi.setObjectName("sql_peizhi")
        sql_peizhi.resize(321, 160)
        sql_peizhi.setStyleSheet("background-color: rgb(57, 58, 60);\n"
"color: rgb(255, 0, 0);")
        self.layoutWidget = QtWidgets.QWidget(sql_peizhi)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 24, 286, 120))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.sql_database = QtWidgets.QLabel(self.layoutWidget)
        self.sql_database.setObjectName("sql_database")
        self.verticalLayout.addWidget(self.sql_database)
        self.sql_passwd = QtWidgets.QLabel(self.layoutWidget)
        self.sql_passwd.setObjectName("sql_passwd")
        self.verticalLayout.addWidget(self.sql_passwd)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.sql_name_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.sql_name_edit.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.sql_name_edit.setObjectName("sql_name_edit")
        self.verticalLayout_2.addWidget(self.sql_name_edit)
        self.sql_passwd_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.sql_passwd_edit.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.sql_passwd_edit.setObjectName("sql_passwd_edit")
        self.verticalLayout_2.addWidget(self.sql_passwd_edit)
        self.sql_database_edit = QtWidgets.QLineEdit(self.layoutWidget)
        self.sql_database_edit.setStyleSheet("color: rgb(85, 255, 127);\n"
"background-color: rgb(72, 72, 73);\n"
"border: 1px solid rgb(100, 100, 100);")
        self.sql_database_edit.setObjectName("sql_database_edit")
        self.verticalLayout_2.addWidget(self.sql_database_edit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sql_type = QtWidgets.QComboBox(self.layoutWidget)
        self.sql_type.setObjectName("sql_type")
        self.sql_type.addItem("")
        self.sql_type.addItem("")
        self.sql_type.addItem("")
        self.sql_type.addItem("")
        self.horizontalLayout.addWidget(self.sql_type)
        self.quxiao = QtWidgets.QPushButton(self.layoutWidget)
        self.quxiao.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.quxiao.setObjectName("quxiao")
        self.horizontalLayout.addWidget(self.quxiao)
        self.sql_peizhi_ok = QtWidgets.QPushButton(self.layoutWidget)
        self.sql_peizhi_ok.setStyleSheet("background-color: rgb(68, 69, 73);")
        self.sql_peizhi_ok.setObjectName("sql_peizhi_ok")
        self.horizontalLayout.addWidget(self.sql_peizhi_ok)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(sql_peizhi)
        self.quxiao.clicked.connect(sql_peizhi.close)
        QtCore.QMetaObject.connectSlotsByName(sql_peizhi)
        sql_peizhi.setTabOrder(self.sql_name_edit, self.sql_passwd_edit)
        sql_peizhi.setTabOrder(self.sql_passwd_edit, self.sql_database_edit)

    def retranslateUi(self, sql_peizhi):
        _translate = QtCore.QCoreApplication.translate
        sql_peizhi.setWindowTitle(_translate("sql_peizhi", "配置数据库"))
        self.sql_database.setText(_translate("sql_peizhi", "用户名："))
        self.sql_passwd.setText(_translate("sql_peizhi", "密  码："))
        self.label_3.setText(_translate("sql_peizhi", "数据库名："))
        self.sql_type.setItemText(0, _translate("sql_peizhi", "MYSQL"))
        self.sql_type.setItemText(1, _translate("sql_peizhi", "MSQSL"))
        self.sql_type.setItemText(2, _translate("sql_peizhi", "ORACLE"))
        self.sql_type.setItemText(3, _translate("sql_peizhi", "ACCESS"))
        self.quxiao.setText(_translate("sql_peizhi", "取消"))
        self.sql_peizhi_ok.setText(_translate("sql_peizhi", "确定"))


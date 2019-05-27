# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'baidudemo.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import baidu
import re
import requests
import http.cookiejar
from PIL import Image
import time
import hashlib
import random
import urllib

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(230, 180, 291, 61))
        self.password.setObjectName("password")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(250, 330, 201, 81))
        self.login.setObjectName("login")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 430, 301, 81))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 100, 81, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(120, 200, 54, 12))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(110, 460, 54, 12))
        self.label_4.setObjectName("label_4")
        self.name = QtWidgets.QLineEdit(self.centralwidget)
        self.name.setGeometry(QtCore.QRect(230, 100, 291, 61))
        self.name.setObjectName("name")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(110, 300, 54, 12))
        self.label_5.setObjectName("label_5")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(230, 280, 171, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(420, 290, 101, 31))
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)



        #chacao
        self.login.


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.login.setText(_translate("MainWindow", "登录"))
        self.label_2.setText(_translate("MainWindow", "用户名"))
        self.label_3.setText(_translate("MainWindow", "密码"))
        self.label_4.setText(_translate("MainWindow", "结果"))
        self.label_5.setText(_translate("MainWindow", "验证码"))
        self.label_6.setText(_translate("MainWindow", ""))



        sum_success = "0"
        fail_to_sing = ""

        session = requests.Session()
        session.cookies = http.cookiejar.LWPCookieJar("cookie")

        # POST请求头
        headers = {
            'User-Agent': 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 )',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        # 登录时POST请求头
        headers_login = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8,zh;q=0.6",
            "Host": "passport.baidu.com",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "http://www.baidu.com",
            "Referer": "http://www.baidu.com/",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"
        }

        def fetch_cookies_and_bduss(username,password,verifycode):
            username = username
            password = password
            # 登陆POST用信息
            token = ""
            verifycode = ""
            codestring = ""

            # 第一次POST的信息，如果需要验证码则获取验证码并进行第二次POST
            login_data_first_time = {
                "staticpage": "https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
                "token": token,
                "tpl": "mn",
                "username": user,
                "password": password,
                "loginmerge": "true",
                "mem_pass": "on",
                "logintype": "dialogLogin",
                "logLoginType": "pc_loginDialog",
            }
            # 第二次POST的信息
            login_data_second_time = {
                "staticpage": "https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
                "codestring": codestring,
                "verifycode": verifycode,
                "token": token,
                "tpl": "mn",
                "username": user,
                "password": password,
                "loginmerge": "true",
                "mem_pass": "on",
                "logintype": "dialogLogin",
                "logLoginType": "pc_loginDialog",
            }






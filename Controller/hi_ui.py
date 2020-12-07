# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'hi.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(792, 426)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.text = QPlainTextEdit(self.centralwidget)
        self.text.setObjectName(u"text")
        self.text.setGeometry(QRect(200, 200, 481, 181))
        self.text.setReadOnly(True)
        self.btn_go = QPushButton(self.centralwidget)
        self.btn_go.setObjectName(u"btn_go")
        self.btn_go.setGeometry(QRect(70, 200, 61, 61))
        self.btn_left = QPushButton(self.centralwidget)
        self.btn_left.setObjectName(u"btn_left")
        self.btn_left.setGeometry(QRect(10, 260, 61, 61))
        self.btn_back = QPushButton(self.centralwidget)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setGeometry(QRect(70, 320, 61, 61))
        self.btn_right = QPushButton(self.centralwidget)
        self.btn_right.setObjectName(u"btn_right")
        self.btn_right.setGeometry(QRect(130, 260, 61, 61))
        self.btn_mid = QPushButton(self.centralwidget)
        self.btn_mid.setObjectName(u"btn_mid")
        self.btn_mid.setGeometry(QRect(70, 260, 61, 61))
        self.video_1 = QLabel(self.centralwidget)
        self.video_1.setObjectName(u"video_1")
        self.video_1.setGeometry(QRect(10, 10, 251, 181))
        self.video_1.setStyleSheet(u"background-color: rgb(255, 255,255);")
        self.btn_stop = QPushButton(self.centralwidget)
        self.btn_stop.setObjectName(u"btn_stop")
        self.btn_stop.setGeometry(QRect(690, 340, 91, 41))
        self.video_2 = QLabel(self.centralwidget)
        self.video_2.setObjectName(u"video_2")
        self.video_2.setGeometry(QRect(270, 10, 251, 181))
        self.video_2.setStyleSheet(u"background-color: rgb(255, 255,255);")
        self.video_3 = QLabel(self.centralwidget)
        self.video_3.setObjectName(u"video_3")
        self.video_3.setGeometry(QRect(530, 10, 251, 181))
        self.video_3.setStyleSheet(u"background-color: rgb(255, 255,255);")
        self.btn_night = QPushButton(self.centralwidget)
        self.btn_night.setObjectName(u"btn_night")
        self.btn_night.setGeometry(QRect(690, 200, 91, 41))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 792, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btn_right.clicked.connect(MainWindow.clickedRight)
        self.btn_stop.clicked.connect(MainWindow.clickedStop)
        self.btn_left.clicked.connect(MainWindow.clickedLeft)
        self.btn_go.clicked.connect(MainWindow.clickedGo)
        self.btn_back.clicked.connect(MainWindow.clickedBack)
        self.btn_mid.clicked.connect(MainWindow.clickedMid)
        self.btn_night.clicked.connect(MainWindow.clickedNight)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.text.setPlainText("")
        self.btn_go.setText(QCoreApplication.translate("MainWindow", u"Go", None))
        self.btn_left.setText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.btn_back.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.btn_right.setText(QCoreApplication.translate("MainWindow", u"Right", None))
        self.btn_mid.setText(QCoreApplication.translate("MainWindow", u"Mid", None))
        self.video_1.setText("")
        self.btn_stop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.video_2.setText("")
        self.video_3.setText("")
        self.btn_night.setText(QCoreApplication.translate("MainWindow", u"Night Vision", None))
    # retranslateUi


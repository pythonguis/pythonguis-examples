# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(207, 503)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.head = QtWidgets.QLabel(self.widget)
        self.head.setGeometry(QtCore.QRect(0, -40, 201, 261))
        self.head.setText("")
        self.head.setPixmap(QtGui.QPixmap("images/cat-head-glasses.png"))
        self.head.setAlignment(QtCore.Qt.AlignCenter)
        self.head.setObjectName("head")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(90, 232, 81, 131))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.fileBar = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.fileBar.setContentsMargins(0, 0, 0, 0)
        self.fileBar.setSpacing(0)
        self.fileBar.setObjectName("fileBar")
        self.progress_1 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_1.setFont(font)
        self.progress_1.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_1.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_1.setObjectName("progress_1")
        self.fileBar.addWidget(self.progress_1)
        self.progress_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_2.setFont(font)
        self.progress_2.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_2.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_2.setObjectName("progress_2")
        self.fileBar.addWidget(self.progress_2)
        self.progress_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_3.setFont(font)
        self.progress_3.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_3.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_3.setObjectName("progress_3")
        self.fileBar.addWidget(self.progress_3)
        self.progress_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_4.setFont(font)
        self.progress_4.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_4.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_4.setObjectName("progress_4")
        self.fileBar.addWidget(self.progress_4)
        self.progress_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_5.setFont(font)
        self.progress_5.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_5.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_5.setObjectName("progress_5")
        self.fileBar.addWidget(self.progress_5)
        self.progress_6 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_6.setFont(font)
        self.progress_6.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_6.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_6.setObjectName("progress_6")
        self.fileBar.addWidget(self.progress_6)
        self.progress_7 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_7.setFont(font)
        self.progress_7.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_7.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_7.setObjectName("progress_7")
        self.fileBar.addWidget(self.progress_7)
        self.progress_8 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_8.setFont(font)
        self.progress_8.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_8.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_8.setObjectName("progress_8")
        self.fileBar.addWidget(self.progress_8)
        self.progress_9 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_9.setFont(font)
        self.progress_9.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_9.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_9.setObjectName("progress_9")
        self.fileBar.addWidget(self.progress_9)
        self.progress_10 = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.progress_10.setFont(font)
        self.progress_10.setStyleSheet("QLabel {\n"
"   background-color: rgb(233,30,99);\n"
"border: 2px solid rgb(194,24,91);\n"
"color: rgb(136,14,79);\n"
"}")
        self.progress_10.setAlignment(QtCore.Qt.AlignCenter)
        self.progress_10.setObjectName("progress_10")
        self.fileBar.addWidget(self.progress_10)
        self.body = QtWidgets.QLabel(self.widget)
        self.body.setGeometry(QtCore.QRect(20, 120, 191, 381))
        self.body.setText("")
        self.body.setPixmap(QtGui.QPixmap("images/cat-body-space.png"))
        self.body.setObjectName("body")
        self.verticalLayoutWidget.raise_()
        self.body.raise_()
        self.head.raise_()
        self.verticalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "7Pez"))
        self.progress_1.setText(_translate("MainWindow", "7PEZ"))
        self.progress_2.setText(_translate("MainWindow", "7PEZ"))
        self.progress_3.setText(_translate("MainWindow", "7PEZ"))
        self.progress_4.setText(_translate("MainWindow", "7PEZ"))
        self.progress_5.setText(_translate("MainWindow", "7PEZ"))
        self.progress_6.setText(_translate("MainWindow", "7PEZ"))
        self.progress_7.setText(_translate("MainWindow", "7PEZ"))
        self.progress_8.setText(_translate("MainWindow", "7PEZ"))
        self.progress_9.setText(_translate("MainWindow", "7PEZ"))
        self.progress_10.setText(_translate("MainWindow", "7PEZ"))


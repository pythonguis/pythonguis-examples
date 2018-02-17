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
        MainWindow.resize(721, 333)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.srcLanguage = QtWidgets.QComboBox(self.centralwidget)
        self.srcLanguage.setObjectName("srcLanguage")
        self.verticalLayout.addWidget(self.srcLanguage)
        self.srcTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.srcTextEdit.setObjectName("srcTextEdit")
        self.verticalLayout.addWidget(self.srcTextEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.translateButton = QtWidgets.QPushButton(self.centralwidget)
        self.translateButton.setMinimumSize(QtCore.QSize(75, 50))
        self.translateButton.setMaximumSize(QtCore.QSize(75, 50))
        self.translateButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/flag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.translateButton.setIcon(icon)
        self.translateButton.setIconSize(QtCore.QSize(75, 50))
        self.translateButton.setObjectName("translateButton")
        self.verticalLayout_3.addWidget(self.translateButton)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.destTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.destTextEdit.setObjectName("destTextEdit")
        self.verticalLayout_2.addWidget(self.destTextEdit)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 721, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Translataarrr"))
        self.translateButton.setToolTip(_translate("MainWindow", "Translate"))


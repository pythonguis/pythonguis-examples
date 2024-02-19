# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLCDNumber, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(484, 433)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionReset = QAction(MainWindow)
        self.actionReset.setObjectName(u"actionReset")
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralWidget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lcdNumber = QLCDNumber(self.centralWidget)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setDigitCount(10)

        self.verticalLayout.addWidget(self.lcdNumber)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pushButton_n4 = QPushButton(self.centralWidget)
        self.pushButton_n4.setObjectName(u"pushButton_n4")
        self.pushButton_n4.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(27)
        font.setBold(True)
        self.pushButton_n4.setFont(font)
        self.pushButton_n4.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n4, 3, 0, 1, 1)

        self.pushButton_n1 = QPushButton(self.centralWidget)
        self.pushButton_n1.setObjectName(u"pushButton_n1")
        self.pushButton_n1.setMinimumSize(QSize(0, 50))
        self.pushButton_n1.setFont(font)
        self.pushButton_n1.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n1, 4, 0, 1, 1)

        self.pushButton_n8 = QPushButton(self.centralWidget)
        self.pushButton_n8.setObjectName(u"pushButton_n8")
        self.pushButton_n8.setMinimumSize(QSize(0, 50))
        self.pushButton_n8.setFont(font)
        self.pushButton_n8.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n8, 2, 1, 1, 1)

        self.pushButton_mul = QPushButton(self.centralWidget)
        self.pushButton_mul.setObjectName(u"pushButton_mul")
        self.pushButton_mul.setMinimumSize(QSize(0, 50))
        font1 = QFont()
        font1.setPointSize(27)
        font1.setBold(False)
        self.pushButton_mul.setFont(font1)

        self.gridLayout.addWidget(self.pushButton_mul, 2, 3, 1, 1)

        self.pushButton_n7 = QPushButton(self.centralWidget)
        self.pushButton_n7.setObjectName(u"pushButton_n7")
        self.pushButton_n7.setMinimumSize(QSize(0, 50))
        self.pushButton_n7.setFont(font)
        self.pushButton_n7.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n7, 2, 0, 1, 1)

        self.pushButton_n6 = QPushButton(self.centralWidget)
        self.pushButton_n6.setObjectName(u"pushButton_n6")
        self.pushButton_n6.setMinimumSize(QSize(0, 50))
        self.pushButton_n6.setFont(font)
        self.pushButton_n6.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n6, 3, 2, 1, 1)

        self.pushButton_n5 = QPushButton(self.centralWidget)
        self.pushButton_n5.setObjectName(u"pushButton_n5")
        self.pushButton_n5.setMinimumSize(QSize(0, 50))
        self.pushButton_n5.setFont(font)
        self.pushButton_n5.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n5, 3, 1, 1, 1)

        self.pushButton_n0 = QPushButton(self.centralWidget)
        self.pushButton_n0.setObjectName(u"pushButton_n0")
        self.pushButton_n0.setMinimumSize(QSize(0, 50))
        self.pushButton_n0.setFont(font)
        self.pushButton_n0.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n0, 5, 0, 1, 1)

        self.pushButton_n2 = QPushButton(self.centralWidget)
        self.pushButton_n2.setObjectName(u"pushButton_n2")
        self.pushButton_n2.setMinimumSize(QSize(0, 50))
        self.pushButton_n2.setFont(font)
        self.pushButton_n2.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n2, 4, 1, 1, 1)

        self.pushButton_n9 = QPushButton(self.centralWidget)
        self.pushButton_n9.setObjectName(u"pushButton_n9")
        self.pushButton_n9.setMinimumSize(QSize(0, 50))
        self.pushButton_n9.setFont(font)
        self.pushButton_n9.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n9, 2, 2, 1, 1)

        self.pushButton_n3 = QPushButton(self.centralWidget)
        self.pushButton_n3.setObjectName(u"pushButton_n3")
        self.pushButton_n3.setMinimumSize(QSize(0, 50))
        self.pushButton_n3.setFont(font)
        self.pushButton_n3.setStyleSheet(u"QPushButton {\n"
"color: #1976D2;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_n3, 4, 2, 1, 1)

        self.pushButton_div = QPushButton(self.centralWidget)
        self.pushButton_div.setObjectName(u"pushButton_div")
        self.pushButton_div.setMinimumSize(QSize(0, 50))
        self.pushButton_div.setFont(font1)

        self.gridLayout.addWidget(self.pushButton_div, 1, 3, 1, 1)

        self.pushButton_sub = QPushButton(self.centralWidget)
        self.pushButton_sub.setObjectName(u"pushButton_sub")
        self.pushButton_sub.setMinimumSize(QSize(0, 50))
        self.pushButton_sub.setFont(font1)

        self.gridLayout.addWidget(self.pushButton_sub, 3, 3, 1, 1)

        self.pushButton_add = QPushButton(self.centralWidget)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMinimumSize(QSize(0, 50))
        self.pushButton_add.setFont(font1)

        self.gridLayout.addWidget(self.pushButton_add, 4, 3, 1, 1)

        self.pushButton_ac = QPushButton(self.centralWidget)
        self.pushButton_ac.setObjectName(u"pushButton_ac")
        self.pushButton_ac.setMinimumSize(QSize(0, 50))
        self.pushButton_ac.setFont(font1)
        self.pushButton_ac.setStyleSheet(u"QPushButton {\n"
"    color: #f44336;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_ac, 1, 0, 1, 1)

        self.pushButton_mr = QPushButton(self.centralWidget)
        self.pushButton_mr.setObjectName(u"pushButton_mr")
        self.pushButton_mr.setMinimumSize(QSize(0, 50))
        self.pushButton_mr.setFont(font1)
        self.pushButton_mr.setStyleSheet(u"QPushButton {\n"
"   color: #FFC107;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_mr, 1, 2, 1, 1)

        self.pushButton_m = QPushButton(self.centralWidget)
        self.pushButton_m.setObjectName(u"pushButton_m")
        self.pushButton_m.setMinimumSize(QSize(0, 50))
        self.pushButton_m.setFont(font1)
        self.pushButton_m.setStyleSheet(u"QPushButton {\n"
"   color: #FFC107;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_m, 1, 1, 1, 1)

        self.pushButton_pc = QPushButton(self.centralWidget)
        self.pushButton_pc.setObjectName(u"pushButton_pc")
        self.pushButton_pc.setMinimumSize(QSize(0, 50))
        self.pushButton_pc.setFont(font1)

        self.gridLayout.addWidget(self.pushButton_pc, 5, 1, 1, 1)

        self.pushButton_eq = QPushButton(self.centralWidget)
        self.pushButton_eq.setObjectName(u"pushButton_eq")
        self.pushButton_eq.setMinimumSize(QSize(0, 50))
        self.pushButton_eq.setFont(font)
        self.pushButton_eq.setStyleSheet(u"QPushButton {\n"
"color: #4CAF50;\n"
"}")

        self.gridLayout.addWidget(self.pushButton_eq, 5, 2, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 484, 22))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionReset)
        self.menuFile.addAction(self.actionExit)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Calculon", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionReset.setText(QCoreApplication.translate("MainWindow", u"Reset", None))
#if QT_CONFIG(shortcut)
        self.actionReset.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n4.setText(QCoreApplication.translate("MainWindow", u"4", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n4.setShortcut(QCoreApplication.translate("MainWindow", u"4", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n1.setText(QCoreApplication.translate("MainWindow", u"1", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n1.setShortcut(QCoreApplication.translate("MainWindow", u"1", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n8.setText(QCoreApplication.translate("MainWindow", u"8", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n8.setShortcut(QCoreApplication.translate("MainWindow", u"8", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_mul.setText(QCoreApplication.translate("MainWindow", u"x", None))
#if QT_CONFIG(shortcut)
        self.pushButton_mul.setShortcut(QCoreApplication.translate("MainWindow", u"*", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n7.setText(QCoreApplication.translate("MainWindow", u"7", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n7.setShortcut(QCoreApplication.translate("MainWindow", u"7", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n6.setText(QCoreApplication.translate("MainWindow", u"6", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n6.setShortcut(QCoreApplication.translate("MainWindow", u"6", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n5.setText(QCoreApplication.translate("MainWindow", u"5", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n5.setShortcut(QCoreApplication.translate("MainWindow", u"5", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n0.setText(QCoreApplication.translate("MainWindow", u"0", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n0.setShortcut(QCoreApplication.translate("MainWindow", u"0", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n2.setText(QCoreApplication.translate("MainWindow", u"2", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n2.setShortcut(QCoreApplication.translate("MainWindow", u"2", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n9.setText(QCoreApplication.translate("MainWindow", u"9", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n9.setShortcut(QCoreApplication.translate("MainWindow", u"9", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_n3.setText(QCoreApplication.translate("MainWindow", u"3", None))
#if QT_CONFIG(shortcut)
        self.pushButton_n3.setShortcut(QCoreApplication.translate("MainWindow", u"3", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_div.setText(QCoreApplication.translate("MainWindow", u"\u00f7", None))
#if QT_CONFIG(shortcut)
        self.pushButton_div.setShortcut(QCoreApplication.translate("MainWindow", u"/", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_sub.setText(QCoreApplication.translate("MainWindow", u"-", None))
#if QT_CONFIG(shortcut)
        self.pushButton_sub.setShortcut(QCoreApplication.translate("MainWindow", u"-", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_add.setText(QCoreApplication.translate("MainWindow", u"+", None))
#if QT_CONFIG(shortcut)
        self.pushButton_add.setShortcut(QCoreApplication.translate("MainWindow", u"+", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_ac.setText(QCoreApplication.translate("MainWindow", u"AC", None))
#if QT_CONFIG(shortcut)
        self.pushButton_ac.setShortcut(QCoreApplication.translate("MainWindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_mr.setText(QCoreApplication.translate("MainWindow", u"MR", None))
#if QT_CONFIG(shortcut)
        self.pushButton_mr.setShortcut(QCoreApplication.translate("MainWindow", u"R", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_m.setText(QCoreApplication.translate("MainWindow", u"M", None))
#if QT_CONFIG(shortcut)
        self.pushButton_m.setShortcut(QCoreApplication.translate("MainWindow", u"M", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_pc.setText(QCoreApplication.translate("MainWindow", u"%", None))
#if QT_CONFIG(shortcut)
        self.pushButton_pc.setShortcut(QCoreApplication.translate("MainWindow", u"%", None))
#endif // QT_CONFIG(shortcut)
        self.pushButton_eq.setText(QCoreApplication.translate("MainWindow", u"=", None))
#if QT_CONFIG(shortcut)
        self.pushButton_eq.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi


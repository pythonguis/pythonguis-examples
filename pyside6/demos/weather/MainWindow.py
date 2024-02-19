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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(330, 417)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_3.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        icon = QIcon()
        icon.addFile(u"images/arrow-circle-225.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.weatherIcon = QLabel(self.centralwidget)
        self.weatherIcon.setObjectName(u"weatherIcon")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.weatherIcon.sizePolicy().hasHeightForWidth())
        self.weatherIcon.setSizePolicy(sizePolicy)
        self.weatherIcon.setMinimumSize(QSize(16, 16))
        self.weatherIcon.setMaximumSize(QSize(16, 16))

        self.horizontalLayout_4.addWidget(self.weatherIcon)

        self.weatherLabel = QLabel(self.centralwidget)
        self.weatherLabel.setObjectName(u"weatherLabel")

        self.horizontalLayout_4.addWidget(self.weatherLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.forecastIcon4 = QLabel(self.centralwidget)
        self.forecastIcon4.setObjectName(u"forecastIcon4")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.forecastIcon4.sizePolicy().hasHeightForWidth())
        self.forecastIcon4.setSizePolicy(sizePolicy1)
        self.forecastIcon4.setMinimumSize(QSize(16, 16))
        self.forecastIcon4.setMaximumSize(QSize(200, 16))
        self.forecastIcon4.setBaseSize(QSize(0, 0))
        self.forecastIcon4.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastIcon4, 1, 3, 1, 1)

        self.forecastTemp2 = QLabel(self.centralwidget)
        self.forecastTemp2.setObjectName(u"forecastTemp2")

        self.gridLayout_2.addWidget(self.forecastTemp2, 2, 1, 1, 1)

        self.forecastTemp5 = QLabel(self.centralwidget)
        self.forecastTemp5.setObjectName(u"forecastTemp5")

        self.gridLayout_2.addWidget(self.forecastTemp5, 2, 4, 1, 1)

        self.forecastTemp4 = QLabel(self.centralwidget)
        self.forecastTemp4.setObjectName(u"forecastTemp4")

        self.gridLayout_2.addWidget(self.forecastTemp4, 2, 3, 1, 1)

        self.forecastIcon2 = QLabel(self.centralwidget)
        self.forecastIcon2.setObjectName(u"forecastIcon2")
        sizePolicy1.setHeightForWidth(self.forecastIcon2.sizePolicy().hasHeightForWidth())
        self.forecastIcon2.setSizePolicy(sizePolicy1)
        self.forecastIcon2.setMinimumSize(QSize(16, 16))
        self.forecastIcon2.setMaximumSize(QSize(200, 16))
        self.forecastIcon2.setBaseSize(QSize(0, 0))
        self.forecastIcon2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastIcon2, 1, 1, 1, 1)

        self.forecastIcon5 = QLabel(self.centralwidget)
        self.forecastIcon5.setObjectName(u"forecastIcon5")
        sizePolicy1.setHeightForWidth(self.forecastIcon5.sizePolicy().hasHeightForWidth())
        self.forecastIcon5.setSizePolicy(sizePolicy1)
        self.forecastIcon5.setMinimumSize(QSize(16, 16))
        self.forecastIcon5.setMaximumSize(QSize(200, 16))
        self.forecastIcon5.setBaseSize(QSize(0, 0))
        self.forecastIcon5.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastIcon5, 1, 4, 1, 1)

        self.forecastIcon1 = QLabel(self.centralwidget)
        self.forecastIcon1.setObjectName(u"forecastIcon1")
        sizePolicy1.setHeightForWidth(self.forecastIcon1.sizePolicy().hasHeightForWidth())
        self.forecastIcon1.setSizePolicy(sizePolicy1)
        self.forecastIcon1.setMinimumSize(QSize(16, 16))
        self.forecastIcon1.setMaximumSize(QSize(200, 16))
        self.forecastIcon1.setBaseSize(QSize(0, 0))
        self.forecastIcon1.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastIcon1, 1, 0, 1, 1)

        self.forecastIcon3 = QLabel(self.centralwidget)
        self.forecastIcon3.setObjectName(u"forecastIcon3")
        sizePolicy1.setHeightForWidth(self.forecastIcon3.sizePolicy().hasHeightForWidth())
        self.forecastIcon3.setSizePolicy(sizePolicy1)
        self.forecastIcon3.setMinimumSize(QSize(16, 16))
        self.forecastIcon3.setMaximumSize(QSize(200, 16))
        self.forecastIcon3.setBaseSize(QSize(0, 0))
        self.forecastIcon3.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastIcon3, 1, 2, 1, 1)

        self.forecastTemp3 = QLabel(self.centralwidget)
        self.forecastTemp3.setObjectName(u"forecastTemp3")

        self.gridLayout_2.addWidget(self.forecastTemp3, 2, 2, 1, 1)

        self.forecastTemp1 = QLabel(self.centralwidget)
        self.forecastTemp1.setObjectName(u"forecastTemp1")

        self.gridLayout_2.addWidget(self.forecastTemp1, 2, 0, 1, 1)

        self.forecastTime1 = QLabel(self.centralwidget)
        self.forecastTime1.setObjectName(u"forecastTime1")
        self.forecastTime1.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastTime1, 0, 0, 1, 1)

        self.forecastTime2 = QLabel(self.centralwidget)
        self.forecastTime2.setObjectName(u"forecastTime2")
        self.forecastTime2.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastTime2, 0, 1, 1, 1)

        self.forecastTime3 = QLabel(self.centralwidget)
        self.forecastTime3.setObjectName(u"forecastTime3")
        self.forecastTime3.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastTime3, 0, 2, 1, 1)

        self.forecastTime4 = QLabel(self.centralwidget)
        self.forecastTime4.setObjectName(u"forecastTime4")
        self.forecastTime4.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastTime4, 0, 3, 1, 1)

        self.forecastTime5 = QLabel(self.centralwidget)
        self.forecastTime5.setObjectName(u"forecastTime5")
        self.forecastTime5.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.forecastTime5, 0, 4, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setBold(True)
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_6)

        self.temperatureLabel = QLabel(self.centralwidget)
        self.temperatureLabel.setObjectName(u"temperatureLabel")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.temperatureLabel)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_7)

        self.humidityLabel = QLabel(self.centralwidget)
        self.humidityLabel.setObjectName(u"humidityLabel")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.humidityLabel)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_8)

        self.pressureLabel = QLabel(self.centralwidget)
        self.pressureLabel.setObjectName(u"pressureLabel")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.pressureLabel)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_2)

        self.longitudeLabel = QLabel(self.centralwidget)
        self.longitudeLabel.setObjectName(u"longitudeLabel")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.longitudeLabel)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label_3)

        self.latitudeLabel = QLabel(self.centralwidget)
        self.latitudeLabel.setObjectName(u"latitudeLabel")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.latitudeLabel)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_4)

        self.sunriseLabel = QLabel(self.centralwidget)
        self.sunriseLabel.setObjectName(u"sunriseLabel")

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.sunriseLabel)

        self.label_9 = QLabel(self.centralwidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_9)

        self.label_10 = QLabel(self.centralwidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font)
        self.label_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_10)

        self.windLabel = QLabel(self.centralwidget)
        self.windLabel.setObjectName(u"windLabel")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.windLabel)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.label_11)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.label_13)

        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.label_12)


        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)


        self.horizontalLayout.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Raindar", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"Utrecht,the Netherlands", None))
        self.pushButton.setText("")
        self.weatherIcon.setText("")
        self.weatherLabel.setText("")
        self.forecastIcon4.setText("")
        self.forecastTemp2.setText("")
        self.forecastTemp5.setText("")
        self.forecastTemp4.setText("")
        self.forecastIcon2.setText("")
        self.forecastIcon5.setText("")
        self.forecastIcon1.setText("")
        self.forecastIcon3.setText("")
        self.forecastTemp3.setText("")
        self.forecastTemp1.setText("")
        self.forecastTime1.setText(QCoreApplication.translate("MainWindow", u"+3h", None))
        self.forecastTime2.setText(QCoreApplication.translate("MainWindow", u"+6h", None))
        self.forecastTime3.setText(QCoreApplication.translate("MainWindow", u"+9h", None))
        self.forecastTime4.setText(QCoreApplication.translate("MainWindow", u"+12h", None))
        self.forecastTime5.setText(QCoreApplication.translate("MainWindow", u"+15h", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Barometer", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.temperatureLabel.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Humidity", None))
        self.humidityLabel.setText("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Pressure", None))
        self.pressureLabel.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"Location", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Longitude", None))
        self.longitudeLabel.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Latitude", None))
        self.latitudeLabel.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Sunrise", None))
        self.sunriseLabel.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Speed", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Wind", None))
        self.windLabel.setText("")
        self.label_11.setText("")
        self.label_13.setText("")
        self.label_12.setText("")
    # retranslateUi


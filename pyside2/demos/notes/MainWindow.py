# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(264, 279)
        MainWindow.setAutoFillBackground(True)
        self.centralWidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.closeButton = QtWidgets.QPushButton(parent=self.centralWidget)
        self.closeButton.setMinimumSize(QtCore.QSize(25, 20))
        self.closeButton.setMaximumSize(QtCore.QSize(25, 20))
        self.closeButton.setBaseSize(QtCore.QSize(2, 0))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.closeButton.setFont(font)
        self.closeButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.closeButton.setStyleSheet("QPushButton {\n"
"    border: 0px;\n"
"}")
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem = QtWidgets.QSpacerItem(237, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.moreButton = QtWidgets.QPushButton(parent=self.centralWidget)
        self.moreButton.setMinimumSize(QtCore.QSize(25, 25))
        self.moreButton.setMaximumSize(QtCore.QSize(25, 25))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.moreButton.setFont(font)
        self.moreButton.setStyleSheet("QPushButton {\n"
"    border: 0px;\n"
"}")
        self.moreButton.setObjectName("moreButton")
        self.horizontalLayout.addWidget(self.moreButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtWidgets.QTextEdit(parent=self.centralWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.textEdit.setFont(font)
        self.textEdit.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.textEdit.setLineWidth(0)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Failamp"))
        self.closeButton.setText(_translate("MainWindow", "×"))
        self.moreButton.setText(_translate("MainWindow", "＋"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(552, 479)
        MainWindow.setMinimumSize(QtCore.QSize(552, 479))
        MainWindow.setMaximumSize(QtCore.QSize(552, 479))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(552, 434))
        self.centralwidget.setMaximumSize(QtCore.QSize(552, 434))
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 30, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.txtClientPath = QtWidgets.QLineEdit(self.centralwidget)
        self.txtClientPath.setGeometry(QtCore.QRect(110, 30, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtClientPath.setFont(font)
        self.txtClientPath.setObjectName("txtClientPath")
        self.chkClientPath = QtWidgets.QCheckBox(self.centralwidget)
        self.chkClientPath.setGeometry(QtCore.QRect(410, 30, 101, 21))
        self.chkClientPath.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chkClientPath.setFont(font)
        self.chkClientPath.setObjectName("chkClientPath")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 50, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.txtServerPath = QtWidgets.QLineEdit(self.centralwidget)
        self.txtServerPath.setGeometry(QtCore.QRect(110, 50, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.txtServerPath.setFont(font)
        self.txtServerPath.setObjectName("txtServerPath")
        self.chkServerPath = QtWidgets.QCheckBox(self.centralwidget)
        self.chkServerPath.setGeometry(QtCore.QRect(410, 50, 101, 21))
        self.chkServerPath.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.chkServerPath.setFont(font)
        self.chkServerPath.setObjectName("chkServerPath")
        self.txtLog = QtWidgets.QTextBrowser(self.centralwidget)
        self.txtLog.setGeometry(QtCore.QRect(0, 70, 551, 201))
        self.txtLog.setObjectName("txtLog")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 552, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.menu.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "客户端项目根目录："))
        self.chkClientPath.setText(_translate("MainWindow", "生成代码"))
        self.label_2.setText(_translate("MainWindow", "服务端项目根目录："))
        self.chkServerPath.setText(_translate("MainWindow", "生成代码"))
        self.menu.setTitle(_translate("MainWindow", "视图"))
        self.action.setText(_translate("MainWindow", "刷新"))

if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QWidget()
    ui=Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
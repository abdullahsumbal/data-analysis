# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'github.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GithubWindow(object):
    def setupUi(self, GithubWindow):
        GithubWindow.setObjectName("GithubWindow")
        GithubWindow.resize(860, 300)
        self.label = QtWidgets.QLabel(GithubWindow)
        self.label.setGeometry(QtCore.QRect(10, 10, 831, 281))
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")

        self.retranslateUi(GithubWindow)
        QtCore.QMetaObject.connectSlotsByName(GithubWindow)

    def retranslateUi(self, GithubWindow):
        _translate = QtCore.QCoreApplication.translate
        GithubWindow.setWindowTitle(_translate("GithubWindow", "GitHub"))
        self.label.setText(_translate("GithubWindow", "This Application is developed by\n"
"Muhammad Abdullah Sumbal\n"
"during the summer of 2019.\n"
"\n"
"Code for this application can be found github:\n"
"https://github.com/abdullahsumbal/data-analysis"))



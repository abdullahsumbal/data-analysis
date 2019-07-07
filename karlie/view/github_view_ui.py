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
        GithubWindow.resize(438, 204)
        self.gridLayout_2 = QtWidgets.QGridLayout(GithubWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(GithubWindow)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(GithubWindow)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(GithubWindow)
        QtCore.QMetaObject.connectSlotsByName(GithubWindow)

    def retranslateUi(self, GithubWindow):
        _translate = QtCore.QCoreApplication.translate
        GithubWindow.setWindowTitle(_translate("GithubWindow", "GitHub"))
        self.label_2.setText(_translate("GithubWindow", "<html><head/><body><p><a href=\"https://github.com/abdullahsumbal/data-analysis\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/abdullahsumbal/data-analysis</span></a></p></body></html>"))
        self.label.setText(_translate("GithubWindow", "This Application is developed by\n"
"Muhammad Abdullah Sumbal\n"
"during the summer of 2019.\n"
"\n"
"Code for this application can be found github:\n"
""))



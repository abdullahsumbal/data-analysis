# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        AboutWindow.setObjectName("AboutWindow")
        AboutWindow.setWindowModality(QtCore.Qt.WindowModal)
        AboutWindow.resize(439, 199)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(AboutWindow.sizePolicy().hasHeightForWidth())
        AboutWindow.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(AboutWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(AboutWindow)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(AboutWindow)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(AboutWindow)
        self.label_2.setOpenExternalLinks(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(AboutWindow)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 5, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(AboutWindow)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(AboutWindow)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(AboutWindow)
        QtCore.QMetaObject.connectSlotsByName(AboutWindow)

    def retranslateUi(self, AboutWindow):
        _translate = QtCore.QCoreApplication.translate
        AboutWindow.setWindowTitle(_translate("AboutWindow", "About Application"))
        self.label_4.setText(_translate("AboutWindow", "<html><head/><body><p><a href=\"https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.scatter.html\"><span style=\" text-decoration: underline; color:#0000ff;\">scatter</span></a></p></body></html>"))
        self.label_5.setText(_translate("AboutWindow", "<html><head/><body><p><a href=\"https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.axes.Axes.tick_params.html\"><span style=\" text-decoration: underline; color:#0000ff;\">tick_params</span></a></p></body></html>"))
        self.label_2.setText(_translate("AboutWindow", "<html><head/><body><p><a href=\"https://matplotlib.org/3.1.0/gallery/color/named_colors.html\"><span style=\" text-decoration: underline; color:#0000ff;\">colors</span></a></p></body></html>"))
        self.label_7.setText(_translate("AboutWindow", "<html><head/><body><p><a href=\"https://matplotlib.org/api/_as_gen/matplotlib.pyplot.figure.html#matplotlib.pyplot.figure\"><span style=\" text-decoration: underline; color:#0000ff;\">figure</span></a></p></body></html>"))
        self.label_6.setText(_translate("AboutWindow", "<html><head/><body><p><a href=\"https://matplotlib.org/3.1.0/api/text_api.html#matplotlib.text.Text\"><span style=\" text-decoration: underline; color:#0000ff;\">axis_label</span></a></p></body></html>"))
        self.label.setText(_translate("AboutWindow", "The purpose of this application is to plot tenary diagrams. \n"
"The following are config file parameter links"))



# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view/app.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(804, 538)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 4)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.medusa_file_button = QtWidgets.QPushButton(self.centralwidget)
        self.medusa_file_button.setAutoFillBackground(False)
        self.medusa_file_button.setObjectName("medusa_file_button")
        self.gridLayout.addWidget(self.medusa_file_button, 0, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 2)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 20))
        self.menubar.setObjectName("menubar")
        self.menuwhats_here = QtWidgets.QMenu(self.menubar)
        self.menuwhats_here.setObjectName("menuwhats_here")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbout_application = QtWidgets.QAction(MainWindow)
        self.actionAbout_application.setObjectName("actionAbout_application")
        self.actionGitHub = QtWidgets.QAction(MainWindow)
        self.actionGitHub.setObjectName("actionGitHub")
        self.menuwhats_here.addAction(self.actionAbout_application)
        self.menuwhats_here.addSeparator()
        self.menuwhats_here.addAction(self.actionGitHub)
        self.menubar.addAction(self.menuwhats_here.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Karlie\'s Application"))
        self.label.setText(_translate("MainWindow", "File Selected:"))
        self.pushButton_2.setText(_translate("MainWindow", "Open Mass File"))
        self.pushButton_4.setText(_translate("MainWindow", "Open Config File"))
        self.medusa_file_button.setText(_translate("MainWindow", "Open File"))
        self.pushButton_3.setText(_translate("MainWindow", "Open X Y File"))
        self.menuwhats_here.setTitle(_translate("MainWindow", "Help"))
        self.actionAbout_application.setText(_translate("MainWindow", "About application"))
        self.actionGitHub.setText(_translate("MainWindow", "GitHub"))


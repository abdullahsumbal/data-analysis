from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Cycle(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 211)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 70, 360, 71))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle("Dialog")
        self.label.setText(
            """
              <p><br><br><span style=\" font-size:28pt;\">This is a new window.</span></p>
            """)
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Cycle(object):
    def setupUi(self, CycleWindow):
        CycleWindow.setObjectName("CycleWindow")
        # CycleWindow.resize(400, 211)
        CycleWindow.setWindowModality(QtCore.Qt.NonModal)
        CycleWindow.resize(597, 476)

        self.centralwidget = QtWidgets.QWidget(CycleWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.gridLayout.setObjectName("gridLayout")



        self.retranslateUi(CycleWindow)
        QtCore.QMetaObject.connectSlotsByName(CycleWindow)

    def retranslateUi(self, CycleWindow):
        _translate = QtCore.QCoreApplication.translate
        CycleWindow.setWindowTitle("Select Cycles")

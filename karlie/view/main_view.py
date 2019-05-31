from PyQt5.QtWidgets import QMainWindow, QFileDialog, QCheckBox, QLabel, QPushButton, QDialog
from PyQt5.QtCore import pyqtSlot
from view.main_view_ui import Ui_MainWindow
from view.cycle_view_ui import Ui_Cycle
from PyQt5 import QtCore

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self.cycle_view = CycleView()
        self._ui.setupUi(self)

        # connect widgets to controllers
        self._ui.medusa_file_button.clicked.connect(self.open_file_name_dialog)
        self._ui.plot_volt_cur_button.clicked.connect(self._main_controller.plot_volt_cur)

        # listen for model event signals
        self._model.file_name_changed.connect(self.on_file_name_changed)

    @pyqtSlot(str)
    def on_file_name_changed(self, value):
        # things to do after the file is successfully loaded

        # show file name at the bottom of the window (status bar)
        self._ui.label.setText("File Name: " + value)

        # add checkbox for cycles
        # self.hide()

        self.cycle_view.show()

    # Set one file
    def open_file_name_dialog(self):
        self._main_controller.file_name_changed("")
        return
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "CSV File (*.csv);;All Files (*)", options=options)
        if file_name:
            print(file_name)
        self._main_controller.file_name_changed(file_name)


    # select multiple files
    def open_file_names_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    # save file
    def save_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            print(file_name)

    def select_cycles(self):
        grid = self._ui.gridLayout_select_cycle
        print("adding checkbox")

        # self._ui.add_check()
        for i in range(10):
            name = "Cycle "+str(i + 1)
            checkbox = QCheckBox(self._ui.gridLayoutWidget_2)
            checkbox.setObjectName(name)
            self._ui.gridLayout_select_cycle.addWidget(checkbox, i, 0, 3, 0)
            checkbox.setText(QtCore.QCoreApplication.translate("MainWindow", name))


class CycleView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Cycle()
        self.ui.setupUi(self)
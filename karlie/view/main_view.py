from PyQt5.QtWidgets import QMainWindow, QFileDialog, QCheckBox, QLabel, QPushButton, QDialog
from PyQt5.QtCore import pyqtSlot
from view.main_view_ui import Ui_MainWindow
from view.cycle_view_ui import Ui_Cycle
from os import path
from PyQt5 import QtCore

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self.cycle_view = CycleView()
        self._ui.setupUi(self)

        ####################################################################
        #   connect widgets to controllers
        ####################################################################
        # open file buttons
        self._ui.medusa_file_button.clicked.connect(lambda: self.open_file_name_dialog("medusa"))
        self._ui.button_mass_file.clicked.connect(lambda: self.open_file_name_dialog("mass"))
        self._ui.button_x_y_file.clicked.connect(lambda: self.open_file_name_dialog("x_y"))
        self._ui.button_config_file.clicked.connect(lambda: self.open_file_name_dialog("config"))


        self._ui.button_select_cycle.clicked.connect(self.select_cycles)
        self._ui.plot_volt_cur_button.clicked.connect(self._main_controller.plot_volt_cur)

        ####################################################################
        #   listen for model event signals
        ####################################################################
        # file name is updated
        self._model.file_name_changed.connect(self.on_file_name_changed)


    @pyqtSlot(str, str)
    def on_file_name_changed(self, name, file_type):
        # update file name label

        # only show basename
        name = path.basename(name)

        # update label based on file type
        if file_type == "medusa":
            self._ui.label_medusa_file.setText(self._ui.label_medusa_file.text() + name)
            self._ui.label_medusa_file.setStyleSheet('color: green')
        elif file_type == "mass":
            self._ui.label_mass_file.setText(self._ui.label_mass_file.text() + name)
            self._ui.label_mass_file.setStyleSheet('color: green')
        elif file_type == "x_y":
            self._ui.label_x_y_file.setText(self._ui.label_x_y_file.text() + name)
            self._ui.label_x_y_file.setStyleSheet('color: green')
        elif file_type == "config":
            self._ui.label_config_file.setText( self._ui.label_config_file.text() + name)
            self._ui.label_config_file.setStyleSheet('color: green')
        else:
            self._ui.label_status.setText("Something wrong while loading file")
            self._ui.label_status.setStyleSheet('color: red')

        self._ui.label_status.setText("Successfully loaded {} file".format(file_type))
        self._ui.label_status.setStyleSheet('color: green')

    @pyqtSlot(str)
    def on_mass_file_changed(self, value):
        # update label on ui
        self._ui.label_medusa_file.setText("Medusa file name: " + value)

    # Set one file
    def open_file_name_dialog(self, file_type):
        # open window to select file

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        if file_type == "config":
            file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "JSON File (*.json);;All Files (*)", options=options)
        else:
            file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "CSV File (*.csv);;All Files (*)", options=options)
        if file_name:
            self._main_controller.file_name_changed(file_name, file_type)


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
        self.cycle_view.show()
        # grid = self._ui.gridLayout_select_cycle
        # print("adding checkbox")
        #
        # # self._ui.add_check()
        # for i in range(10):
        #     name = "Cycle "+str(i + 1)
        #     checkbox = QCheckBox(self._ui.gridLayoutWidget_2)
        #     checkbox.setObjectName(name)
        #     self._ui.gridLayout_select_cycle.addWidget(checkbox, i, 0, 3, 0)
        #     checkbox.setText(QtCore.QCoreApplication.translate("MainWindow", name))


class CycleView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Cycle()
        self.ui.setupUi(self)


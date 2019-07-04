from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot
from os import path
from view.main_view_ui import Ui_MainWindow


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)

        ####################################################################
        #   connect widgets to controllers
        ####################################################################
        # open file buttons
        self._ui.button_ternary_file.clicked.connect(lambda: self.open_file_name_dialog("ternary"))
        self._ui.button_master_file.clicked.connect(lambda: self.open_file_name_dialog("master"))

        # plot button
        self._ui.button_plot.clicked.connect(self._main_controller.plot)

        # color scaling
        self._ui.checkbox_default_color.stateChanged.connect(lambda checked: self.enable_color_scale(checked))

        # compare option
        self._ui.checkbox_compare.stateChanged.connect(lambda checked: self.enable_compare(checked))

        ####################################################################
        #   listen for model event signals
        ####################################################################
        # file name is updated
        self._model.file_name_changed.connect(self.on_file_name_changed)

        ####################################################################
        #   listen for controller event signals
        ####################################################################
        # status bar  message
        self._main_controller.task_bar_message.connect(self.on_task_bar_message)

    ####################################################################
    #   model listener functions
    ####################################################################
    @pyqtSlot(str)
    def on_file_name_changed(self, file_type):
        file_label_color = "green"
        self.on_task_bar_message(file_label_color, "Successfully loaded {} file".format(file_type))

        # enable buttons in UI
        if file_type == "master" or "ternary":
            self._ui.checkbox_default_color.setEnabled(True)
            self._ui.button_reset_ternary.setEnabled(True)
            self._ui.comboBox_cycle_1.setEnabled(True)
            self._ui.comboBox_type_1.setEnabled(True)
            self._ui.button_plot.setEnabled(True)
            self._ui.checkbox_compare.setEnabled(True)

            # populate combo box cycles
            cycles_list = self.get_cycle_list()
            self._ui.comboBox_cycle_1.clear()
            self._ui.comboBox_cycle_1.addItems(cycles_list)
            self._ui.comboBox_cycle_2.clear()
            self._ui.comboBox_cycle_2.addItems(cycles_list)



    ####################################################################
    #   controller listener functions
    ####################################################################
    @pyqtSlot(str, str)
    def on_task_bar_message(self, color, message):
        self._ui.statusbar.show()
        self._ui.statusbar.showMessage(message)
        self._ui.statusbar.setStyleSheet('color: {}'.format(color))

    ####################################################################
    #   helper functions to send request to controller
    ####################################################################

    # Set one file
    def open_file_name_dialog(self, file_type):
        # open window to select file
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        if file_type == "config":
            file_name, _ = QFileDialog.getOpenFileName(self, "Select {} file".format(file_type), "",
                                                       "JSON File (*.json);;All Files (*)", options=options)
        else:
            file_name, _ = QFileDialog.getOpenFileName(self,"Select {} file".format(file_type), "",
                                                       "CSV File (*.csv);;All Files (*)", options=options)
        if file_name:
            exclude_channels = self._ui.lineEdit_outlier.text()
            self._main_controller.file_name_changed(file_name, file_type, exclude_channels=exclude_channels)

    ####################################################################
    #   View helper methods
    ####################################################################

    def get_cycle_list(self):
        data = self._model.ternary_file_data
        columns = data.columns
        # get all the columns names with charge in it
        charges = []
        for column in columns:
            if "charge_" in column:
                charges.append(column)

        # get cycles
        cycles = []
        for charge in charges:
            cycles.append(charge[len("charge_"):])

        return cycles

    def enable_color_scale(self, checked):
        self._ui.lineEdit_min_color.setEnabled(not checked)
        self._ui.lineEdit_max_color.setEnabled(not checked)

    def enable_compare(self, checked):
        self._ui.comboBox_operation.setEnabled(checked)
        self._ui.comboBox_cycle_2.setEnabled(checked)
        self._ui.comboBox_type_2.setEnabled(checked)




from PyQt5.QtWidgets import QMainWindow, QFileDialog, QCheckBox, QLabel, QPushButton, QDialog
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from view.main_view_ui import Ui_MainWindow
from view.about_view_ui import Ui_AboutWindow
from view.github_view_ui import Ui_GithubWindow
from view.helper import *
from os import path
from PyQt5 import QtCore

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui_about = AboutView()
        self._ui_github = GithubView()
        self._ui.setupUi(self)

        ####################################################################
        #  Validation for line edit widget
        ####################################################################
        # scale limit validation
        self._ui.lineEdit_scale_x_min.setValidator(QDoubleValidator())
        self._ui.lineEdit_scale_x_max.setValidator(QDoubleValidator())
        self._ui.lineEdit_scale_y_min.setValidator(QDoubleValidator())
        self._ui.lineEdit_scale_y_max.setValidator(QDoubleValidator())
        # filter channel validation
        self._ui.lineEdit_channel.setValidator(QIntValidator())

        ####################################################################
        #   trigger function for UI widgets
        ####################################################################
        self._ui.action_about.triggered.connect(lambda: self._ui_about.show())
        self._ui.action_github.triggered.connect(lambda: self._ui_github.show())

        ####################################################################
        #   connect widgets to controllers
        ####################################################################
        # open file buttons
        self._ui.medusa_file_button.clicked.connect(lambda: self.open_file_name_dialog("medusa"))
        self._ui.button_mass_file.clicked.connect(lambda: self.open_file_name_dialog("mass"))
        self._ui.button_x_y_file.clicked.connect(lambda: self.open_file_name_dialog("x_y"))
        self._ui.button_config_file.clicked.connect(lambda: self.open_file_name_dialog("config"))

        # filter
        # select cycle
        self._ui.checkbox_cycle.stateChanged.connect(
            lambda checked: self._ui.lineEdit_cycle.setEnabled(not checked)
        )
        # select channel
        self._ui.checkbox_channel.stateChanged.connect(
            lambda checked: self._ui.lineEdit_channel.setEnabled(not checked)
        )

        # scale default
        self._ui.checkbox_scale_default.stateChanged.connect(lambda checked: self.enable_custom_scale(checked))

        # button listeners
        self._ui.button_norm_curr_volt.clicked.connect(lambda: self.plot("norm"))
        self._ui.button_charge_discharge.clicked.connect(lambda: self.plot("charge"))
        self._ui.button_avg_volt.clicked.connect(lambda: self.plot("avg_voltage"))
        self._ui.button_capacity.clicked.connect(lambda: self.plot("capacity"))
        self._ui.button_export.clicked.connect(self.export_csv)

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
    @pyqtSlot(str, str)
    def on_file_name_changed(self, name, file_type):
        # update file name label

        # only show basename
        name = path.basename(name)

        # update label based on file type
        if file_type == "medusa":
            new_label = get_new_label(self._ui.label_medusa_file.text(), name)
            self._ui.label_medusa_file.setText(new_label)
            self._ui.label_medusa_file.setStyleSheet('color: green')

            # enable filter options
            self._ui.checkbox_cycle.setEnabled(True)
            self._ui.checkbox_channel.setEnabled(True)

            # enable scale options
            self._ui.checkbox_scale_default.setEnabled(True)

            # update buttons
            self._ui.button_norm_curr_volt.setEnabled(True)
            self._ui.button_charge_discharge.setEnabled(True)
            self._ui.button_avg_volt.setEnabled(True)
            self._ui.button_export.setEnabled(True)
            self._ui.button_capacity.setEnabled(True)

            # update line edit place holder for cycles
            all_cycles = self._main_controller.get_all_cycles()
            all_cycles = [str(i) for i in all_cycles]
            all_cycles = ",".join(all_cycles)
            self._ui.lineEdit_cycle.setText(all_cycles)

        elif file_type == "mass":
            new_label = get_new_label(self._ui.label_mass_file.text(), name)
            self._ui.label_mass_file.setText(new_label)
            self._ui.label_mass_file.setStyleSheet('color: green')
        elif file_type == "x_y":
            new_label = get_new_label(self._ui.label_x_y_file.text(), name)
            self._ui.label_x_y_file.setText(new_label)
            self._ui.label_x_y_file.setStyleSheet('color: green')
        elif file_type == "config":
            new_label = get_new_label(self._ui.label_config_file.text(), name)
            self._ui.label_config_file.setText(new_label)
            self._ui.label_config_file.setStyleSheet('color: green')
        else:
            self._ui.label_status.setText("Something wrong while loading file")
            self._ui.label_status.setStyleSheet('color: red')

        self.on_task_bar_message("green", "Successfully loaded {} file".format(file_type))

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
        options |= QFileDialog.DontUseNativeDialog
        if file_type == "config":
            file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "JSON File (*.json);;All Files (*)", options=options)
        else:
            file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "CSV File (*.csv);;All Files (*)", options=options)
        if file_name:
            self._main_controller.file_name_changed(file_name, file_type)

    # send information to controller about which channels and cycles to plot
    def plot(self, plot_name):
        cycles = self.get_selected_cycles()
        channels = self.get_selected_channels()
        y_limits = self.get_y_axis_limit()
        x_limits = self.get_x_axis_limit()
        # request to send to controller
        self._main_controller.plot(cycles, channels, x_limits, y_limits, plot_name)

    def export_csv(self):
        # get user input for cycles and channels
        cycles = self.get_selected_cycles()
        channels = self.get_selected_channels()
        # validate user input before openning save window
        if self._main_controller.validate_cycles_channels(cycles, channels):
            csv_file_name = self.save_file_dialog()
            # export
            self._main_controller.export_csv(cycles, channels, csv_file_name)

    ####################################################################
    #   View helper methods
    ####################################################################

    # enable custom scaling
    def enable_custom_scale(self, checked):
        self._ui.lineEdit_scale_x_min.setEnabled(not checked)
        self._ui.lineEdit_scale_x_max.setEnabled(not checked)
        self._ui.lineEdit_scale_y_min.setEnabled(not checked)
        self._ui.lineEdit_scale_y_max.setEnabled(not checked)

    # get y-axis limits from ui
    def get_y_axis_limit(self):
        if self._ui.checkbox_scale_default.isChecked():
            y_min = ""
            y_max = ""
        else:
            y_min = self._ui.lineEdit_scale_y_min.text()
            y_max = self._ui.lineEdit_scale_y_max.text()
        return y_min, y_max

    # get x-axis limits from ui
    def get_x_axis_limit(self):
        if self._ui.checkbox_scale_default.isChecked():
            x_min = ""
            x_max = ""
        else:
            x_min = self._ui.lineEdit_scale_x_min.text()
            x_max = self._ui.lineEdit_scale_x_max.text()
        return x_min, x_max

    # get cycles form ui
    def get_selected_cycles(self):
        if self._ui.checkbox_cycle.isChecked():
            return "all"
        else:
            return self._ui.lineEdit_cycle.text()

    # get channels form ui
    def get_selected_channels(self):
        if self._ui.checkbox_channel.isChecked():
            return "all"
        else:
            return self._ui.lineEdit_channel.text()

    # enable and disable line edit based on checkbox
    def toggle_line_edit(self, lineEdit, checked):
        lineEdit.setEnabled(not lineEdit)

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
                                                   "CSV File (*.csv) ;; All Files (*)", options=options)
        if file_name:
            return file_name


class AboutView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AboutWindow()
        self.ui.setupUi(self)


class GithubView(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GithubWindow()
        self.ui.setupUi(self)


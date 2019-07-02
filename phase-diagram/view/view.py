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
        self._ui.button_ternary_file.clicked.connect(lambda: self.open_file_name_dialog("one"))
        self._ui.button_master_file.clicked.connect(lambda: self.open_master_file("master"))

        # plot button
        self._ui.button_plot.clicked.connect(self._main_controller.plot)

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
    def on_file_name_changed(self, name):

        # unable button
        self._ui.button_plot.setEnabled(True)
        name = path.basename(name)
        file_label_color = "green"
        self.on_task_bar_message(file_label_color, "Successfully loaded {} file".format(name))

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
            self._main_controller.file_name_changed(file_name, file_type)

    ####################################################################
    #   View helper methods
    ####################################################################


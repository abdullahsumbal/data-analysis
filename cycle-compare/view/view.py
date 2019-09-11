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
        self._ui.pushButton_master.clicked.connect(self.open_file_name_dialog)

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

    def on_file_name_changed(self, name):
        # label color based on file_name
        # if the file name is empty them it means file is reseted
        name = path.basename(name)
        file_label_color = "green"
        self.on_task_bar_message(file_label_color, "Successfully loaded {} file".format(name))

        # update cycle dropdown
        cycle_set = set()
        master_data = self._model.master_data
        cycle_1 = master_data[0][0].Cycle.unique()
        cycle_2 = master_data[1][0].Cycle.unique()
        cycle_3 = master_data[2][0].Cycle.unique()
        cycle_set.update(cycle_1)
        cycle_set.update(cycle_2)
        cycle_set.update(cycle_3)

        cycle_list = list(cycle_set)
        sorted(cycle_list)

        # assuming there are always even cycles
        self._ui.comboBox_cycle.clear()
        for index in range(0, len(cycle_list), 2):
            charge = cycle_list[index]
            discharge = cycle_list[index + 1]
            self._ui.comboBox_cycle.addItem("{},{}".format(charge, discharge))



    @pyqtSlot(str, str)
    def on_task_bar_message(self, color, message):
        self._ui.statusbar.show()
        self._ui.statusbar.showMessage(message)
        self._ui.statusbar.setStyleSheet('color: {}'.format(color))

    # Set one file
    def open_file_name_dialog(self):
        self._main_controller.validate_master("master-template.csv")
        # # open window to select file
        # options = QFileDialog.Options()
        # # options |= QFileDialog.DontUseNativeDialog
        #
        # file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
        #                                                "All Files (*)", options=options)
        #
        # if file_name:
        #     self._main_controller.validate_master(file_name)

from builtins import enumerate

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog
from PyQt5.QtCore import pyqtSlot, QRegExp, Qt, QObject, pyqtSignal, QRunnable, QThreadPool
from PyQt5.QtGui import QRegExpValidator
from os import path
from view.main_view_ui import Ui_MainWindow
from view.about_view_ui import Ui_AboutWindow
from view.github_view_ui import Ui_GithubWindow


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()
        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui_about = AboutView()
        self._ui_github = GithubView()
        self._ui.setupUi(self)
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(3)
        self.missing_channels = []

        # model and guesses
        self.model_guess = {
            "randles": [0.01,0.005,0.1,0.001,200],
            "R0-p(R1,C1)-W1" : [0.01,0.005,0.1,0.001,200]
        }

        # input validation for missing channel lineedit
        self.apply_validation(self._ui.lineEdit_missing, "(([0-9]{1,2}|([0-9]{1,2}-[0-9]{1,2})),)+")
        self.apply_validation(self._ui.lineEdit_freq_min, "[0-9]+\.?[0-9]+")
        self.apply_validation(self._ui.lineEdit_freq_max, "[0-9]+\.?[0-9]+")
        self.apply_validation(self._ui.lineEdit_freq_point_min, "[1-9][0-9]+")
        self.apply_validation(self._ui.lineEdit_freq_point_max, "[1-9][0-9]+")
        self.apply_validation(self._ui.lineEdit_channel, "([1-9]|[1-5][0-9]|6[0-4])")
        self.apply_validation(self._ui.lineEdit_timeout, "[1-9][0-9]+")
        self.apply_validation(self._ui.lineEdit_guess, "([0-9]+\.[0-9]*,|[0-9]+,)*")

        # frequency range checkout listeners
        self._ui.checkBox_freq_range.stateChanged.connect(lambda checked:
                                                          self.enable_item_based_on_freq_range(checked))
        self._ui.checkBox_freq_point_range.stateChanged.connect(
            lambda checked: self.enable_item_based_on_freq_point_range(checked))

        # select channel
        self._ui.checkBox_channel.stateChanged.connect(
            lambda checked: self._ui.lineEdit_channel.setEnabled(not checked)
        )

        # fitting
        #self._ui.checkBox_fitting.stateChanged.connect(lambda checked: self._ui.lineEdit_timeout.setEnabled(checked))
        self._ui.checkBox_fitting.stateChanged.connect(lambda checked: self.enable_fitting(checked))

        # scale default
        self._ui.checkBox_default_scale.stateChanged.connect(lambda checked: self.enable_custom_scale(checked))

        # default guess
        self._ui.checkBox_default_guess.stateChanged.connect(lambda checked: self._ui.lineEdit_guess.setEnabled(not checked))

        ####################################################################
        #   trigger function for UI widgets
        ####################################################################
        self._ui.action_about.triggered.connect(lambda: self._ui_about.show())
        self._ui.action_github.triggered.connect(lambda: self._ui_github.show())

        ####################################################################
        #   connect widgets to controllers
        ####################################################################
        # open file buttons
        self._ui.button_data_folder.clicked.connect(lambda: self.load_file_folder("data"))
        self._ui.button_x_y.clicked.connect(lambda: self.load_file_folder("x_y"))
        self._ui.button_guess_model.clicked.connect(lambda: self.load_file_folder("guess_model"))
        self._ui.button_area_thickness.clicked.connect(lambda: self.load_file_folder("area_thickness"))
        self._ui.button_config.clicked.connect(lambda: self.load_file_folder("config"))
        self._ui.button_plot.clicked.connect(lambda: self.send_plot_info_to_controller(""))
        self._ui.button_export.clicked.connect(self.export)

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
        self._main_controller.enabled_plot_button.connect(lambda : self._ui.button_plot.setEnabled(True))

    ####################################################################
    #   controller listener functions
    ####################################################################
    def on_file_name_changed(self, file_name, file_type):
        # label color based on file_name
        # if the file name is empty them it means file is reseted

        name = path.basename(file_name)
        enable = not(name == "")
        if enable:
            file_label_color = "green"
            self.on_task_bar_message("green", "Successfully loaded {} file".format(file_type))
        else:
            file_label_color = 'black'
            self.on_task_bar_message("green", "Successfully removed {} file".format(file_type))

        if file_type == "data":
            new_label = self.get_new_label(self._ui.label_data_folder.text(), name)
            self._ui.label_data_folder.setText(new_label)
            self._ui.label_data_folder.setStyleSheet('color: ' + file_label_color)

            # enable rest of the UI
            self._ui.button_plot.setEnabled(enable)

            # enable channel checkbox
            self._ui.checkBox_channel.setEnabled(enable)

            # enable scale
            self._ui.checkBox_default_scale.setEnabled(enable)

            # filter and options
            self._ui.checkBox_freq_range.setEnabled(enable)
            self._ui.checkBox_freq_point_range.setEnabled(enable)

            # enable fitting
            self._ui.checkBox_fitting.setEnabled(enable)

            # other files
            self._ui.button_x_y.setEnabled(enable)
            self._ui.button_config.setEnabled(enable)
            self._ui.button_guess_model.setEnabled(enable)
            self._ui.button_area_thickness.setEnabled(enable)

            # enable guess
            self._ui.checkBox_default_guess.setEnabled(enable)

            # enable model
            self._ui.comboBox_model.setEnabled(enable)

            # enable tile
            self._ui.checkBox_title.setEnabled(enable)

            # update frequency Range
            if enable:
                min_freq, max_freq, total_points = self._main_controller.get_frequency_range_from_data()
                self.set_freq_range(min_freq, max_freq, total_points)

        elif file_type == "config":
            new_label = self.get_new_label(self._ui.label_config.text(), name)
            self._ui.label_config.setText(new_label)
            self._ui.label_config.setStyleSheet('color: ' + file_label_color)
        elif file_type == "x_y":
            new_label = self.get_new_label(self._ui.label_x_y.text(), name)
            self._ui.label_x_y.setText(new_label)
            self._ui.label_x_y.setStyleSheet('color: ' + file_label_color)
        elif file_type == "config":
            new_label = self.get_new_label(self._ui.label_config.text(), name)
            self._ui.label_config.setText(new_label)
            self._ui.label_config.setStyleSheet('color: ' + file_label_color)
        elif file_type == "guess_model":
            new_label = self.get_new_label(self._ui.label_guess_model.text(), name)
            self._ui.label_guess_model.setText(new_label)
            self._ui.label_guess_model.setStyleSheet('color: ' + file_label_color)
        elif file_type == "area_thickness":
            new_label = self.get_new_label(self._ui.label_area_thickness.text(), name)
            self._ui.label_area_thickness.setText(new_label)
            self._ui.label_area_thickness.setStyleSheet('color: ' + file_label_color)

        # open export button
        if self._model.x_y_data is not None and self._model.data_data is not None and self._ui.checkBox_fitting.isChecked():
            self._ui.button_export.setEnabled(True)

    ####################################################################
    #   helper functions to send request to controller
    ####################################################################

    def plotting(self):
        worker = Worker(self.send_plot_info_to_controller) # Any other args, kwargs are passed to the run function
        # worker.signals.result.connect(self.print_output)
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)


        self.threadpool.start(worker)


    def send_plot_info_to_controller(self, progress_callback):
        # turn of the plot button
        # self._ui.button_plot.setEnabled(False)
        self.on_task_bar_message("blue", "Processing Request for plot")
        # missing. return a list of missing channels
        valid, missing = self.validate_missing_channel()
        if not valid:
            return

        # get channel
        channels = self.get_selected_channels()

        # get scale
        y_limits = self.get_y_axis_limit()
        x_limits = self.get_x_axis_limit()
        limits = [x_limits, y_limits]

        # allow fitting
        apply_fitting = self._ui.checkBox_fitting.isChecked()

        # get fitting timeout
        timeout = self._ui.lineEdit_timeout.text()
        if timeout == "":
            self.on_task_bar_message("red", "Error: timeout can not be empty")
            return
        timeout = int(timeout)

        # show title
        show_title = self._ui.checkBox_title.isChecked()

        #get guess and model
        model = self._ui.comboBox_model.currentText()
        valid, guess = self.get_initial_guess()
        if not valid:
            return

        # get frequency info. sends checkbox and lineedit and
        # lets the control decide which one to use
        if not self.validate_freq_line_edits():
            return

        freq_range_info = {"default": self._ui.checkBox_freq_range.isChecked(),
                           "range": [float(self._ui.lineEdit_freq_min.text()), float(self._ui.lineEdit_freq_max.text())]}
        freq_range_point_info = {"default": self._ui.checkBox_freq_point_range.isChecked(),
                           "range": [int(self._ui.lineEdit_freq_point_min.text()), int(self._ui.lineEdit_freq_point_max.text())]}

        self._main_controller.plot(missing, freq_range_info, freq_range_point_info, channels, limits, timeout, apply_fitting, model, guess, show_title)

    def export(self):
        file_path = self.save_file_dialog()
        if not file_path:
            return

        # turn of the plot button
        # self._ui.button_plot.setEnabled(False)
        self.on_task_bar_message("blue", "Processing Request for plot")
        # missing. return a list of missing channels
        valid, missing = self.validate_missing_channel()
        if not valid:
            return

        # get channel
        channels = self.get_selected_channels()

        # get scale
        y_limits = self.get_y_axis_limit()
        x_limits = self.get_x_axis_limit()
        limits = [x_limits, y_limits]

        # allow fitting
        apply_fitting = self._ui.checkBox_fitting.isChecked()

        # get fitting timeout
        timeout = self._ui.lineEdit_timeout.text()
        if timeout == "":
            self.on_task_bar_message("red", "Error: timeout can not be empty")
            return
        timeout = int(timeout)

        #get guess and model
        model = self._ui.comboBox_model.currentText()
        valid, guess = self.get_initial_guess()
        if not valid:
            return

        # get frequency info. sends checkbox and lineedit and
        # lets the control decide which one to use
        if not self.validate_freq_line_edits():
            return

        freq_range_info = {"default": self._ui.checkBox_freq_range.isChecked(),
                           "range": [float(self._ui.lineEdit_freq_min.text()), float(self._ui.lineEdit_freq_max.text())]}
        freq_range_point_info = {"default": self._ui.checkBox_freq_point_range.isChecked(),
                           "range": [int(self._ui.lineEdit_freq_point_min.text()), int(self._ui.lineEdit_freq_point_max.text())]}

        self._main_controller.export(file_path, missing, freq_range_info, freq_range_point_info, channels, limits, timeout, apply_fitting, model, guess)

    def load_file_folder(self, file_type):
        if file_type == "data":
            valid, missing_channels = self.validate_missing_channel()
            self.missing_channels = missing_channels
            if valid:
                folder_name = self.open_folder_dialog() #"test" #
                if folder_name:
                    self._main_controller.validate_file_folder(folder_name, file_type, missing=missing_channels)
        else:
            file_name = self.open_file_name_dialog()
            if file_name:
                self._main_controller.validate_file_folder(file_name, file_type, self.missing_channels)

    ####################################################################
    #   View helper methods
    ####################################################################

    # Set one file
    def open_file_name_dialog(self):
        # open window to select file
        options = QFileDialog.Options()

        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "All Files (*)", options=options)
        return file_name

    # save file
    def save_file_dialog(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save to file", "",
                                                   "CSV File (*.csv) ;; All Files (*)", options=options)
        if file_name:
            return file_name
        else:
            return False

    # Set one file
    def open_folder_dialog(self):
        # open window to select file
        folder_name = QFileDialog.getExistingDirectory(self, "Select Data Directory")
        return folder_name

    @pyqtSlot(str, str)
    def on_task_bar_message(self, color, message):
        self._ui.statusbar.show()
        self._ui.statusbar.showMessage(message)
        self._ui.statusbar.setStyleSheet('color: {}'.format(color))

    def keyPressEvent(self, e):
        # V: validate missing channel
        if e.key() == Qt.Key_V:
            valid, missing = self.validate_missing_channel()
            if valid:
                self.on_task_bar_message("Green", "Valid Missing Channel input: {}".format(",".join(map(str, missing))))
                # also expand the missing channel list in lineedit
                self.set_missing_channel(missing)

        # D: open data file
        if e.key() == Qt.Key_D:
            self.load_file_folder("data")

        # D: open data file
        if e.key() == Qt.Key_P:
            self.send_plot_info_to_controller()

    # take away focus from missing channel lineEdit
    def mousePressEvent(self, e):
        self._ui.lineEdit_missing.clearFocus()
        self._ui.lineEdit_freq_min.clearFocus()
        self._ui.lineEdit_freq_max.clearFocus()
        self._ui.lineEdit_freq_point_min.clearFocus()
        self._ui.lineEdit_freq_point_max.clearFocus()


    # expand the missing channel list in lineEdit
    def set_missing_channel(self, missing_channels):
        self._ui.lineEdit_missing.setText(",".join(map(str, missing_channels)))

    def get_missing_channels_set(self, missing_channels):
        missing_range = missing_channels.split(",")
        missing_channels_set = set()
        for channel in missing_range:
            if '-' in channel:
                start, end = channel.split("-")
                missing_channels_set |= set(range(int(start), int(end) + 1))
            else:
                missing_channels_set.add(int(channel))

        return missing_channels_set

    def validate_missing_channel(self):
        missing_channels = self._ui.lineEdit_missing.text()
        if missing_channels == "":
            # self.on_task_bar_message("red", "Please add missisng channels")
            return True, []
        if missing_channels[-1] == "," or missing_channels[-1] == "-":
            self.on_task_bar_message("red", "Incorrect missing channel format. Should not end with , or -")
            return False, []
        missing_channels = self.get_missing_channels_set(missing_channels)

        greater_than_64 = list(filter(lambda x: x > 64, missing_channels))
        if len(greater_than_64) > 0:
            self.on_task_bar_message("red", "channel can not be greater than 64. Invalid channels {}".format(",".join(map(str, greater_than_64))))
            return False, []
        return True, missing_channels

    def get_new_label(self, old_label, file_name):
        original_label_index = old_label.index(":")
        original_label = old_label[:original_label_index]
        return "{}: {}".format(original_label, file_name)

    def set_freq_range(self, min_freq, max_freq, total_points):
        self._ui.lineEdit_freq_point_min.setText("1")
        self._ui.lineEdit_freq_point_max.setText(str(total_points))
        self._ui.lineEdit_freq_min.setText(str(min_freq))
        self._ui.lineEdit_freq_max.setText(str(max_freq))

    def apply_validation(self, line_edit, pattern):
        reg_ex = QRegExp(pattern)
        input_validator = QRegExpValidator(reg_ex, line_edit)
        line_edit.setValidator(input_validator)

    def enable_item_based_on_freq_point_range(self, checked):
        self._ui.lineEdit_freq_point_min.setEnabled(not checked)
        self._ui.lineEdit_freq_point_max.setEnabled(not checked)

        self._ui.checkBox_freq_range.setEnabled(checked)
        # if not checked:
        if not checked:
            self._ui.lineEdit_freq_min.setEnabled(checked)
            self._ui.lineEdit_freq_max.setEnabled(checked)
        else:
            self._ui.lineEdit_freq_min.setEnabled(not self._ui.checkBox_freq_range.isChecked())
            self._ui.lineEdit_freq_max.setEnabled(not self._ui.checkBox_freq_range.isChecked())

    def enable_item_based_on_freq_range(self, checked):
        self._ui.lineEdit_freq_min.setEnabled(not checked)
        self._ui.lineEdit_freq_max.setEnabled(not checked)

    # enable custom scaling
    def enable_custom_scale(self, checked):
        self._ui.lineEdit_scale_x_min.setEnabled(not checked)
        self._ui.lineEdit_scale_x_max.setEnabled(not checked)
        self._ui.lineEdit_scale_y_min.setEnabled(not checked)
        self._ui.lineEdit_scale_y_max.setEnabled(not checked)


    # get y-axis limits from ui
    def get_y_axis_limit(self):
        if self._ui.checkBox_default_scale.isChecked():
            y_min = ""
            y_max = ""
        else:
            y_min = self._ui.lineEdit_scale_y_min.text()
            y_max = self._ui.lineEdit_scale_y_max.text()
        return y_min, y_max

    # get x-axis limits from ui
    def get_x_axis_limit(self):
        if self._ui.checkBox_default_scale.isChecked():
            x_min = ""
            x_max = ""
        else:
            x_min = self._ui.lineEdit_scale_x_min.text()
            x_max = self._ui.lineEdit_scale_x_max.text()
        return x_min, x_max

    def get_initial_guess(self):
        model = self._ui.comboBox_model.currentText()
        guess = self._ui.lineEdit_guess.text()
        default_guess = self.model_guess[model]
        valid = True
        # if default checked is checked then use default guesses or guesses are empty
        if self._ui.checkBox_default_guess.isChecked():
            return valid, default_guess
        if guess == "":
            return valid, default_guess
        if guess[-1] == ",":
            guess = guess[:-1]

        # convert guess string to list of floats
        guess_list = list(map(float, guess.split(",")))

        if model == "randles":
            if len(guess_list) != len(default_guess):
                self.on_task_bar_message("red", "Error: There should be {} guesses".format(len(default_guess)))
                return not valid, None
        return valid, guess_list

    # get channels form ui
    def get_selected_channels(self):
        if self._ui.checkBox_channel.isChecked():
            return "all"
        else:
            return self._ui.lineEdit_channel.text()

    def validate_freq_line_edits(self):
        min_freq, max_freq, total_points = self._main_controller.get_frequency_range_from_data()
        if self._ui.lineEdit_freq_point_min.text() == "":
            self.on_task_bar_message("red", "Error: min frequency point can not be empty. resetting to default")
            self._ui.lineEdit_freq_point_min.setText("1")
            return False
        elif self._ui.lineEdit_freq_point_max.text() == "":
            self.on_task_bar_message("red", "Error: max frequency point can not be empty. resetting to default")
            self._ui.lineEdit_freq_point_max.setText(str(total_points))
            return False
        elif self._ui.lineEdit_freq_min.text() == "":
            self.on_task_bar_message("red", "Error: min frequency can not be empty. resetting to default")
            self._ui.lineEdit_freq_min.setText(str(min_freq))
            return False
        elif self._ui.lineEdit_freq_max.text() == "":
            self.on_task_bar_message("red", "Error: max frequency can not be empty. resetting to default")
            self._ui.lineEdit_freq_max.setText(str(max_freq))
            return False

        return True

    def enable_fitting(self, checked):
        self._ui.lineEdit_timeout.setEnabled(checked)
        if self._model.x_y_data is not None:
            self._ui.button_export.setEnabled(checked)



# dont know how this code works but this makes the application
# more responsive during a long process.
import traceback, sys

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


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

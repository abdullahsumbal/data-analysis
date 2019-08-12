from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    file_name_changed = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self._data_file_name = ''
        self._data_data = None
        self._config_file = ""
        self._config_data = None
        self._guess_model_name = ""
        self._guess_model_data = None
        self._x_y_name = ""
        self._x_y_data = None
        self._area_thickness_name = ""
        self._area_thickness_data = None

    @property
    def file_name(self):
        return self._file_name

    @property
    def data_data(self):
        return self._data_data

    @property
    def config_data(self):
        return self._config_data

    @property
    def guess_model_data(self):
        return self._guess_model_data

    @property
    def x_y_data(self):
        return self._x_y_data

    @property
    def area_thickness_name(self):
        return self._area_thickness_name

    @file_name.setter
    def file_name(self, value):
        file_name = value[0]
        data = value[1]
        file_type = value[2]
        emit_message = value[3]
        if file_type == "data":
            self._data_file_name = file_name
            self._data_data = data
        elif file_type == "guess_model":
            self._guess_model_name = file_name
            self._guess_model = data
        elif file_type == "x_y":
            self._x_y_name = file_name
            self._x_y_data = data
        elif file_type == "area_thickness":
            self._area_thickness_name = file_name
            self._area_thickness_data = data
        elif file_type == "config":
            self._config_name = file_name
            self._config_data = data

        if emit_message:
            # update in model is reflected in view by sending a signal to view
            self.file_name_changed.emit(file_name, file_type)

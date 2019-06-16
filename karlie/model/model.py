from PyQt5.QtCore import QObject, pyqtSignal

class Medusa(QObject):
    file_name_changed = pyqtSignal(str, str)


    def __init__(self):
        super().__init__()
        self._medusa_file_name = ''
        self._mass_file_name = ''
        self._x_y_file_name = ""
        self._config_file_name = ""
        self._file_name = ""
        self._medusa_data = None
        self._x_y_data = None
        self._config_data = None
        self._mass_data = []


    @property
    def file_name(self):
        return self._file_name

    @property
    def medusa_data(self):
        return self._medusa_data

    @property
    def mass_data(self):
        return self._mass_data

    @property
    def x_y_data(self):
        return self._x_y

    @file_name.setter
    def file_name(self, value):
        name = value[0]
        data = value[1]
        file_type = value[2]

        if file_type == "medusa":
            self._medusa_file_name = name
            self._medusa_data = data
        elif file_type == "mass":
            self._mass_file_name = name
            self._mass_data = data
        elif file_type == "x_y":
            self._x_y_file_name = name
            self._x_y_data = data
        elif file_type == "config":
            self._config_file_name = name
            self._config_data = data

        self.file_name_changed.emit(name, file_type)



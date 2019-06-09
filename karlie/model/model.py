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
        self._charge = {}
        self._time_h = {}
        self._avg_voltage = {}
        self._current = {}
        self._mass = []


    @property
    def file_name(self):
        return self._file_name

    @property
    def medusa_data(self):
        return self._medusa_data

    @property
    def charge(self):
        return self._charge

    @property
    def time_h(self):
        return self._time_h

    @property
    def avg_voltage(self):
        return self._avg_voltage

    @property
    def current(self):
        return self._current

    @property
    def mass(self):
        return self._mass

    @mass.setter
    def mass(self, value):
        self._mass = value

    @avg_voltage.setter
    def avg_voltage(self, value):
        self._avg_voltage = value

    @current.setter
    def current(self, value):
        self._current = value

    @time_h.setter
    def time_h(self, value):
        self._time_h = value

    @charge.setter
    def charge(self, value):
        self._charge = value

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
            self._mass = data
        elif file_type == "x_y":
            self._x_y_file_name = name
            self._x_y_data = data
        elif file_type == "config":
            self._config_file_name = name
            self._config_data = data

        self.file_name_changed.emit(name, file_type)



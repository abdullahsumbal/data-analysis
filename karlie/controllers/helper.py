import pandas as pd

def validate_medusa_file(name):
    data = pd.read_csv(name, skiprows=7)
    return data, True

def validate_mass_file(file_name):
    pass
def validate_config_file(file_name):
    pass

def validate_x_y_file(x_y_file):
    pass


def validate_cycles():
    pass

def validate_channels():
    pass

def get_unique_cycles():
    pass

def get_unique_channels():
    pass


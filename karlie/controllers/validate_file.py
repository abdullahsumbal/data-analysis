import pandas as pd
import csv

def validate_medusa_file(name):
    data = pd.read_csv(name, skiprows=7)
    return data, False

def validate_mass_file(file_name):
    pass
def validate_config_file(file_name):
    pass

def validate_x_y_file(x_y_file):
    pass



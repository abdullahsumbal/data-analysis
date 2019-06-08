def get_new_label(old_label, file_name):
    original_label_index = old_label.index(":")
    original_label = old_label[:original_label_index]
    return "{}: {}".format(original_label, file_name)

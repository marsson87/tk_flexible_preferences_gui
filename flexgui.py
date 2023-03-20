from tkinter import *

import preferencesgui


def create_gui(config_json_filename='conf.json'):
    root = Tk()

    root.resizable(False, False)  # This code helps to disable windows from resizing

    # Remove the Title bar of the window
    # root.overrideredirect(True)

    preferencesgui.PreferencesGUI(root, config_filename=config_json_filename, debug=False)

    root.unbind_all('<<NextWindow>>')  # Unbinding the behavior that causes Tab Cycling
    root.mainloop()


create_gui(config_json_filename='conf.json')
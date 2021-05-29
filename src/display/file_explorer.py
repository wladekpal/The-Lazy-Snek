from tkinter import filedialog
import tkinter
import json
import os
import shutil

CUSTOM_LEVELS_FOLDER_PATH = os.path.join(os.path.dirname(__file__), '../../levels/custom/')


def select_destination(level_to_save):
    root = tkinter.Tk()
    root.withdraw()
    path_to_file = filedialog.asksaveasfilename(filetypes=[('JSON file', '*.json')], defaultextension='*.json')

    if path_to_file:
        created_file = open(path_to_file, 'w')
        json.dump(level_to_save, created_file)


def import_level():
    root = tkinter.Tk()
    root.withdraw()
    file = filedialog.askopenfile(mode ='r', filetypes =[('JSON file', '*.json')])

    # Maybe validation
    shutil.copy(file.name, CUSTOM_LEVELS_FOLDER_PATH)
    file.close()


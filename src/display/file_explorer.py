from tkinter import filedialog
import tkinter


def select_destination(level_to_save):
    root = tkinter.Tk()
    root.withdraw()
    path_to_file = filedialog.asksaveasfilename(filetypes=[('JSON file', '*.json')], defaultextension='*.json')

    if path_to_file:
        created_file = open(path_to_file, 'w')
        created_file.write(level_to_save)

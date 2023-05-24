"""
Rename files inside selected folders

This script allows the user to select multiple folders and then renames
all the files inside these folders. Both the PySimpleGUI FolderBrowse()
and popup_get_folder() only allow a single folder to be selected so this
script is an example of how to select multiple folders.

The renaming is specific to my use but is done in rename_files() and can
be changed for different needs. My renaming uses the parent folder name as
a base then adds a number as a suffix which is incremented for each file in
the folder.

This file contains the following functions:

* rename_files - renames the files
* main - the main function of the script
"""

from pathlib import Path
import PySimpleGUI as psG

PROGRAM_VERSION = '5/18/2023'


def rename_files(window, selected):
    """Rename the files."""
    if not selected:
        psG.Popup('You need to select one or more folders', title='Error', keep_on_top=True)
        return
    number_padding = 2  # use 3 if more than 100 png files
    for folder_name in selected:
        sub_foldername = ''
        file_number = 1
        folder_path = Path(folder_name)
        if folder_path.is_dir():
            for sub_path in folder_path.glob("**/*"):
                if sub_path.is_file():
                    file_numberstr = str(file_number).rjust(number_padding, '0')
                    sub_foldername = sub_path.parts[-2]
                    new_filename = sub_foldername + '-' + file_numberstr + sub_path.suffix
                    new_filepath = sub_path.with_name(new_filename)
                    sub_path.rename(new_filepath)
                    # print(new_filepath)
                    file_number += 1
            msg = 'Finished Folder ' + sub_foldername + ' - Renamed ' + str(file_number - 1) + ' files'
            window['Status'].update(msg+'\n', append=True)
            # print(msg)
    msg = 'Finished renaming selected files'
    window['Status'].update(msg+'\n', append=True)


def main():
    """The main function of the script."""
    font = ("Courier New", 12)
    psG.theme("Dark Brown 3")
    psG.set_options(font=font)

    subfolders = []
    selected = []

    frame_subfolders = [[psG.Listbox(subfolders, size=(100, 10), key='Subfolders',
                        select_mode=psG.LISTBOX_SELECT_MODE_EXTENDED, enable_events=True)]]
    frame_selected = [[psG.Listbox(selected, size=(100, 10), key='Selected')]]
    frame_status = [[psG.Multiline(size=(100, 12), key='Status')]]

    layout = [
        [psG.Input(readonly=True, expand_x=True, key='Main',
                   disabled_readonly_background_color=psG.theme_input_background_color()),
         psG.Button("Main Folder", key='-MainFolder-')],
        [psG.Frame("Subfolder", frame_subfolders)],
        [psG.Frame("Selected Subfolder(s)", frame_selected)],
        [psG.Frame("Status", frame_status)],
        [psG.Button('Update Selected', key='-Add-'),
         psG.Button('Rename', key='-Rename-'),
         psG.Button('Exit', key='-Exit-')],
    ]

    window = psG.Window('File Renamer', layout, icon=PROGICON, finalize=True)
    msg = 'Program version ' + PROGRAM_VERSION
    window['Status'].update(msg+'\n', append=True)

    while True:
        event, values = window.read()
        if event in (psG.WINDOW_CLOSED, '-Exit-'):
            break
        if event == '-MainFolder-':
            main_folder = psG.popup_get_folder("", no_window=True)
            if main_folder and Path(main_folder).is_dir():
                window['Main'].update(main_folder)

                subfolders = sorted([str(f) for f in Path(main_folder).iterdir() if f.is_dir()])
                window['Subfolders'].update(values=subfolders)
                selected = []
                window['Selected'].update(values=selected)
        elif event == '-Add-':
            selected = sorted(path for path in list(values['Subfolders']))
            window['Selected'].update(values=selected)
        elif event == '-Rename-':
            selected = sorted(path for path in list(values['Subfolders']))
            window['Selected'].update(values=selected)
            rename_files(window, selected)
    window.close()


if __name__ == "__main__":
    PROGICON = 'multi-folder3-64x64.ico'
    main()

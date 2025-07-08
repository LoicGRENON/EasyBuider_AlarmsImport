import json
import logging
import queue
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from src import __version__
from category_settings import CategorySettings
from import_source import ImportSource
from settings_manager import SettingsManager
from ui import CategoriesSettingsDialog
from ui import StatusBar
from ui import WorkerThread


logger = logging.getLogger(__name__)


supported_import_sources = [
    ImportSource('codesys', 'CODESYS XML symbols'),
    ImportSource('omron-sysmac', 'OMRON Sysmac Studio')
]
# mapping full_name -> ImportSource used to get ImportSource objet from ComboBox selection
full_name_to_source = {src.full_name: src for src in supported_import_sources}


class AppUi(tk.Tk):
    def __init__(self):
        super(AppUi, self).__init__()

        self.alarms = []
        self.import_filepath = None

        # Queues
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()

        # Worker to handle time-consuming tasks in order to keep the UI responsive
        self.worker = WorkerThread(self.task_queue, self.result_queue)
        self.worker.start()

        self.settings = SettingsManager()
        self.categories_settings = self.get_categories_settings()

        self.title(f"EasyBuilder Alarms Import - V{__version__}")
        self.minsize(200, 100)
        self.main_frm = ttk.Frame(self, padding=10)

        label = ttk.Label(
            self.main_frm,
            text="This application allows you to create a XLSX file "
                 "to import alarms in Weintek (KEP) EasyBuilder Pro.\n"
        )
        label.pack(side=tk.TOP)

        # Import source ComboBox
        frame = ttk.Frame(self.main_frm)
        label = ttk.Label(frame, text="Import symbols from: ")
        label.grid(row=0, column=0, sticky="E")
        self.src_type_combobox = ttk.Combobox(frame, values=[src.full_name for src in supported_import_sources])
        self.src_type_combobox.state(["readonly"])
        self.src_type_combobox.grid(row=0, column=1)

        # PLC name entry
        label = ttk.Label(frame, text="PLC name: ")
        label.grid(row=1, column=0, sticky="E")
        self.plc_name_entry_text = tk.StringVar()
        plc_name_entry = tk.Entry(frame, textvariable=self.plc_name_entry_text)
        plc_name_entry.grid(row=1, column=1, pady=5, sticky="W")

        # Categories
        label = ttk.Label(frame, text="Categories: ")
        label.grid(row=2, column=0, sticky="E")
        self.categories_button = tk.Button(frame, text="Define", command=self.open_categories_settings)
        self.categories_button.grid(row=2, column=1, sticky="W")

        frame.pack()

        buttons_frame = ttk.Frame(self.main_frm)

        # Import button
        import_button = tk.Button(buttons_frame, text='Import', command=self.on_click_import_button)
        import_button.grid(row=0, column=0)

        # Save button
        self.save_button = tk.Button(buttons_frame, text='Save', command=self.on_click_save_button)
        self.save_button.grid(row=0, column=1, padx=20)
        self.save_button["state"] = "disabled"

        buttons_frame.pack(pady=10)

        self.status_bar = StatusBar(self.main_frm)

        self.load_from_settings()

        self.main_frm.pack(fill=tk.BOTH, expand=True)

        # Check worker thread results (Called repeatedly)
        self.__check_result_queue()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # TODO: Add a menu to import/export the settings (or a subset of the settings)

    def __check_result_queue(self):
        try:
            while True:
                message, data = self.result_queue.get_nowait()
                if message == 'parse_result':
                    self.alarms = data
                    nb_alarms = len(self.alarms)
                    if nb_alarms:
                        self.save_button["state"] = "normal"
                    self.status_bar.set_text(f'{nb_alarms} alarms found.')
                elif message == 'write_xls_success':
                    self.status_bar.set_text(f'Alarms saved to {data}')

        except queue.Empty:
            pass
        # Schedule another call after 100ms
        self.after(100, self.__check_result_queue)

    def on_closing(self):
        """
        This method is called when closing the application
        """
        self.task_queue.put(("stop", None))
        self.settings.save()
        self.destroy()

    def on_click_import_button(self):
        """
        This method is called when clicking on the Import button
        """
        selected_full_name  = self.src_type_combobox.get()
        if selected_full_name == '':
            self.settings.set('general', 'import_source', '')
            messagebox.showerror(
                "No source type selected",
                "You first need to select the source type of the symbols you are importing."
            )
            return

        selected_source = full_name_to_source[selected_full_name]
        self.settings.set('general', 'import_source', selected_source.name)

        # Define title and filter file types according to the selected import source
        if selected_source.name == 'codesys':
            askopenfile_title = "Please choose a CoDeSys application symbols file to open"
            askopenfile_filetypes = [('XML files', '.xml')]
        elif selected_source.name == 'omron-sysmac':
            askopenfile_title = "Please choose a Symac Studio application symbols file to open"
            askopenfile_filetypes = [('TXT files', '.txt')]
        else:
            askopenfile_title = "Please choose a file to open"
            askopenfile_filetypes = []

        askopenfile_filetypes.extend([('All files', '.*')])
        self.import_filepath = askopenfilename(title=askopenfile_title, filetypes=askopenfile_filetypes)

        if not self.import_filepath:
            messagebox.showerror("No input file selected",
                                 "No file was selected. Aborted.")
            return

        # Delegate the parsing to the worker thread
        command = 'parse'
        cmd_args = (selected_source, self.import_filepath, self.categories_settings)
        task = (command, cmd_args)
        self.task_queue.put(task)

    def on_click_save_button(self):
        plc_name = self.plc_name_entry_text.get()
        if plc_name:
            self.settings.set('general', 'plc_name', plc_name)
        else:
            messagebox.showerror("PLC name is missing",
                                 "Please enter a PLC name value")
            return

        xlsx_out_filename = Path(self.import_filepath).with_suffix('.xlsx')
        asksavefile_title = "Please choose a filename to save the alarms on"
        asksavefile_filetypes = [('XLSX files', '.xlsx')]
        asksavefile_filetypes.extend([('All files', '.*')])
        xlsx_out_filepath = asksaveasfilename(title=asksavefile_title,
                                              initialdir=xlsx_out_filename.parent,
                                              initialfile=xlsx_out_filename.stem,
                                              filetypes=asksavefile_filetypes,
                                              defaultextension='.xlsx')
        if xlsx_out_filepath:
            command = 'write_xls'
            cmd_args = (self.alarms, plc_name, xlsx_out_filepath, self.categories_settings)
            task = (command, cmd_args)
            self.task_queue.put(task)

    def _select_last_import_source_used(self):
        """
        Select the last used import source from the settings on the ComboBox widget
        """
        import_source_setting = self.settings.get('general', 'import_source')
        if import_source_setting != '':
            name_to_source = {src.name: src for src in supported_import_sources}
            import_source = name_to_source.get(import_source_setting)
            if import_source:  # Make sure the value read from the setting is valid
                self.src_type_combobox.set(import_source.full_name)

    def load_from_settings(self):
        self._select_last_import_source_used()
        self.plc_name_entry_text.set(self.settings.get('general', 'plc_name', ''))

    def get_categories_settings(self):
        categories_settings = []
        for category_id in range(256):
            category_settings = self.settings.get('Categories', str(category_id), None)
            if not category_settings:
                category_settings = json.dumps({
                    'name': '',
                    'filter': '',
                    'bg_color': [255, 0, 0],
                    'fg_color': [0, 0, 0]
                })
            settings_json = json.loads(category_settings)
            categories_settings.append(
                CategorySettings(
                    name=settings_json['name'],
                    regex=settings_json['filter'],
                    bg_color=settings_json['bg_color'],
                    fg_color=settings_json['fg_color'],
                )
            )
        return categories_settings

    def open_categories_settings(self):
        popup = CategoriesSettingsDialog(self,
                                         categories_settings=self.categories_settings,
                                         settings_manager=self.settings)
        popup.wait_window()
        self.categories_settings = popup.categories_settings


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main_app = AppUi()
    main_app.mainloop()

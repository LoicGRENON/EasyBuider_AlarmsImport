import copy
import json
import logging
import pickle
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from tkinter.messagebox import askyesno

from src.alarm_category import AlarmCategory
from .scrollable_frame import ScrollableFrame


BACKGROUND = 1
FOREGROUND = 2


logger = logging.getLogger(__name__)


class CategorySettings:
    def __init__(self, name='', **kwargs):
        self.name = name
        self.alarm_category = AlarmCategory(**kwargs)


class CategoriesSettingsDialog(tk.Toplevel):

    def __init__(self, master, settings_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.settings_manager = settings_manager

        self.title(f'Categories settings')
        self.minsize(300, 100)
        self.geometry('680x400')

        # Make dialog modal
        self.grab_set()

        self.categories = self.get_current_settings()
        # Used to check for modifications by serialization
        self._categories_copy = copy.deepcopy(self.categories)

        main_frm = ttk.Frame(self, padding=10)

        frame = ScrollableFrame(main_frm)
        for row, category in enumerate(self.categories):
            self.show_category(frame.scrollable_frame, row, category)
        frame.pack(fill='both', expand=True)

        button = tk.Button(main_frm, text='Apply changes', command=self.on_apply_change_button)
        button.pack()

        main_frm.pack(fill='both', expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def choose_color(self, button, row, color_type):
        color_type_str = 'foreground' if  color_type == FOREGROUND else 'background'
        (rgb_color, html_color) = colorchooser.askcolor(title=f"Choose {color_type_str} color for category #{row:0{3}}")
        if html_color:
            if color_type == BACKGROUND:
                self.categories[row].alarm_category.bg_color = rgb_color
            elif color_type == FOREGROUND:
                self.categories[row].alarm_category.fg_color = rgb_color

            # Update button color
            button.configure(bg=html_color)

    def on_apply_change_button(self):
        for category_id, category in enumerate(self.categories):
            category_settings = {
                'name': category.name,
                'filter': category.alarm_category.regex,
                'bg_color': category.alarm_category.bg_color,
                'fg_color': category.alarm_category.fg_color
            }
            self.settings_manager.set('Categories', str(category_id), json.dumps(category_settings))

        # Used to check for modifications by serialization
        self._categories_copy = copy.deepcopy(self.categories)

    def on_closing(self):
        """
        This method is called when closing the window
        """

        # Ask for confirmation in case of unsaved changes
        answer = False
        no_modifications_done = pickle.dumps(self._categories_copy) == pickle.dumps(self.categories)
        if not no_modifications_done:
            answer = askyesno(title="Unsaved changes", message="Some changes are not saved .Are you want to exit ?")

        if no_modifications_done or answer:
            self.destroy()

    def on_filter_change(self, widget, row):
        text = widget.get()
        self.categories[row].alarm_category.regex = text
        logger.debug(f'Category row {row} filter set to "{text}"')

    def on_name_change(self, widget, row):
        text = widget.get()
        self.categories[row].name = text
        logger.debug(f'Category row {row} name set to "{text}"')

    def get_current_settings(self):
        categories_settings = []
        for category_id in range(256):
            category_settings = self.settings_manager.get('Categories', str(category_id), None)
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

    def show_category(self, parent_frame, row: int, category: CategorySettings):
        category_frm = ttk.Frame(parent_frame)

        label = ttk.Label(category_frm, text=f"#{row:0{3}} - Name: ")
        label.grid(row=row, column=0, sticky="E")
        name_entry_text = tk.StringVar()
        name_entry_text.set(category.name)
        name_entry = tk.Entry(category_frm, textvariable=name_entry_text)
        name_entry.bind('<KeyRelease>', lambda x: self.on_name_change(name_entry, row))
        name_entry.grid(row=row, column=1, pady=5, sticky="W")

        label = ttk.Label(category_frm, text="Filter: ")
        label.grid(row=row, column=2, sticky="E")
        filter_entry_text = tk.StringVar()
        filter_entry_text.set(category.alarm_category.regex)
        filter_entry = tk.Entry(category_frm, textvariable=filter_entry_text)
        filter_entry.bind('<KeyRelease>', lambda x: self.on_filter_change(filter_entry, row))
        filter_entry.grid(row=row, column=3, pady=5, sticky="W")

        label = ttk.Label(category_frm, text="Background: ")
        label.grid(row=row, column=4, sticky="E")
        bg_button = tk.Button(category_frm,
                              text='     ',
                              command=lambda: self.choose_color(bg_button, row, BACKGROUND),
                              bg=category.alarm_category.bg_color_hex)
        bg_button.grid(row=row, column=5, padx=5, sticky="W")

        label = ttk.Label(category_frm, text="Foreground: ")
        label.grid(row=row, column=6, sticky="E")
        fg_button = tk.Button(category_frm,
                              text='     ',
                              command=lambda: self.choose_color(fg_button, row, FOREGROUND),
                              bg=category.alarm_category.fg_color_hex)
        fg_button.grid(row=row, column=7, padx=5, sticky="W")

        category_frm.grid(row=row)

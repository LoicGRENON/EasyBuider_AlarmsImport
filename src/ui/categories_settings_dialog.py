import copy
import json
import logging
import pickle
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
from tkinter.messagebox import askyesno

from .scrollable_frame import ScrollableFrame
from src.category_settings import CategorySettings

BACKGROUND = 1
FOREGROUND = 2


logger = logging.getLogger(__name__)


class CategoriesSettingsDialog(tk.Toplevel):

    def __init__(self, master, categories_settings, settings_manager, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.categories = categories_settings
        self.settings_manager = settings_manager

        self.title(f'Categories settings')
        self.minsize(600, 200)
        self.geometry('600x400')

        # Make dialog modal
        self.grab_set()

        # Used to check for modifications by serialization
        self._categories_copy = copy.deepcopy(self.categories)

        main_frm = ttk.Frame(self, padding=10)
        frame = ScrollableFrame(main_frm)
        category_frm = ttk.Frame(frame.scrollable_frame)

        self.category_headings(category_frm)
        self.name_entries = []
        for row, category in enumerate(self.categories, start=1):
            self.show_category(category_frm, row, category)

        button = tk.Button(main_frm, text='Apply changes', command=self.on_apply_change_button)

        main_frm.pack(fill='both', expand=True)
        button.pack(side='bottom')
        category_frm.pack()
        frame.pack(fill='both', expand=True)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    @property
    def categories_settings(self):
        return self._categories_copy

    def choose_color(self, button, row, color_type):
        if color_type == FOREGROUND:
            color_type_str = 'foreground'
            default_color = self.categories[row].alarm_category.fg_color_hex
        else:
            color_type_str = 'background'
            default_color = self.categories[row].alarm_category.bg_color_hex

        (rgb_color, html_color) = colorchooser.askcolor(color=default_color,
                                                        title=f"Choose {color_type_str} color for category #{row:0{3}}")
        if html_color:
            if color_type == BACKGROUND:
                self.categories[row].alarm_category.bg_color = rgb_color
                self.name_entries[row].configure(background=html_color)
            elif color_type == FOREGROUND:
                self.categories[row].alarm_category.fg_color = rgb_color
                self.name_entries[row].configure(foreground=html_color)

            # Update button color
            button.configure(bg=html_color)

    def category_headings(self, parent_frame):
        ttk.Label(parent_frame, text="Name").grid(row=0, column=1)
        ttk.Label(parent_frame, text="Filter").grid(row=0, column=2)
        ttk.Label(parent_frame, text="Background").grid(row=0, column=3)
        ttk.Label(parent_frame, text="Foreground").grid(row=0, column=4)

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
            answer = askyesno(title="Unsaved changes",
                              message="Some changes are not saved.\nAre sure you want to exit ?",
                              default="no")

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

    def show_category(self, parent_frame, row: int, category: CategorySettings):
        label = ttk.Label(parent_frame, text=f"#{row}: ")
        label.grid(row=row, column=0, sticky="E")

        name_entry_text = tk.StringVar()
        name_entry_text.set(category.name)
        name_entry = tk.Entry(parent_frame,
                              textvariable=name_entry_text,
                              width=25,
                              background=category.alarm_category.bg_color_hex,
                              foreground=category.alarm_category.fg_color_hex)
        name_entry.bind('<KeyRelease>', lambda x: self.on_name_change(name_entry, row - 1))
        self.name_entries.append(name_entry)
        name_entry.grid(row=row, column=1, padx=5, pady=5)

        filter_entry_text = tk.StringVar()
        filter_entry_text.set(category.alarm_category.regex)
        filter_entry = tk.Entry(parent_frame, textvariable=filter_entry_text, width=30)
        filter_entry.bind('<KeyRelease>', lambda x: self.on_filter_change(filter_entry, row - 1))
        filter_entry.grid(row=row, column=2, padx=5, pady=5)

        bg_button = tk.Button(parent_frame,
                              text='     ',
                              command=lambda: self.choose_color(bg_button, row - 1, BACKGROUND),
                              bg=category.alarm_category.bg_color_hex)
        bg_button.grid(row=row, column=3, padx=5)

        fg_button = tk.Button(parent_frame,
                              text='     ',
                              command=lambda: self.choose_color(fg_button, row - 1, FOREGROUND),
                              bg=category.alarm_category.fg_color_hex)
        fg_button.grid(row=row, column=4, padx=5)

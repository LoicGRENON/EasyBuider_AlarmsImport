import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        yscrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        xscrollbar = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)

        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        xscrollbar.pack(side="bottom", fill="x")
        yscrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

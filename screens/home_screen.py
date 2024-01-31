from tkinter import *
from .parent_screens import FullScreen

class HomeScreen(FullScreen):

    def __init__(self, container):
        super().__init__(container)

        # configure two side-by-side screens
        self.screen_window.grid_rowconfigure(0, weight=1)
        self.screen_window.grid_columnconfigure(0, weight=1)
        self.screen_window.grid_columnconfigure(1, weight=1)

        # ------------------------------------------------------------------------
        # left screen - recent applications
        self.recent_applications = LabelFrame(self.screen_window, bg="blue")
        self.recent_applications.grid_columnconfigure(0, weight=1)
        self.recent_applications.grid(row=0, column=0, sticky="NEWS", padx=5, pady=5)

        self.recent_app_title = Label(self.recent_applications, text="Applications")
        self.recent_app_title.grid(row=0, column=0)

        # ------------------------------------------------------------------------
        # right screen - notes summary
        self.notes = LabelFrame(self.screen_window, bg="red")
        self.notes.grid_columnconfigure(0, weight=1)
        self.notes.grid(row=0, column=1, sticky="NEWS", padx=5, pady=5)

        self.recent_notes_title = Label(self.notes, text="Notes")
        self.recent_notes_title.grid(row=0, column=0)






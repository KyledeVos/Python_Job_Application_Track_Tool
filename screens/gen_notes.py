from ttkbootstrap import *
from .parent_screens import FullScreen

class GeneralNotesScreen(FullScreen):

    def __init__(self, container):
        super().__init__(container)
        
        self.window_title = Label(self.screen_window, text = "General Notes")
        self.screen_window.grid_columnconfigure(0, weight=1)
        self.window_title.grid(row=0, column=0)






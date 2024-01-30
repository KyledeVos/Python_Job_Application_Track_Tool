from tkinter import *

class FullScreen():

    def __init__(self, container):
        self.screen_window = LabelFrame(container)
    
    def get_labelFrame(self):
        return self.screen_window
    
    def load_window(self):
        self.screen_window.grid(row=0, column=0, sticky="NEWS")
    


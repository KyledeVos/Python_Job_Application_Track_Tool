from tkinter import *

class FullScreen():

    def __init__(self, container) -> None:
        self.screen_window = LabelFrame(container)
    
    def get_labelFrame(self):
        return self.screen_window
    
    def load_window(self):
        self.screen_window.grid(row=0, column=0, sticky="NEWS")


class SectionedLeftMinor():

    def __init__(self, container, frame_title) -> None:
        self.enclosing_window = LabelFrame(container)
        self.left_minor_window = LabelFrame(self.enclosing_window, bg='red')
        self.right_major_window = LabelFrame(self.enclosing_window, bg='purple')

        self.configure_sub_windows(frame_title)

    def configure_sub_windows(self, frame_title):
        
        
        self.enclosing_window.grid_columnconfigure(0, weight = 1)
        self.enclosing_window.grid_columnconfigure(1, weight=3)
        self.enclosing_window.grid_rowconfigure(1, weight = 1)
            
        self.window_title = Label(self.enclosing_window, text = frame_title )
        self.window_title.grid(row=0, column=0, columnspan=2, sticky="NEWS")

    def load_left_minor(self):
        self.left_minor_window.grid(row = 1, column= 0, sticky="NEWS")

    def load_right_major(self):
        self.right_major_window.grid(row = 1, column = 1, sticky="NEWS")

    def get_enclosing_window(self):
        return self.enclosing_window

    def get_left_minor(self):
        return self.left_minor_window
    
    def get_right_major(self):
        return self.right_major_window
    


    


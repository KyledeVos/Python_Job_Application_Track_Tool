from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledFrame

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
        self.left_minor_window = LabelFrame(self.enclosing_window)
        self.scrollable_screen = ScrollableScreen(self.enclosing_window, 1, 1)
        self.right_major_window = self.scrollable_screen.get_container()


        self.configure_sub_windows(frame_title)

    def configure_sub_windows(self, frame_title):
        
        self.enclosing_window.grid_columnconfigure(0, weight = 1)
        self.enclosing_window.grid_columnconfigure(1, weight=2)
        self.enclosing_window.grid_rowconfigure(1, weight = 1)
            
        self.window_title = Label(self.enclosing_window, text = frame_title )
        self.window_title.grid(row=0, column=0, columnspan=2, sticky="NEWS")

    def load_left_minor(self):
        self.left_minor_window.grid(row = 1, column= 0, sticky="NEWS")

    def load_right_major(self):
        self.right_major_window.grid(row = 1, column = 1, sticky="NEWS")
        self.scrollable_screen.load_screen()

    def clear_left_minor(self):
        for screen in self.left_minor_window.grid_slaves():
            screen.grid_forget()

    def clear_right_major(self):
        for screen in self.right_major_window.grid_slaves():
            screen.grid_forget()

    def get_enclosing_window(self):
        return self.enclosing_window

    def get_left_minor(self):
        return self.left_minor_window
    
    def get_right_major(self):
        return self.right_major_window
    
class ScrollableScreen():

    def __init__(self, container, row_placement=0, column_placement=0) -> None:

        self.row_placement = row_placement
        self.column_placement = column_placement

        self.container = container

        # Create Scrollable Outer Screen
        self.scrollable = ScrolledFrame(container, autohide=False)
        
        # Second Frame will house widgets that use this parent screen (placed within scrollable screen)
        self.second_frame = Frame(self.scrollable)


    def get_container(self):
        return self.second_frame
    
    def force_scroll(self):
        self.scrollable.enable_scrolling()
    
    def reset_scroll_window(self):
        self.scrollable.yview_moveto(0.0)
    
    def load_screen(self):

        # # move scroll window back to top for each page load
        self.reset_scroll_window()

        # place second frame
        self.second_frame.grid(row=0, column=0, sticky="NEWS", padx=5, pady=5)
        self.scrollable.grid(row=self.row_placement, column=self.column_placement, sticky="NEWS", padx=5, pady=5)







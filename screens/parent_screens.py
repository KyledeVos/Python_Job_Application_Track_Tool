from tkinter import *
from tkinter import ttk

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

        # 1) Create the Main Frame
        self.main_frame = Frame(container, bg="yellow")
        # Make the frame expand to the full size of the window
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight = 1)
        self.main_frame.grid(row=row_placement, column=column_placement, sticky="NEWS", padx=5, pady=5)

        # 2) Create the Canvas
        self.my_canvas = Canvas(self.main_frame)
        self.my_canvas.grid_rowconfigure(0, weight=1)
        self.my_canvas.grid_columnconfigure(0, weight=1)
        self.my_canvas.grid(row = 0, column=0, sticky="NEWS")

        # 3) Add the Scrollbar to the Canvas (it goes to the mainframe)
        self.my_scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL)
        self.my_scrollbar.config(command=self.my_canvas.yview)
        self.my_scrollbar.grid(row = 0, column=0, sticky='NSE')

        # 5) Create another frame within the Canvas
        self.second_frame = Frame(self.my_canvas)


    def get_container(self):
        return self.second_frame
    
    def reset_scroll_window(self):
        self.my_canvas.update_idletasks()
        self.my_canvas.yview_moveto(0)
    
    def load_screen(self):

        # move scroll window back to top for each page load
        self.reset_scroll_window()
                                    
        # 4) Configure the Canvas
        self.my_canvas.configure(yscrollcommand=self.my_scrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))
        # self.my_canvas.bind_all('<MouseWheel>', lambda e: self.my_canvas.yview_scroll(-1 * int(e.delta / 60), "units"))
        # 6) Add a new window to the canvas
        self.my_canvas.create_window((0, 0), window=self.second_frame, anchor="nw")

        # enable window scrolling on load
        self.my_canvas.bind('<Enter>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox("all")))
        self.my_canvas.bind('<MouseWheel>', lambda e: self.my_canvas.yview_scroll(-1 * int(e.delta / 60), "units"))



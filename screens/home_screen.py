from ttkbootstrap import *
from .parent_screens import FullScreen, ScrollableScreen

class HomeScreen(FullScreen):

    def __init__(self, container):
        super().__init__(container)

        # configure two side-by-side screens
        self.screen_window.grid_rowconfigure(1, weight=1)
        self.screen_window.grid_columnconfigure(0, weight=1)
        self.screen_window.grid_columnconfigure(1, weight=1)

        # ------------------------------------------------------------------------
        # left screen - recent applications
        self.left_scrollable = ScrollableScreen(self.screen_window, 1, 0)
        self.left_holder = self.left_scrollable.get_container()
        

        self.recent_applications = LabelFrame(self.left_holder, bootstyle = "default")
        self.recent_applications.grid_columnconfigure(0, weight=1)
        self.recent_applications.grid(row=0, column=0, sticky="NEWS", padx=5, pady=5)

        self.recent_app_title = Label(self.recent_applications, text="Applications")
        self.recent_app_title.grid(row=0, column=0)

        # Add in some default text for size testing
        self.test_label = Label(self.recent_applications, text='This is some default text to get sizing of the left screen')
        self.test_label.grid(row=1, column=0, sticky="NEWS")

        for element in range(1,100):
            Button(self.left_holder, width=30, text = f'button: {element}').grid(row=element, column=0, pady=10, padx = 10)

        # ------------------------------------------------------------------------
        # right screen - notes summary
        self.right_scrollable = ScrollableScreen(self.screen_window, 1, 1)
        self.holding_screen = self.right_scrollable.get_container()
        
        
        
        self.recent_notes_title = Label(self.screen_window, text="Notes", anchor=N)
        self.recent_notes_title.grid(row=0, column=1)

        for element in range(100):
            Button(self.holding_screen, width=30, text = f'button: {element}').grid(row=element, column=0, pady=10, padx = 10)


    def load_window(self):
        super().load_window()
        self.left_scrollable.load_screen()
        self.right_scrollable.load_screen()






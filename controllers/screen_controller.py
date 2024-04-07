from ttkbootstrap import *

# Main Screens
from screens.home_screen import HomeScreen
from screens.job_applications_screen import JobApplicationsScreen
from screens.gen_notes import GeneralNotesScreen

# Sub Menu Screens

class ScreenController():

    def __init__(self, db_controller) -> None:
        self.root_window = Window()
        self.page_title_frame = None
        self.page_title = None
        self.app_screen = None
        self.menu_option = None
        self.current_screen = None
        self.db_controller = db_controller

        # list containing application main screens
        self.screen_dict = None

        self.configure_root_window()
        self.configure_root_sections()

    def configure_root_window(self):
        self.root_window.geometry("1200x900")
        self.root_window.minsize(700, 200)
        self.root_window.grid_columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=0)
        self.root_window.rowconfigure(1, weight=1)

    def configure_root_sections(self):

        # Title Frame to Hold Menu Tab and Application Name
        self.page_title_frame = LabelFrame(self.root_window, bootstyle = 'default')
        self.page_title_frame.grid_columnconfigure(1, weight=1)
        self.page_title_frame.grid(row=0, column=0, sticky=W+E, padx=5, pady=10)

        # Application Title Sub-Section
        self.page_title = Label(self.page_title_frame, text="Personal Job Search Tracker", bootstyle = 'default')
        self.page_title.grid(row=0, column=1, sticky=W+E)

        # Application Screen
        self.app_screen = LabelFrame(self.root_window, bootstyle = 'default')
        self.app_screen.grid_columnconfigure(0, weight=1)
        self.app_screen.grid_rowconfigure(0, weight=1)
        self.app_screen.grid(row=1, column=0, sticky="NEWS")

        # configure different application screens
        self.configure_main_screens()

        # Main Menu Dropdown Sub-Section ----------------------------------------------------------

        # get menu names (keys) from screen.dict -> Dictionary housing constructors for each screen
        self.main_menu_keys = list(self.screen_dict.keys())

        self.main_menu = Menubutton(self.page_title_frame, text = self.main_menu_keys[0], style="primary")
        self.menu = Menu(self.main_menu)

        # variable to track selected main screen
        self.option_variable = StringVar()

        # set each main screen as a radiobutton
        for menu_option in self.main_menu_keys:
            self.menu.add_radiobutton(label=menu_option, value=menu_option, variable=self.option_variable,
                                       command=lambda: self.change_main_screen(self.option_variable))

        # allows association of menu containing radio buttons for screen to MenuButton Widget
        self.main_menu['menu'] = self.menu
        self.main_menu.grid(row=0, column=0, sticky=W+E, padx=5)

        # load home screen
        self.current_screen = self.screen_dict['Home'].load_window()


    def configure_main_screens(self):
        self.screen_dict = {'Home': HomeScreen(self.app_screen),
                            'Job Applications': JobApplicationsScreen(self.app_screen, self.db_controller),
                           'Notes': GeneralNotesScreen(self.app_screen)}
        

    def change_main_screen(self, menu_option):
        # Clear Application Screen
        for screen in self.app_screen.grid_slaves():
            screen.grid_forget()

        # Update Main Menu text to name of new main screen
        self.main_menu.config(text=menu_option.get())

        # change main screen
        self.screen_dict[menu_option.get()].load_window()


    def start_main_screen(self):
        # start running of Application GUI
        self.root_window.mainloop()

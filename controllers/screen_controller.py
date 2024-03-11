from tkinter import *

# Main Screens
from screens.home_screen import HomeScreen
from screens.job_applications_screen import JobApplicationsScreen
from screens.gen_notes import GeneralNotesScreen

# Sub Menu Screens

class ScreenController():

    def __init__(self, db_controller) -> None:
        self.root_window = Tk()
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
        self.root_window.geometry("800x600")
        self.root_window.minsize(700, 200)
        self.root_window.grid_columnconfigure(0, weight=1)
        self.root_window.rowconfigure(0, weight=0)
        self.root_window.rowconfigure(1, weight=1)

    def configure_root_sections(self):

        # Title Frame to Hold Menu Tab and Application Name
        self.page_title_frame = LabelFrame(self.root_window, borderwidth=2, relief="solid", bg="blue", padx=5, pady=5)
        self.page_title_frame.grid_columnconfigure(1, weight=1)
        self.page_title_frame.grid(row=0, column=0, sticky=W+E, padx=5, pady=10)

        # Application Title Sub-Section
        self.page_title = Label(self.page_title_frame, text="Personal Job Search Tracker",borderwidth=1, relief="solid")
        self.page_title.grid(row=0, column=1, sticky=W+E)

        # Application Screen
        self.app_screen = LabelFrame(self.root_window)
        self.app_screen.grid_columnconfigure(0, weight=1)
        self.app_screen.grid_rowconfigure(0, weight=1)
        self.app_screen.grid(row=1, column=0, sticky="NEWS")

        # configure different application screens
        self.configure_main_screens()

        # Main Menu Dropdown Sub-Section ----------------------------------------------------------

        # Main Menu Dropdown
        menu_option = StringVar()
        menu_option.set('Menu')
        main_menu = OptionMenu(self.page_title_frame, menu_option, command=self.change_main_screen, *self.screen_dict)
        main_menu.config(width = 4)
        main_menu.grid(row=0, column=0, sticky=W+E, padx=5)

        # Home (loadup) screen should always have key of 'Home'
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

        self.screen_dict[menu_option].load_window()
        
        # Keep Menu Dropdown text as Menu
        menu_option = StringVar()
        menu_option.set('Menu')
        main_menu = OptionMenu(self.page_title_frame, menu_option, command=self.change_main_screen, *self.screen_dict)
        main_menu.config(width = 4)
        main_menu.grid(row=0, column=0, sticky=W+E, padx=5)


    def start_main_screen(self):
        self.root_window.mainloop()




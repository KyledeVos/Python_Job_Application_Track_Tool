from tkinter import *
from .parent_screens import FullScreen, SectionedLeftMinor
from .new_application_screen import NewApplicationScreen

class JobApplicationsScreen(FullScreen):

    def __init__(self, container):
        super().__init__(container)
        self.left_sub = SectionedLeftMinor(container, "Job Applications")
        self.enclosing_window = self.left_sub.get_enclosing_window()

        self.new_application_btn = None
        self.left_minor_window = self.left_sub.get_left_minor()
        self.left_minor_initialize(self.left_minor_window)
        self.screen_options = self.right_screens_initialize(self.left_sub.get_right_major())


    def left_minor_initialize(self, left_minor_window):
        self.application_home_btn = Button(left_minor_window, text = "Applications Home")
        self.new_application_btn = Button(left_minor_window, text="New Application", 
                                          command=lambda: self.change_right_screen("New Application", self.left_sub.get_right_major()))
        
        self.view_all_btn = Button(left_minor_window, text = "View All Applications")
        self.search_btn = Button(left_minor_window, text="Search Application")
        self.edit_application_btn = Button(left_minor_window, text="Edit Application")
        self.delete_application_btn = Button(left_minor_window, text = "Delete Application")
        

    def right_screens_initialize(self, container):
        return {'New Application': NewApplicationScreen(container)}
    

    def change_right_screen(self, selected_option, parent_container):

        # Clear Application Screen
        for screen in parent_container.grid_slaves():
            screen.grid_forget()

        self.screen_options[selected_option].load_window()
        self.left_sub.load_right_major()

    
    def load_window(self):

        # need to add window loads for left and right screens here
        self.enclosing_window.grid(row=0, column=0, sticky="NEWS")
        self.application_home_btn.grid(row=0, column=0, sticky=W+E)
        self.new_application_btn.grid(row=1, column=0, sticky=W+E)
        self.view_all_btn.grid(row=2, column=0, sticky=W+E)
        self.search_btn.grid(row=3, column=0, sticky=W+E)
        self.edit_application_btn.grid(row=4, column=0, sticky=W+E)
        self.delete_application_btn.grid(row=5, column=0, sticky=W+E)
        

        self.left_sub.load_left_minor()



        







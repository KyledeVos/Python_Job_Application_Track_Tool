from tkinter import *
from .parent_screens import FullScreen, SectionedLeftMinor
from .new_application_screen import NewApplicationScreen

class JobApplicationsScreen(FullScreen):

    def __init__(self, container):
        super().__init__(container)
        self.left_sub = SectionedLeftMinor(container, "Job Applications")
        self.enclosing_window = self.left_sub.get_enclosing_window()

        self.new_application_btn = None

        self.left_minor_initialize()

    def left_minor_initialize(self):
        self.left_minor_window = self.left_sub.get_left_minor()
        self.new_application_btn = Button(self.left_minor_window, text="New Application")
        self.view_all_btn = Button(self.left_minor_window, text = "View All Applications")
        self.search_btn = Button(self.left_minor_window, text="Search Application")
        self.edit_application_btn = Button(self.left_minor_window, text="Edit Application")
        self.delete_application_btn = Button(self.left_minor_window, text = "Delete Application")
        self.application_home_btn = Button(self.left_minor_window, text = "Applications Home")
        


        
    def load_window(self):

        # need to add window loads for left and right screens here
        self.enclosing_window.grid(row=0, column=0, sticky="NEWS")
        self.new_application_btn.grid(row=0, column=0, sticky=W+E)
        self.view_all_btn.grid(row=1, column=0, sticky=W+E)
        self.search_btn.grid(row=2, column=0, sticky=W+E)
        self.edit_application_btn.grid(row=3, column=0, sticky=W+E)
        self.delete_application_btn.grid(row=4, column=0, sticky=W+E)
        self.application_home_btn.grid(row=5, column=0, sticky=W+E)



        







from ttkbootstrap import *
from .parent_screens import FullScreen, SectionedLeftMinor
from .sub_screens.new_application import NewApplicationScreen
from .sub_screens.delete_screen import DeleteApplication
from .sub_screens.job_view_screen import ViewAllApplicationsScreen

class JobApplicationsScreen(FullScreen):

    def __init__(self, container, db_controller):
        super().__init__(container)
        self.db_controller = db_controller
        self.left_sub = SectionedLeftMinor(container, "Job Applications")
        self.enclosing_window = self.left_sub.get_enclosing_window()

        self.new_application_btn = None
        self.left_minor_window = self.left_sub.get_left_minor()
        self.left_minor_initialize(self.left_minor_window)
        self.screen_options = self.right_screens_initialize(self.left_sub.get_right_major())
        


    def left_minor_initialize(self, left_minor_window):
        self.new_application_btn = Button(left_minor_window, text="New Application", 
                                          command=lambda: self.change_right_screen("New Application"))
        
        self.view_all_btn = Button(left_minor_window, text = "View All Applications", 
                                   command=lambda: self.change_right_screen("View All Applications"))
        
        self.search_btn = Button(left_minor_window, text="Search Application")
        self.delete_application_btn = Button(left_minor_window, text = "Delete Application",
                                    command=lambda: self.change_right_screen("Delete Application"))
        

    def right_screens_initialize(self, container):
        
        return {'New Application': NewApplicationScreen(container, self.db_controller),
                'View All Applications': ViewAllApplicationsScreen(container, self.db_controller, self.left_sub),
                'Delete Application': DeleteApplication(container, self.db_controller)}
    

    def change_right_screen(self, selected_option):

        # Clear Application Screen
        self.left_sub.clear_right_major()

        self.left_sub.load_right_major()
        self.screen_options[selected_option].load_window()
        
        self.left_sub.window_title.config(text=selected_option)

    
    def load_window(self):

        # CHANGE TO APPLICATION HOME PAGE WHEN CREATED
        self.change_right_screen("View All Applications")

        # need to add window loads for left and right screens here
        self.enclosing_window.grid(row=0, column=0, sticky="NEWS")
        self.new_application_btn.grid(row=0, column=0, sticky=W+E)
        self.view_all_btn.grid(row=1, column=0, sticky=W+E)
        self.search_btn.grid(row=2, column=0, sticky=W+E)
        self.delete_application_btn.grid(row=3, column=0, sticky=W+E)
        
        self.left_sub.load_left_minor()


from tkinter import *
from .parent_screens import FullScreen, SectionedLeftMinor

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
        self.application_home_btn = Button(left_minor_window, text = "Applications Home")
        self.new_application_btn = Button(left_minor_window, text="New Application", 
                                          command=lambda: self.change_right_screen("New Application", self.left_sub.get_right_major()))
        
        self.view_all_btn = Button(left_minor_window, text = "View All Applications", 
                                   command=lambda: self.change_right_screen("View All Applications", self.left_sub.get_right_major()))
        
        self.search_btn = Button(left_minor_window, text="Search Application")
        self.edit_application_btn = Button(left_minor_window, text="Edit Application")
        self.delete_application_btn = Button(left_minor_window, text = "Delete Application")
        

    def right_screens_initialize(self, container):
        return {'New Application': NewApplicationScreen(container, self.db_controller),
                'View All Applications': ViewAllApplicationsScreen(container, self.db_controller)}
    

    def change_right_screen(self, selected_option, parent_container):

        # Clear Application Screen
        for screen in parent_container.grid_slaves():
            screen.grid_forget()

        self.screen_options[selected_option].load_window()
        self.left_sub.load_right_major()

        self.left_sub.window_title.config(text=selected_option)

    
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


# New Job Application Sub-Screen
class NewApplicationScreen(FullScreen):

    def __init__(self, container, db_controller):
        super().__init__(container)
        self.db_controller = db_controller
        self.all_options = {}

        # ----------------------------------------------------------------
        # company name
        self.company_name_lbl = Label(container, text="'Company:")
        self.company_name = Entry(container, width=50, borderwidth=1)
        
        # ----------------------------------------------------------------
        # Job Position
        self.position_lbl = Label(container, text="Position")
        self.position = Entry(container, width=50, borderwidth=2)

        # ----------------------------------------------------------------
        # Salary
        self.salary_lbl = Label(container, text="Salary")
        self.salary = Entry(container, width=50, borderwidth=2)

        # ----------------------------------------------------------------
        # Date Applied
        self.application_date_lbl = Label(container, text="Date Applied")
        self.application_date = Entry(container, width=50, borderwidth=2)
        
        # ----------------------------------------------------------------
        # Location
        self.location_lbl = Label(container, text="Location")
        self.location = Entry(container, width=50, borderwidth=2)

        # ----------------------------------------------------------------
        # Description
        self.description_lbl = Label(container, text="Description")
        self.description = Entry(container, width=50, borderwidth=2)

        # ----------------------------------------------------------------
        # Employment Type

        self.emp_type_label = Label(container, text="Employment Type")
        
        current_options = self.db_controller.retrieve_id_single_col("type" ,"employment_types")
        self.all_options['employment_types'] = current_options

        self.emp_type = StringVar()
        self.emp_type.set("Full Time")
        self.emp_type_menu = OptionMenu(container, self.emp_type, *[item[1] for item in current_options])
        self.emp_type_menu.config(anchor=W)

        # ----------------------------------------------------------------
        # Contract Duration

        self.contract_duration_lbl = Label(container, text="Contract Duration")

        current_options = self.db_controller.retrieve_id_single_col("duration" ,"contract_period")
        self.all_options['contract_period'] = current_options

        self.contract_duration = StringVar()
        self.contract_duration.set("3 Months")
        self.contract_duration_menu = OptionMenu(container, self.contract_duration, *[item[1] for item in current_options])
        self.contract_duration_menu.config(anchor=W)

        # ----------------------------------------------------------------
        # Application Status

        self.app_status_lbl = Label(container, text="Application Status")

        current_options = self.db_controller.retrieve_id_single_col("status" ,"application_status")
        self.all_options['application_status'] = current_options

        self.app_status = StringVar()
        self.app_status.set("Applied")
        self.app_status_menu = OptionMenu(container, self.app_status , *[item[1] for item in current_options])
        self.app_status_menu.config(anchor=W)

        # ----------------------------------------------------------------
        # Submit Button

        self.save_new_application = Button(container, text="Save", command=self.save_new_data)



    def save_new_data(self):
        data_values = [self.company_name.get(),
                        self.position.get(),
                        self.salary.get(),
                        self.application_date.get(),
                        self.location.get(),
                        self.description.get(),
                        self.find_match(self.emp_type.get(), self.all_options['employment_types']),
                        self.find_match(self.contract_duration.get(), self.all_options['contract_period']),
                        self.find_match(self.app_status.get(), self.all_options['application_status']),
                       ]

        self.db_controller.write_single_row("job_applications", data_values)

        # reset input fields
        self.company_name.delete(0, END)
        self.position.delete(0, END)
        self.salary.delete(0, END)
        self.application_date.delete(0, END)
        self.location.delete(0, END)
        self.description.delete(0, END)


    def find_match(self, description, val_list):
        for item in val_list:
            if item[1] == description:
                return item[0]
    
    def load_window(self):
        
        self.company_name_lbl.grid(row=0, column=0, padx=2, pady=2, sticky=W+E)
        self.company_name.grid(row=0, column=1, sticky=W+E)
        self.position_lbl.grid(row=1, column=0, padx=2, pady=2, sticky=W+E)
        self.position.grid(row=1, column=1, sticky=W+E)
        self.salary_lbl.grid(row=2, column=0, padx=2, pady=2, sticky=W+E)
        self.salary.grid(row=2, column=1, sticky=W+E)
        self.application_date_lbl.grid(row=3, column=0, padx=2, pady=2, sticky=W+E)
        self.application_date.grid(row=3, column=1, sticky=W+E)
        self.location_lbl.grid(row=4, column=0, padx=2, pady=2, sticky=W+E)
        self.location.grid(row=4, column=1, sticky=W+E)
        self.description_lbl.grid(row=5, column=0, padx=2, pady=2, sticky=W+E)
        self.description.grid(row=5, column=1, sticky=W+E)
        self.emp_type_label.grid(row = 6, column=0, padx=2, pady=2, sticky=W+E)
        self.emp_type_menu.grid(row=6, column=1, sticky=W)
        self.contract_duration_lbl.grid(row = 7, column=0, padx=2, pady=2, sticky=W+E)
        self.contract_duration_menu.grid(row=7, column=1, sticky=W)
        self.app_status_lbl.grid(row = 8, column=0, padx=2, pady=2, sticky=W+E)
        self.app_status_menu.grid(row=8, column=1, sticky=W)

        self.save_new_application.grid(row=9, column=0, sticky=W+E)


# View All Applications Screen
class ViewAllApplicationsScreen(FullScreen):

    def get_data(self):
        print(self.db_controller.retrieve_all_data("job_applications"))

    def __init__(self, container, db_controller):
        super().__init__(container)
        self.container = container
        self.db_controller = db_controller
        self.empty_label = Label(container)

        
    def load_window(self):
        # self.test_btn.grid(row=0, column=0)
        current_applications = self.db_controller.retrieve_col_specific(['company, position'], 'job_applications')

        if len(current_applications) == 0:
            self.empty_label.config(text="No Job Applications")
        else:

            class Job_Instance():

                def __init__(self, count, application, container):
                    self.id = application[0]

                    self.job_count = Label(container, text=f"{count + 1}", width=5, anchor=W)
                    self.job_count.bind("<Button-1>", self.open_job_application)

                    self.company = Label(container, text=application[1], width=20,anchor=W)
                    self.company.bind("<Button-1>", self.open_job_application)

                    self.position = Label(container, text=application[2], width=20, anchor=W)
                    self.position.bind("<Button-1>", self.open_job_application)

                def open_job_application(self, event):
                    print(self.id)

                def place_on_screen(self, row_count):
                    self.job_count.grid(row = row_count, column=0, pady=2)
                    self.company.grid(row=row_count, column=1, pady=2)
                    self.position.grid(row=row_count, column=2, pady=2)


                             
            for count, application in enumerate(current_applications):
                current_job = Job_Instance(count, application, self.container)
                current_job.place_on_screen(count)







        







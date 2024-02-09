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
                                          command=lambda: self.change_right_screen("New Application"))
        
        self.view_all_btn = Button(left_minor_window, text = "View All Applications", 
                                   command=lambda: self.change_right_screen("View All Applications"))
        
        self.search_btn = Button(left_minor_window, text="Search Application")
        self.delete_application_btn = Button(left_minor_window, text = "Delete Application")
        

    def right_screens_initialize(self, container):
        return {'New Application': NewApplicationScreen(container, self.db_controller),
                'View All Applications': ViewAllApplicationsScreen(container, self.db_controller, self.left_sub)}
    

    def change_right_screen(self, selected_option):

        # Clear Application Screen
        self.left_sub.clear_right_major()

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
        self.delete_application_btn.grid(row=4, column=0, sticky=W+E)
        

        self.left_sub.load_left_minor()


# New Job Application Sub-Screen
class NewApplicationScreen(FullScreen):

    def __init__(self, container, db_controller):
        super().__init__(container)
        self.db_controller = db_controller

        self.single_data_inputs = []
        self.menu_data_inputs = []

        self.job_attributes_titles = self.db_controller.retrieve_job_data_configured()
        # print(job_attributes_titles)

        for val_name in self.job_attributes_titles['single_data']:
            self.single_data_inputs.append((Label(container, text=val_name), Entry(container, width=50, borderwidth=1)))

        # Menu Option Configuration
        class MenuInput():

            def __init__(self, default_value):
                self.input_val = StringVar()
                self.input_val.set(default_value)

            def get_input_val(self):
                return self.input_val
            

        for menu_option in self.job_attributes_titles['menu_data']:
            
            value_holder = MenuInput(menu_option[1][0][1]).get_input_val()
            menu_options = [val[1] for val in menu_option[1]]

            # Form: (Label, input_holder, OptionMenu)
            self.menu_data_inputs.append((Label(container, text=menu_option[0]), 
                                     value_holder,
                                     OptionMenu(container, value_holder, *menu_options)))
            
        self.save_new_application = Button(container, text="Save", command=self.save_data)

    
    def return_id_from_name(self, description, label_name, val_list):
        # for item in val_list:
        #     if item[1] == description:
        #         return item[0]

        for val in val_list:
            if val[0] == label_name:
                for inner_tup in val[1]:
                    if inner_tup[1] == description:
                        return inner_tup[0]
                    
        return None

    def save_data(self):
        data_values = []
        for single_input in self.single_data_inputs:
            data_values.append(single_input[1].get())

        for menu_input in self.menu_data_inputs:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
            
            data_values.append(self.return_id_from_name(selected_option, menu_title, self.job_attributes_titles['menu_data']))

        self.db_controller.write_single_row("job_applications", data_values)

        # clear input fields after save
        for input_field in self.single_data_inputs:
            input_field[1].delete(0, END)


    def load_window(self):

        row_count = 0

        for single_tup in self.single_data_inputs:
            single_tup[0].grid(row=row_count, column = 0, padx=2, pady=2, sticky=W+E)
            single_tup[1].grid(row = row_count, column = 1 , sticky=W+E)
            row_count += 1
        
        for menu_tup in self.menu_data_inputs:
            menu_tup[0].grid(row=row_count, column = 0, padx=2, pady=2, sticky=W+E)
            menu_tup[2].grid(row = row_count, column = 1 , sticky=W)
            row_count += 1
        
        self.save_new_application.grid(row=row_count, column=0, sticky=W+E)

        
# View All Applications Screen
class ViewAllApplicationsScreen(FullScreen):


    def __init__(self, container, db_controller, left_sub_window):
        super().__init__(container)
        self.container = container
        self.db_controller = db_controller
        self.empty_label = Label(container)
        self.left_sub_window = left_sub_window

    def get_data(self):
        print(self.db_controller.retrieve_all_data("job_applications"))

        
    def load_window(self):
        # self.test_btn.grid(row=0, column=0)
        current_applications = self.db_controller.retrieve_col_specific(['company, position'], 'job_applications')

        if len(current_applications) == 0:
            self.empty_label.config(text="No Job Applications")
        else:

            class Job_Instance():

                def __init__(self, count, application, container, left_sub_window, db_controller):
                    self.left_sub_window = left_sub_window
                    self.db_controller = db_controller
                    self.id = application[0]

                    self.job_count = Label(container, text=f"{count + 1}", width=5, anchor=W)
                    self.job_count.bind("<Button-1>", self.open_job_application)

                    self.company = Label(container, text=application[1], width=20,anchor=W)
                    self.company.bind("<Button-1>", self.open_job_application)

                    self.position = Label(container, text=application[2], width=20, anchor=W)
                    self.position.bind("<Button-1>", self.open_job_application)

                def open_job_application(self, event):
                    JobView(self.left_sub_window.get_right_major(), self.left_sub_window, self.db_controller, self.id).load_window()

                def place_on_screen(self, row_count):
                    self.job_count.grid(row = row_count, column=0, pady=2)
                    self.company.grid(row=row_count, column=1, pady=2)
                    self.position.grid(row=row_count, column=2, pady=2)
 
            for count, application in enumerate(current_applications):
                current_job = Job_Instance(count, application, self.container, self.left_sub_window, self.db_controller)
                current_job.place_on_screen(count)


# View Specific Job
class JobView(FullScreen):

    def __init__(self, container, left_minor_subscreen, db_controller, job_id) -> None:
        self.left_minor_subscreen = left_minor_subscreen
        self.container = container
        self.db_controller = db_controller
        self.job_id = job_id
        self.job_data = db_controller.retrieve_job_data_configured(job_id)


    def load_window(self):
        self.left_minor_subscreen.clear_right_major()
        
        # add each job column name and corresponding data (as input) to screen
        for count, job_attribute in enumerate(self.job_data):
            label = Label(self.container, text=job_attribute[0])
            input = Entry(self.container)
            input.insert(0, job_attribute[1])
            label.grid(row=count, column=0, pady=2, padx=2, sticky=W+E)
            input.grid(row=count, column=1, pady=2, padx=2, sticky=W+E)








        







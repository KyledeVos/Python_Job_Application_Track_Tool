from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ..parent_screens import FullScreen
from .job_progress_instance import ProgressInstanceWindow, DataConverter, MenuInput

# New Job Application Sub-Screen
class NewApplicationScreen(FullScreen):

    def __init__(self, container, db_controller):
        super().__init__(container)
        self.db_controller = db_controller
        self.data_converter = DataConverter()
        self.container = container

        self.row_count = 0

        # ---------------------------------------------------------------
        # JOB BASIC INFO

        self.single_data_inputs = []
        self.menu_data_inputs = []

        self.job_attributes_titles = self.db_controller.retrieve_job_data_configured()

        for val_name in self.job_attributes_titles['single_data']:
            self.single_data_inputs.append((Label(container, text=val_name, anchor=W),
                                            Entry(container, width=50, borderwidth=1)))

        for menu_option in self.job_attributes_titles['menu_data']:
            
            value_holder = MenuInput(menu_option[1][0][1]).get_input_val()
            menu_options = [val[1] for val in menu_option[1]]

            # Form: (Label, input_holder, OptionMenu)
            self.menu_data_inputs.append((Label(container, text=menu_option[0], anchor=W), 
                                     value_holder,
                                     OptionMenu(container, value_holder, *menu_options)))
        
        
        # ---------------------------------------------------------------
        # JOB PROGRESS TRACK SECTION
        
        # retrieve job progress config data
        self.progress_attributes = self.db_controller.retrieve_job_progress_column_names()

        # hold list of progress data after save  
        self.progress_instance_list = []
        # list of buttons to be disabled/enabled during progress creation
        self.buttons_list = []

        self.job_progress_frame = Frame(container, borderwidth=2, relief='solid', padx=5, pady=5)
        self.add_progress_btn = Button(self.job_progress_frame, text='Add Progress Note', padx=5, pady=5, command=self.load_progress_window)

        self.buttons_list.append(self.add_progress_btn)

        self.progress_counter = len(self.progress_instance_list) + 1
        self.progress_count_label = Label(self.job_progress_frame, text=f"Progress Notes: {self.progress_counter - 1}",
                                      padx=5, pady=5)

        # list to store single data inputs (one-line)
        self.single_data_list = []
        # list to store foreign key inputs
        self.fk_data = []
        # list to store single data inputs needing larger input box
        self.large_box_data = []

        # new progress window screen
        self.progress_window = ProgressInstanceWindow(self.progress_attributes, self.db_controller, self.single_data_list, self.large_box_data,
                                                      self.fk_data, self.buttons_list, self.load_window, self.retrieve_progress_data, None, None)       

        # ---------------------------------------------------------------
        # JOB NOTES SECTION
        self.new_note_btn = Button(container, text='Add Job Note', anchor=W)

        # ---------------------------------------------------------------
        # Save Application Button
        self.save_new_application = Button(container, text="Save", command=self.save_data)
        self.buttons_list.append(self.save_new_application)

    def load_progress_window(self):
        # initializes all widgets in progress window and populates single_data_list, large_box_data
        # and fk_data lists with values
        self.progress_window.create_window()


    def retrieve_progress_data(self):
        # progress data retrieval order designed to match database format as:
        # single,line inputs, multil-line data-inputs (text boxes), foreign-tables menu inputs, 

        # list to store current progress note data (appended to progress_instance_list at end)
        self.progress_counter += 1
        # correct progress count label in main application
        self.progress_count_label.config(text=f"Progress Notes: {self.progress_counter - 1}")
        self.progress_count_label.grid(row=0, column=1, padx=10, pady=2)
        self.row_count += 1

        progress_instance = []

        # 1) Retrieve Single Items
        for item in self.single_data_list:
            progress_instance.append(item.get())

        # 2) Retrieve multi-line input data
        for item in self.large_box_data:
            progress_instance.append(item.get("1.0", END).strip())
                
        # 3) Retrieve Foreign-Key (Menu-Based Data)
        for menu_input in self.fk_data:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
        
            progress_instance.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.progress_attributes['fk_data']))

        # Add Progress instance to list of instances
        # NOTE - current implementation still needs job_id retrieved only after save of new job application
        self.progress_instance_list.append(progress_instance)

        # clear lists
        self.single_data_list.clear()
        self.large_box_data.clear()
        self.fk_data.clear()

        # print message to user that progres instance has been added to list (not saved in db)
        messagebox.showinfo(message='Job Progress has been added on')

        # re-enable buttons to add progress_instance, save new application and close progress window
        self.progress_window.enable_buttons_close_window()


    def save_data(self):

        data_values = []
        for single_input in self.single_data_inputs:
            data_values.append(single_input[1].get())

        for menu_input in self.menu_data_inputs:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
            
            data_values.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.job_attributes_titles['menu_data']))

        # save new job application and retrieve id
        job_id = self.db_controller.write_single_job_no_id(data_values)
        self.db_controller.write_job_progress(self.progress_instance_list , job_id)

        # clear input fields after save
        for input_field in self.single_data_inputs:
            input_field[1].delete(0, END)

        # Display Message to user that Application has been saved
        messagebox.showinfo(message='Application has been saved')

        # clear progress instanc list after job application save
        self.progress_instance_list.clear()
        # reset progress counter
        self.progress_counter = 1
        self.progress_count_label.destroy()
        self.progress_count_label = Label(self.job_progress_frame, text=f"Progress Notes: {self.progress_counter - 1}",
                                      padx=5, pady=5)
        self.load_window()


    def load_window(self):

        # load single data inputs
        for single_tup in self.single_data_inputs:
            single_tup[0].grid(row=self.row_count, column = 0, padx=2, pady=5, sticky=W+E)
            single_tup[1].grid(row = self.row_count, column = 1 , sticky=W+E)
            self.row_count += 1
        
        # load menu data inputs
        for menu_tup in self.menu_data_inputs:
            menu_tup[0].grid(row=self.row_count, column = 0, padx=2, pady=5, sticky=W+E)
            menu_tup[2].grid(row = self.row_count, column = 1 , sticky=W)
            self.row_count += 1

        # load job progress section (in main application)
        self.job_progress_frame.grid(row=self.row_count, column=0, columnspan=2, padx=2, pady=5, sticky=W+E)
        self.add_progress_btn.grid(row=0, column=0, padx=2, pady=5)
        if self.progress_counter > 1:
            self.progress_count_label.grid(row=0, column=1, padx=10, pady=2)
        self.row_count += 1

        # ------------------------------------------------------------------------
        # BUTTONS
        self.save_new_application.grid(row=self.row_count, column=0, sticky=W+E)
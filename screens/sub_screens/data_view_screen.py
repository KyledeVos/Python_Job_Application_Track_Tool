from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ..parent_screens import FullScreen


# HELPER CLASS FOR MENU BASED DATA
class MenuInput():

    def __init__(self, default_value):
        self.input_val = StringVar()
        self.input_val.set(default_value)

    def get_input_val(self):
        return self.input_val

# HELPER CLASS FOR DESCRIPTION TO ID CONVERSION
class DataConverter():

    def return_id_from_name(self, description, label_name, val_list):
        for val in val_list:
            if val[0] == label_name:
                for inner_tup in val[1]:
                    if inner_tup[1] == description:
                        return inner_tup[0]     
        return None



# View All Applications Screen
class ViewAllApplicationsScreen(FullScreen):

    def __init__(self, container, db_controller, left_sub_window):
        super().__init__(container)
        self.container = container
        self.db_controller = db_controller
        self.empty_label = Label(container)
        self.left_sub_window = left_sub_window

        # retrieve column names adding 'number' column (ignoring id column)
        self.column_titles = None

    def get_data(self):
        print(self.db_controller.retrieve_all_job_data())

        
    def load_window(self):
        
        # retrieve job_application_data
        current_applications = self.db_controller.retrieve_job_display_cols()


        if len(current_applications) == 0:
            self.empty_label.config(text="No Job Applications")
            self.empty_label.grid(row=0, column=0)
        else:
            self.column_titles = ['Number']

            self.column_titles += [name.title().replace("_", " ") for name in self.db_controller.retrieve_job_column_names()[1:len(current_applications[0])]]

            class Job_Instance():

                def __init__(self, count, application, container, left_sub_window, db_controller):
                    self.left_sub_window = left_sub_window
                    self.db_controller = db_controller
                    # retrieve id of application needed to load specific job data
                    self.id = application[0]
                    # new list with current job count and remaining columns to be displayed
                    self.job_data_columns = [count] + list(application)[1:]
                    # list to hold Label attributes
                    self.job_data_values = []

                    for count, column in enumerate(self.job_data_columns):
                        
                        if count == 0:
                            # reduce label width for row count
                            current_label = Label(container, text=column, width=8, anchor=W)
                        else:
                            current_label = Label(container, text=column, width=20, anchor=W)

                        current_label.bind("<Button-1>", self.open_job_application)
                        self.job_data_values.append(current_label)

                def open_job_application(self, event):
                    JobView(self.left_sub_window.get_right_major(), self.left_sub_window, self.db_controller, self.id).load_window()

                def place_on_screen(self, row_count):
                    for col_count, job_instance in enumerate(self.job_data_values):
                        job_instance.grid(row = row_count, column=col_count, padx=10, pady=2)
                        job_instance.grid(row=row_count, column=col_count,padx = 10, pady=2)
                        job_instance.grid(row=row_count, column=col_count, padx = 10, pady=2)

            for count, application in enumerate(current_applications):
                # Add Column Titles
                if count == 0:
                    for col_count, title in enumerate(self.column_titles):
                        # Set reduced width for row count
                        if col_count == 0:
                            current_label = Label(self.container, text=title, width=8, anchor=W)
                        else:
                        # Set longer width for other rows (company, position, etc.)
                            current_label = Label(self.container, text=title, width=20, anchor=W)
                        current_label.grid(row=0, column=col_count, pady=2)

                # Create Job Instane (with job data) and place on screen
                current_job = Job_Instance(count+1, application, self.container, self.left_sub_window, self.db_controller)
                current_job.place_on_screen(count+1)

# View Specific Job
class JobView(FullScreen):

    def __init__(self, container, left_minor_subscreen, db_controller, job_id) -> None:
        self.left_minor_subscreen = left_minor_subscreen
        self.container = container
        self.db_controller = db_controller
        self.job_id = job_id 
        self.job_data = db_controller.retrieve_job_data_configured(job_id)
        self.data_converter = DataConverter()

        self.single_data_inputs = []
        self.menu_data_inputs = []

        # retrieve job_application_data
        self.job_attributes_titles = self.db_controller.retrieve_job_data_configured(job_id)
        # retrieve most recent job progress data - function call below:
        # sets return_one to True and display_only to True
        self.recent_job_progress = self.db_controller.retrieve_job_progress_data(job_id, True, True)

        # ----------------------------------------------------------------------------
        # JOB BASIC INFO SECTION

        self.basic_title = Label(container, padx=5, text="Job Information", anchor='w')
        self.basic_info_frame = Frame(container, padx=5, pady=5, borderwidth=2, relief='solid')

        # Retrieve single data input labels and assigned value
        for data_tup in self.job_attributes_titles['single_data']:
            new_Entry = Entry(self.basic_info_frame, width = 50, borderwidth=1)
            new_Entry.insert(0, data_tup[1])
            self.single_data_inputs.append((Label(self.basic_info_frame, text=data_tup[0], anchor='e'), new_Entry))


        for menu_option in self.job_attributes_titles['menu_data']:
            
            value_holder = MenuInput(menu_option[2]).get_input_val()
            menu_options = [val[1] for val in menu_option[1]]

            # Form: (Label, input_holder, OptionMenu)
            self.menu_data_inputs.append((Label(self.basic_info_frame, text=menu_option[0], anchor='e'), 
                                     value_holder,
                                     OptionMenu(self.basic_info_frame, value_holder, *menu_options)))
            
        self.update_application_btn = Button(self.basic_info_frame, text="Save Changes", command=self.update_data)

        # ----------------------------------------------------------------------------
        # JOB PROGRESS SECTION - Display most recent job progress (no edit functionality)
        
        # check if current job has job progress data
        if self.recent_job_progress != None:
            self.progress_title = Label(container, text = "Latest Progress Note", anchor='w')
            self.progress_data_frame = Frame(container, padx=5, pady=5, borderwidth=2, relief='solid')
            self.progress_data_frame.grid_columnconfigure(1, weight=1)
            self.edit_latest_progress_btn = Button(self.progress_data_frame, text="Edit",
                                                    anchor='center')
            

            # retrieve large_text_box columns and fk_table joining column names
            large_box_cols =[]
            fk_table_cols = []

            for column_tup in self.recent_job_progress['column_info']:
                if column_tup[0] == "large_box_columns":
                    large_box_cols = column_tup[1]
                elif column_tup[0] == 'fk_columns':
                    fk_table_cols = column_tup[1]
            
            # lists holding single_value, fk_data and large_text box data - DISPLAY ONLY
            self.single_data_labels = []
            self.fk_data_labels = []
            self.large_box_labels = []

        
            for count, col in enumerate(self.recent_job_progress['col_list']):

                # do not add a row for job progress id
                if col == 'id':
                    continue

                elif col in large_box_cols:

                    # create frame to hold large_box_data textbox and scrollbar
                    large_box_frame = Frame(self.progress_data_frame, padx=10)
                    # allow mousewheel/trackpad to scroll text box
                    large_box_frame.bind('<Enter>', lambda e: self.enable_inner_scroll(large_box_frame, text_box))
                    large_box_frame.bind('<Leave>', lambda e: self.disable_inner_scroll(large_box_frame, text_box))


                    text_box = Text(large_box_frame, width=40, height=10, padx=10, pady=5, 
                                    borderwidth=2, relief='solid')
                    text_box.grid(row =0, column=0, sticky='w')
                    text_box.insert("1.0", self.recent_job_progress['val_list'][count])

                    # create and configure text box - scrolls text box
                    scrollbar = ttk.Scrollbar(self.progress_data_frame, orient='vertical', command=text_box.yview)
                    text_box.config(yscrollcommand=scrollbar.set)
                    scrollbar.config(command=text_box.yview)
                    large_box_frame.bind('<Enter>', lambda e: text_box.yview_scroll(-1 * int(e.delta / 60), "units"))
                    
                    

                    self.large_box_labels.append((Label(self.progress_data_frame, text=col.title().replace("_", " "), anchor='w'),
                                                  large_box_frame, scrollbar))
                elif col in fk_table_cols:
                    self.fk_data_labels.append(
                        (Label(self.progress_data_frame, text=col.title().replace("_", " "), anchor='e'), 
                         Label(self.progress_data_frame, text=self.recent_job_progress['val_list'][count],
                               padx=10, pady=5, anchor='w')))
                else:
                    self.single_data_labels.append(
                        (Label(self.progress_data_frame, text=col.title().replace("_", " ") + ":", anchor='e'),
                         Label(self.progress_data_frame, text=self.recent_job_progress['val_list'][count], padx=10, pady=5, anchor='w')))
                    


        # EXTRA
        self.btn_list = []
        for i in range(0, 10):
            self.btn_list.append(Button(container, text=i))

                    
    def enable_inner_scroll(self, frame_box, text_box):
        frame_box.bind_all('<MouseWheel>',lambda e: text_box.yview_scroll(-1 * int(e.delta / 60), "units"))

    def disable_inner_scroll(self, frame_box, text_box):
        frame_box.bind_all('<MouseWheel>',lambda e: None)
    
    def load_window(self):
        self.left_minor_subscreen.clear_right_major()

        row_count = 0
        self.basic_title.grid(row=row_count, column=0, sticky="NEWS", padx=5, pady=5)
        row_count += 1
        self.basic_info_frame.grid(row=row_count, column=0, columnspan=2, sticky="NEWS", padx=5, pady=5)
        row_count += 1
        basic_row_count = 0
        

        for single_tup in self.single_data_inputs[1:]:
            single_tup[0].grid(row=basic_row_count, column = 0, padx=5, pady=2, sticky=W+E)
            single_tup[1].grid(row = basic_row_count, column = 1 , sticky=W+E)
            basic_row_count += 1
        
        for menu_tup in self.menu_data_inputs:
            menu_tup[0].grid(row=basic_row_count, column = 0, padx=5, pady=2, sticky=W+E)
            menu_tup[2].grid(row = basic_row_count, column = 1 , sticky=W)
            basic_row_count += 1
        
        self.update_application_btn.grid(row=basic_row_count, column=0, sticky=W+E, pady=5)
        basic_row_count += 1

        # latest job progress section
        if self.recent_job_progress != None:
            self.progress_title.grid(row=row_count, column=0, sticky="NEWS")
            row_count += 1
            self.progress_data_frame.grid(row=row_count, column=0, columnspan=2, sticky="NEWS", padx=5, pady=5)
            row_count += 1
            progress_row_count = 0

            self.edit_latest_progress_btn.grid(row=progress_row_count, column=0, sticky="NEWS")
            progress_row_count += 1
        
            for single_line_label_tup in self.single_data_labels:
                single_line_label_tup[0].grid(row = progress_row_count, column = 0, padx = 5, sticky=W+E)
                single_line_label_tup[1].grid(row = progress_row_count, column = 1, padx = 5, sticky=W+E)
                progress_row_count += 1

            for fk_label_tup in self.fk_data_labels:
                fk_label_tup[0].grid(row = progress_row_count, column = 0, padx = 5, sticky=W+E)
                fk_label_tup[1].grid(row = progress_row_count, column = 1, padx = 5, sticky=W+E)
                progress_row_count += 1 

            for large_box_item_tup in self.large_box_labels:
                large_box_item_tup[0].grid(row = progress_row_count, column = 0, padx = 5, pady = 10, sticky=W+E)
                progress_row_count += 1
                large_box_item_tup[1].grid(row = progress_row_count, column = 0, columnspan = 2, padx = 5, pady = 2, sticky=W+E)
                large_box_item_tup[2].grid(row = progress_row_count, column = 1, sticky="NSE")
                progress_row_count += 1

        # Extra
        for btn in self.btn_list:
            btn.grid(row=row_count, column=0)
            row_count += 1


    def update_data(self):

        data_values = []
        column_names = self.db_controller.retrieve_job_column_names()

        for single_input in self.single_data_inputs:
            data_values.append(single_input[1].get())

        for menu_input in self.menu_data_inputs:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
            
            data_values.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.job_attributes_titles['menu_data']))

        data_values.append(self.job_id)
        data_values = tuple(data_values)

        self.db_controller.update_job_application(column_names, data_values)

        # Display Message to user that Application has been updated
        messagebox.showinfo(message='Changes have been saved')
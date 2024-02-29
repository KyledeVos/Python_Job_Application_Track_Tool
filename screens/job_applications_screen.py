from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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

        # hold list of progress data after save  
        self.progress_instance_list = []
        
        self.job_progress_frame = Frame(container, borderwidth=2, relief='solid', padx=5, pady=5)
        self.add_progress_btn = Button(self.job_progress_frame, text='Add Progress Note', padx=5, pady=5, command=self.load_progress_window)

    
        # ---------------------------------------------------------------
        # JOB NOTES SECTION
        self.new_note_btn = Button(container, text='Add Progress', anchor=W)

        self.progress_counter = len(self.progress_instance_list) + 1
        self.progress_count_label = Label(self.job_progress_frame, text=f"Progress Notes: {self.progress_counter - 1}",
                                      padx=5, pady=5)

        # list to store single data inputs (one-line)
        self.single_data_list = []
        # list to store foreign key inputs
        self.fk_data = []
        # list to store single data inputs needing larger input box
        self.large_box_data = []

        # Save Application Button
        self.save_new_application = Button(container, text="Save", command=self.save_data)

    def load_progress_window(self):

        # -----------------------------------------------------------------------------
        # Initial Window Configuration
        # retrieve job progress attributes as dict in form of:
        # {'single_data': [()], 'larger_box_data':[()], 'fk_data':[[()]]}
        self.progress_attributes = self.db_controller.retrieve_job_progress_column_names()

        # new window to open progress input
        self.progress_window = Toplevel()
        self.progress_window.geometry("500x450")
        self.progress_window.minsize(500, 450)
        self.progress_window.maxsize(500, 450)

        # disable main application window buttons whilst job progress is being created
        self.add_progress_btn.config(state='disabled')
        self.save_new_application.config(state='disabled')

        # re-enable buttons if progress window is closed
        # does not result in progress data being saved
        self.progress_window.protocol("WM_DELETE_WINDOW", self.enable_buttons_close_window)

        # -----------------------------------------------------------------------------
        # Initial Window Configuration
        label_row_count = 0
        input_row_count = 0

        # Add Progress Note count
        Label(self.progress_window, text=f"Progress Note: {self.progress_counter}", anchor=W
              ).grid(row=label_row_count, column=0, padx=5, pady=5, sticky=W+E)
        label_row_count += 1
        
        # --------------------------------------------------------------------------------
        # SINGLE ITEMS - SINGLE LINE
        # create single data labels and input boxes (one-line)
        for single_item in self.progress_attributes['single_data']:
            item_descr = Label(self.progress_window, text=single_item, anchor=W)
            
            item_input = Entry(self.progress_window, width=30, borderwidth=2, relief='solid')
            self.single_data_list.append(item_input)

            # add frame, label and input box to window
            item_descr.grid(row=label_row_count, column=0, sticky=W+E, padx=5, pady=5)
            label_row_count += 1
            item_input.grid(row=label_row_count, column=0, sticky=W+E, padx=(20,0), pady=5)
            label_row_count += 1

        # --------------------------------------------------------------------------------
        # FOREIGN TABLES - SELECTION INPUT FROM MENU
            
        for menu_option in self.progress_attributes['fk_data']:
            
            value_holder = MenuInput(menu_option[1][0][1]).get_input_val()
            menu_options = [val[1] for val in menu_option[1]]

            holding_frame = Frame(self.progress_window)
            holding_frame.grid(row=label_row_count, column=0, sticky=W+E)
            label_row_count += 1

            # Form: (Label, input_holder, OptionMenu)
            self.fk_data.append((Label(holding_frame, text=menu_option[0], anchor=W), 
                                     value_holder,
                                     OptionMenu(holding_frame, value_holder, *menu_options)))
            

            # load menu options to progress window
            for item in self.fk_data:
                # item[0] - Column Name, item[2] - Option Menu
                item[0].grid(row=0, column = 0, sticky=W+E, pady=10)
                item[2].grid(row=0, column = 1, pady=10)
        

        # --------------------------------------------------------------------------------
        # SINGLE ITEMS - MULTI LINE
        # create single item data labels and input boxes needing larger box
        for multi_line_item in self.progress_attributes['larger_box_data']:
            Label(self.progress_window, text=multi_line_item, anchor=W
                  ).grid(row=label_row_count, column=0, sticky=W+E, padx=5, pady=(10, 5))
            label_row_count += 1

            # Input, Frame, Input Box and ScrollBar
            input_frame = Frame(self.progress_window, padx=10)
            input_frame.grid(row=label_row_count, column=0, columnspan=2, padx=5, pady=5, sticky="NEWS")
            # allow mousewheel/trackpad to scroll text box
            input_frame.bind_all('<MouseWheel>', lambda e: text_box.yview_scroll(-1 * int(e.delta / 60), "units"))

            # add textbox for larger text input
            text_box = Text(input_frame, width=50, height=10, padx=10, pady=5, borderwidth=2, relief='solid')
            # create and configure text box - scrolls text box
            scrollbar = ttk.Scrollbar(self.progress_window, orient='vertical', command=text_box.yview)
            text_box.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=text_box.yview)
            scrollbar.grid(row=label_row_count, column=1, sticky="NSE")
            text_box.grid(row = 0, column=0, sticky=W)
            label_row_count += 1
            
            # add textbox to list to later retrieve input
            self.large_box_data.append(text_box)
            

        # add single item (multi-line) data inputs to progress screen
        for item in self.large_box_data:
            item.grid(row=input_row_count, column = 1, padx=5, pady=5)
            input_row_count += 1

        # ------------------------------------------------------------------
        # Save Progress Button
        self.save_progress_btn = Button(self.progress_window, text="Save Progress", anchor=E, command=self.retrieve_progress_data)
        self.save_progress_btn.grid(row=label_row_count, column=0, pady=10)
        


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
        self.enable_buttons_close_window()


    def enable_buttons_close_window(self):
        # re-enable main windows buttons if progress window is closed (without save)
        self.add_progress_btn.config(state='active')
        self.save_new_application.config(state='active')

        # clear lists
        self.single_data_list.clear()
        self.large_box_data.clear()
        self.fk_data.clear()

        self.progress_window.destroy()


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
        self.db_controller.write_job_progress(self.progress_instance_list, job_id)

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

        self.job_attributes_titles = self.db_controller.retrieve_job_data_configured(job_id)
        # print(self.job_attributes_titles)

        # Retrieve single data input labels and assigned value
        for data_tup in self.job_attributes_titles['single_data']:
            new_Entry = Entry(container, width = 50, borderwidth=1)
            new_Entry.insert(0, data_tup[1])
            self.single_data_inputs.append((Label(container, text=data_tup[0]), new_Entry))


        for menu_option in self.job_attributes_titles['menu_data']:
            
            value_holder = MenuInput(menu_option[2]).get_input_val()
            menu_options = [val[1] for val in menu_option[1]]

            # Form: (Label, input_holder, OptionMenu)
            self.menu_data_inputs.append((Label(container, text=menu_option[0]), 
                                     value_holder,
                                     OptionMenu(container, value_holder, *menu_options)))
            
        self.update_application_btn = Button(container, text="Save Changes", command=self.update_data)


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
        
    
    def load_window(self):
        self.left_minor_subscreen.clear_right_major()

        row_count = 0

        for single_tup in self.single_data_inputs[1:]:
            single_tup[0].grid(row=row_count, column = 0, padx=2, pady=2, sticky=W+E)
            single_tup[1].grid(row = row_count, column = 1 , sticky=W+E)
            row_count += 1
        
        for menu_tup in self.menu_data_inputs:
            menu_tup[0].grid(row=row_count, column = 0, padx=2, pady=2, sticky=W+E)
            menu_tup[2].grid(row = row_count, column = 1 , sticky=W)
            row_count += 1
        
        self.update_application_btn.grid(row=row_count, column=0, sticky=W+E)


# Delete an Application
class DeleteApplication(FullScreen):

    def __init__(self, container, db_controller) -> None:
        super().__init__(container)
        self.container = container
        self.db_controller = db_controller
        self.empty_label = Label(container)

        self.deletion_items = []

        # top-level buttons
        self.top_level_holder = Frame(container, borderwidth=2)
        self.clear_boxes_btn = Button(self.top_level_holder, text="Clear Boxes",anchor=E)
        self.delete_selected_btn = Button(self.top_level_holder, text = 'Delete Selected', anchor=E)

    def deselect_all(self):
        for item in self.deletion_items:
            item.uncheck_box()
        # disbaled clear box and delete all buttons
        self.clear_boxes_btn.config(state=DISABLED)
        self.delete_selected_btn.config(state=DISABLED)

    def delete_selected_jobs(self):

        id_list = [item.get_job_id() for item in self.deletion_items if item.checked.get() == 1]
        
        # create gramatically correct message
        if len(id_list) == 1:
            display_message = "Are you sure you want to delete this job?\nThis action cannot be undone"
        else:
            display_message = f"Are you sure you want to delete {len(id_list)} jobs?\nThis action cannot be undone"

        # Display Yes or No Box to confirm Deletion
        if(messagebox.askyesno('Permanent Deletion Warning!', 
                               message=display_message, default = 'no')):
            # delete all job progress notes associated with job_id
            self.db_controller.delete_job_progress_data(id_list)
            # delete job application data
            self.db_controller.delete_job_data(id_list)

            # reload window after deletion
            for screen in self.container.grid_slaves():
                screen.grid_forget()

            self.load_window()

    def delete_clear_box_disable(self):
        selected_box = False
        for item in self.deletion_items:
            if item.get_selection() == 1:
                selected_box = True
                break

        if selected_box == True and self.clear_boxes_btn.cget('state') == 'disabled' and self.delete_selected_btn.cget('state') == 'disabled':
            self.clear_boxes_btn.config(state=ACTIVE)
            self.delete_selected_btn.config(state=ACTIVE)

        elif selected_box == FALSE and self.clear_boxes_btn.cget('state') == 'active' and self.delete_selected_btn.cget('state') == 'active':
            self.clear_boxes_btn.config(state=DISABLED)
            self.delete_selected_btn.config(state=DISABLED)


    def load_window(self):
        
        # configure functions for clear_boxes and delete_selected
        self.clear_boxes_btn.config(command=self.deselect_all, state=DISABLED)
        self.delete_selected_btn.config(command=self.delete_selected_jobs, state = DISABLED)

        # ---------------------------------------------------------------
        # DATA RETRIEVAL
        # retrieve all application data - id and desired columns specified by database controller
        current_applications = self.db_controller.retrieve_job_display_cols()
        

        if len(current_applications) == 0:
            Label(self.container, text="No Job Applications").grid(row=0, column=0)
        
        else:
            # retrieve column titles
            self.column_titles = [name.title().replace("_", " ") for name in self.db_controller.retrieve_job_column_names()[1:len(current_applications[0])]]

            # ---------------------------------------------------------------
            # DELETION ITEM CLASS
            class DeletionItem():

                def __init__(self, container, job_data_tup, db_controller, reload_window_func, delete_clear_box_disable) -> None:
                    self.db_controller = db_controller
                    self.reload_window_func = reload_window_func
                    self.delete_clear_box_disable = delete_clear_box_disable
                    self.container = container

                    self.containing_box = Frame(container, bg='blue')

                    self.checked = IntVar()
                    self.checkBox = Checkbutton(self.containing_box, variable=self.checked, command=delete_clear_box_disable)
                    self.delete_job_btn = Button(container, text='Delete')

                    self.id = job_data_tup[0]
                    self.label_list = []

                    for job_entry in list(job_data_tup)[1:]:
                        self.label_list.append(Label(self.containing_box, text = job_entry, width=20, anchor=W))

                    
                def place_on_screen(self, row, column):

                    # configure individual deletion button command
                    self.delete_job_btn.config(command=self.delete_job)

                    self.containing_box.grid(row=row, column=0)
                    column_count = column
                    self.checkBox.grid(row=row, column=column_count, pady=2)
                    column_count += 1

                    for label in self.label_list:
                        label.grid(row=row_count, column=column_count, padx=5, pady=2)
                        column_count +=1

                    self.delete_job_btn.grid(row=row_count, column=column_count)

                def delete_job(self):
                    # Display Yes or No Box to confirm Deletion
                    if(messagebox.askyesno('Permanent Deletion Warning!', 
                               message="Are you sure you want to delete this job?\nThis action cannot be undone",
                               default = 'no')):
                        
                        # delete all job progress notes associated with job_id
                        self.db_controller.delete_job_progress_data([self.id])
                        # delete job application data
                        self.db_controller.delete_job_data([self.id])
                    # reload window after row deletion
                        for screen in self.container.grid_slaves():
                            screen.grid_forget()
                        self.reload_window_func()


                def get_job_id(self):
                    return self.id
                
                def get_selection(self):
                    return self.checked.get()
                
                def uncheck_box(self):
                    self.checked.set(0)

            # ---------------------------------------------------------------
            # ELEMENT PLACEMENT ON SCREEN

            # load top-level buttons
            self.top_level_holder.grid(row=0, column=0, pady=10)
            self.clear_boxes_btn.grid(row=0, column=0)
            self.delete_selected_btn.grid(row=0, column=1, padx=5)

            # Job Instance Placements
            row_count = 2
            
            # clear deletion items from potential previous screen load
            self.deletion_items.clear()
            for application in current_applications:
                item = DeletionItem(self.container, application, self.db_controller, self.load_window, self.delete_clear_box_disable)
                item.place_on_screen(row_count, 0)
                self.deletion_items.append(item)
                row_count+=1


    


        








        







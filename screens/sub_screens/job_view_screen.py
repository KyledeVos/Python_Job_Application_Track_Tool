from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date
from ..parent_screens import FullScreen
from .job_progress_instance import RecentJobProgress, AllJobProgress, ProgressInstanceWindow


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
                    # Change Page Main Title
                    self.left_sub_window.window_title.config(text="Job Application Details")
                    JobView(self.left_sub_window.get_right_major(), self.left_sub_window, self.db_controller, self.id).load_window()
                    # COMPULSORY - DO NOT REMOVE THIS OR CHANGE PLACEMENT IN CODE!
                    # Load of the new window requires manual generation of "Enter" event for cursor already present in window
                    # allowing trackpad to scroll immediately
                    self.left_sub_window.scrollable_screen.scrollable.master.event_generate("<Enter>", when="now")
                    self.left_sub_window.scrollable_screen.reset_scroll_window()

                def place_on_screen(self, row_count):
                    for col_count, job_instance in enumerate(self.job_data_values):
                        job_instance.grid(row = row_count, column=col_count, padx=10, pady=10)

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

                # Create Job Instance (with job data) and place on screen
                current_job = Job_Instance(count+1, application, self.container, self.left_sub_window, self.db_controller)
                current_job.place_on_screen(count+1)

# View Specific Job
class JobView(FullScreen):

    def __init__(self, container, left_minor_subscreen, db_controller, job_id) -> None:
        self.left_minor_subscreen = left_minor_subscreen
        self.container = container
        self.db_controller = db_controller
        self.job_id = job_id
        self.job_data = db_controller.retrieve_configured_job_data(job_id)
        self.data_converter = DataConverter()

        self.single_data_inputs = []
        self.large_box_inputs = []
        self.menu_data_inputs = []

        # retrieve job_application_data
        self.job_attributes_titles = self.db_controller.retrieve_configured_job_data(job_id)
        # retrieve most recent job progress data - function call below:
        # sets return_one to True and display_only to True
        self.recent_job_progress = self.db_controller.retrieve_job_progress_data(job_id, True, True)

        # ----------------------------------------------------------------------------
        # JOB BASIC INFO SECTION

        self.basic_title = Label(container, text="Job Information", anchor='w')
        self.basic_info_frame = Frame(container, bootstyle = 'default')

        # Retrieve single data input labels and assigned value
        for data_tup in self.job_attributes_titles['single_data']:
            
            # check for date field
            if 'date' in data_tup[0]:
                # seperate date attributes
                split_date = [int(val) for val in data_tup[1].split("/")]
                set_year = split_date[0]
                set_month = split_date[1]
                set_day = split_date[2]

                new_Entry = DateEntry(self.basic_info_frame, bootstyle='danger', startdate=date(set_year, set_month, set_day))

            else: 
                new_Entry = Entry(self.basic_info_frame, width = 50)
                new_Entry.insert(0, data_tup[1])
            self.single_data_inputs.append((Label(self.basic_info_frame, text=data_tup[0].title().replace("_", ""),
                                                   anchor='w'), new_Entry))

        # Retrieve large box data input labels and assigned value
        for data_tup in self.job_attributes_titles['large_box_data']:

            text_box = ScrolledText(self.basic_info_frame, width=80, height=10, wrap=WORD, autohide=True)
            text_box.insert(END, data_tup[1])

            # add event handles to disable/enable outer scroll bar when entering/leaving text box
            # allowing only text box scroll bar to function with mouse wheel
            text_box.bind("<Enter>", self.disable_outer_scroll, "+")
            text_box.bind("<Leave>", self.re_enable_outer_scroll, "+")

            self.large_box_inputs.append((Label(self.basic_info_frame, text=data_tup[0].title().replace("_", ""), anchor='w'),
                                           text_box))
        
        for menu_option in self.job_attributes_titles['menu_data']:
            
            menu_options = [val[1] for val in menu_option[1]]

            box = Combobox(self.basic_info_frame, bootstyle="success", values=menu_options)
            # find matching menu option to current set and retrieve index position
            for count, menu_tup in enumerate(menu_option[1]):
                if menu_option[2] == menu_tup[1]:
                    box.current(count)
                    break
           
            # Form: (Label, Combobox)
            self.menu_data_inputs.append((Label(self.basic_info_frame, text=menu_option[0], anchor='e'), box))
            
        self.update_application_btn = Button(self.basic_info_frame, text="Save Changes", command=self.update_basic_data)

        # ----------------------------------------------------------------------------
        # JOB PROGRESS SECTION - MOST RECENT PROGRESS
        self.progress_title = Label(container, text = "Job Progress Info", anchor='w')
        
        # Buttons
        self.top_btns_container = Frame(container)
        self.view_all_btn = Button(self.top_btns_container, text="View All", command=self.view_all_job_progress)
        self.add_progress_btn = Button(self.top_btns_container, text="Add Progress", command=self.add_job_progress)
        # check if current job has job progress data
        if self.recent_job_progress != None:
            # Create recent job progress instance
            self.recent_progress = RecentJobProgress(container, self.recent_job_progress, self.left_minor_subscreen.scrollable_screen.scrollable)
            # retrieve recent progress frame containing recent progress data
            self.recent_progress_section = self.recent_progress.retrieve_recent_progress_frame()

                    
        # ----------------------------------------------------------------------------
        # JOB GENERAL NOTES SECTION
            # LATER

    def disable_outer_scroll(self, event):
        self.left_minor_subscreen.scrollable_screen.scrollable.disable_scrolling()

    def re_enable_outer_scroll(self, event):
        self.left_minor_subscreen.scrollable_screen.scrollable.enable_scrolling()

    def add_job_progress(self):

        # retrieve job progress config data - categorized column names
        self.progress_attributes = self.db_controller.retrieve_job_progress_column_names()

        # retrieve names of all columns for job progress
        self.all_progress_cols = self.db_controller.retrieve_job_progress_data(self.job_id, False, False)['col_list']

        # hold list of progress data after save  
        self.progress_instance_list = []
        # list of buttons to be disabled/enabled during progress creation
        self.buttons_list = [self.view_all_btn, self.add_progress_btn]

        # list to store single data inputs (one-line)
        self.single_data_list = []
        # list to store foreign key inputs
        self.fk_data = []
        # list to store single data inputs needing larger input box
        self.large_box_data = []

        # new progress window screen
        self.progress_window = ProgressInstanceWindow(self.progress_attributes, self.all_progress_cols,
                                                      self.db_controller, self.single_data_list, None, 
                                                      self.large_box_data, self.fk_data, self.buttons_list, 
                                                      lambda: self.reload_window(False), 
                                                      self.retrieve_and_save_progress_data, None)
        
        # load progress window
        self.progress_window.configure_window_open()
        
    def retrieve_and_save_progress_data(self):
        # progress data retrieval order designed to match database format as:
        # single,line inputs, multil-line data-inputs (text boxes), foreign-tables menu inputs, 

        progress_instance = []

        # 1) First field set as date for progress instance by default
        progress_instance.append(self.single_data_list[0].entry.get())

        # 2) Retrieve remaining Single Items
        for item in self.single_data_list[1:]:
            progress_instance.append(item.get())

        # 2) Retrieve multi-line input data
        for item in self.large_box_data:
            progress_instance.append(item.get("1.0", END).strip())
                
        # 3) Retrieve Foreign-Key (Menu-Based Data)
        for menu_input in self.fk_data:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
        
            progress_instance.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.progress_attributes['fk_data']))

        # clear lists
        self.single_data_list.clear()
        self.large_box_data.clear()
        self.fk_data.clear()

        # save new job progress
        self.db_controller. write_job_progress([progress_instance], self.job_id)

        # reload windows 
        self.reload_window(True)

        # print message to user that progres instance has been added to list (not saved in db)
        Messagebox.show_info(message='Job Progress has been saved')

        # re-enable buttons to add progress_instance, save new application and close progress window
        self.progress_window.enable_buttons_close_window()

            
    def view_all_job_progress(self):

        # cover job view screen for view all job progress data
        self.cover_frame = Frame(self.container, bootstyle = 'default')
        self.cover_frame.grid_columnconfigure(1, weight=1)
        self.cover_frame.grid(row=0, rowspan=self.row_count, columnspan=2, column=0, sticky="NEWS")

        # move scroll window back to top of page
        self.left_minor_subscreen.scrollable_screen.reset_scroll_window()

        # change window title
        self.left_minor_subscreen.window_title.config(text="Job Progress Notes")

        # retrieve full job progress data for current job
        # setting "return_one" to False and "display_only" to False
        # "display_only" as False returns full fk data with complete row id's and column data
        # NOTE: implementation is designed to work with return_one set to False
        self.all_job_progress_data = self.db_controller.retrieve_job_progress_data(self.job_id, False, False)
        # print(self.all_job_progress_data)

        # BUTTON to return to job view screen - removes covering frame
        self.back_btn = Button(self.cover_frame, text= "<- Back to Application", command=self.back_to_applications)

        # clear boxes and delete selected job progress button
        self.top_level_holder = Frame(self.cover_frame, bootstyle = 'default')
        self.clear_boxes_btn = Button(self.top_level_holder, text="Clear Boxes", command=self.clear_all_boxes)
        self.delete_selected_btn = Button(self.top_level_holder, text = 'Delete Selected')
        
        # Initialize instance of view all job Progress
        self.all_job_progress_instance = AllJobProgress(self.cover_frame, self.db_controller, self.all_job_progress_data, 
                                                        self.clear_boxes_btn, self.delete_selected_btn, self.back_btn, self.job_id,
                                                        self.reload_window)
        # call for creation of frame housing all job_progress data
        self.all_job_progress_instance.view_all_job_progress_notes()

        # call for load of screen widgets, retrieving last set main row count
        main_row_count = self.load_all_progress_top_screen()

        # call for load of recent job progress section - column title and progress rows
        main_row_count = self.all_job_progress_instance.load_all_progress_window(main_row_count)


    def load_all_progress_top_screen(self):
        
        # load return to job view button
        main_row_count = 0
        self.back_btn.grid(row = main_row_count, column=0, padx=2, pady=5)
        main_row_count += 1

        # load top holder holding clear boxes and delete selected buttons
        self.top_level_holder.grid(row=main_row_count, column=1, padx=10, pady=10, sticky='e')
        main_row_count += 1
        self.clear_boxes_btn.grid(row=0, column=0)
        self.delete_selected_btn.grid(row=0, column=1, padx=5)

         # configure functions for clear_boxes and delete_selected as disabled on window load up
        self.clear_boxes_btn.config(command=self.clear_all_boxes, state=DISABLED)
        self.delete_selected_btn.config(state = DISABLED)

        # return incremented main row count for calling method placement of further widgets
        return main_row_count

    def back_to_applications(self):
        # remove covering frame holding all job progress info
        self.cover_frame.grid_forget()

        # reset page title for view all job applications
        self.left_minor_subscreen.window_title.config(text="Job Application Details")
        
        # recall job progress window load - needed for additional add of job progress to load
        # most recent progress
        self.load_window()

    def enable_deselect_and_delete_all(self):
        self.clear_boxes_btn.config(state=ACTIVE)
        self.delete_selected_btn.config(state=ACTIVE)

    def clear_all_boxes(self):
        # iterate through all job_progress rows to remove checks on checkboxes
        for progress_instance in self.all_job_progress_instance.progress_rows:
            progress_instance.checked.set(0)

        # disable clear boxes and selected deletion buttons
        self.clear_boxes_btn.config(state=DISABLED)
        self.delete_selected_btn.config(state=DISABLED)

    def load_window(self):

        # clear previous screen
        self.left_minor_subscreen.clear_right_major()

        self.row_count = 0

        # --- BASIC JOB INFO PLACEMENT  ---
        # place section title
        self.basic_title.grid(row=self.row_count, column=0, sticky="NEWS", padx=5, pady=5)
        self.row_count += 1
        self.basic_info_frame.grid(row=self.row_count, column=0, columnspan=2, sticky="NEWS", padx=5, pady=5)
        self.row_count += 1
        basic_row_count = 0
        
        # first value is always id field - do not place on screen
        for single_tup in self.single_data_inputs[1:]:
            # place label
            single_tup[0].grid(row=basic_row_count, column = 0, padx=5, pady=2, sticky=W+E)
            single_tup[1].grid(row = basic_row_count, column = 1 , sticky=W+E)
            basic_row_count += 1

        for large_tup in self.large_box_inputs:
            large_tup[0].grid(row = basic_row_count, column = 0, padx = 5, pady = 10, sticky=W+E)
            basic_row_count += 1
            large_tup[1].grid(row = basic_row_count, column = 0, columnspan = 2, padx = 5, pady = 2, sticky=W+E)
            basic_row_count += 1
        
        for menu_tup in self.menu_data_inputs:
            menu_tup[0].grid(row=basic_row_count, column = 0, padx=5, pady=5, sticky=W+E)
            menu_tup[1].grid(row = basic_row_count, column = 1, padx=5, pady=5, sticky=W)
            basic_row_count += 1
        
        self.update_application_btn.grid(row=basic_row_count, column=0, sticky=W+E, pady=5)
        basic_row_count += 1

        # # --- LATEST JOB PROGRESS INFO  ---  
        self.progress_title.grid(row=self.row_count, column=0, sticky="NEWS")
        self.row_count += 1
        # place top button container
        self.top_btns_container.grid(row=self.row_count, column=0, sticky="NEWS", padx=5, pady=5)
        self.row_count += 1
        # place job progress function buttons
        
        self.view_all_btn.grid(row=0, column=0, sticky="NEWS", padx=5, pady=5)
        self.add_progress_btn.grid(row=0, column=1, sticky="NEWS", padx=5, pady=5)

        if self.recent_job_progress is None:
            self.view_all_btn.config(state=DISABLED)

        if self.recent_job_progress != None:
            # Place Recent Job Progress Section
            self.row_count = self.recent_progress.place_progress_frame(self.row_count)

    def reload_window(self, reload_view_all = True):
        # reload window after any changes have been made

        # clear previous screen
        self.left_minor_subscreen.clear_right_major()
        
        # 1) Reload underlying job application screen to perform
        # possible update to most recent job progress instance
        self.recent_job_progress = self.db_controller.retrieve_job_progress_data(self.job_id, True, True)
        # if there is remaining job progress data, reload recent progress section
        if self.recent_job_progress is not None:
            self.recent_progress = RecentJobProgress(self.container, self.recent_job_progress, self.left_minor_subscreen.scrollable_screen.scrollable)
            self.recent_progress_section = self.recent_progress.retrieve_recent_progress_frame()
        
        # load window already handles checks for no job progress data
        self.load_window()

        # 2) Reload overlying view all job progress screen
        if self.recent_job_progress is not None and reload_view_all is True:
        # if reload_view_all is True:
            # reload overlying progress window only if there is still progress data
            self.view_all_job_progress()

    def update_basic_data(self):

        data_values = []
        column_names = self.db_controller.retrieve_job_column_names()

        for single_input in self.single_data_inputs:
            # check if input type was for date, if so retrieve date
            if 'date' in single_input[0].cget('text').lower():
                data_values.append(single_input[1].entry.get())
            else:
                data_values.append(single_input[1].get())

        for large_input in self.large_box_inputs:
            data_values.append(large_input[1].get("1.0", END))

        for menu_input in self.menu_data_inputs:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
            
            data_values.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.job_attributes_titles['menu_data']))

        data_values.append(self.job_id)
        data_values = tuple(data_values)

        self.db_controller.update_job_application(column_names, data_values)

        # Display Message to user that changes to application have been saved
        Messagebox.show_info(message='Changes have been saved')


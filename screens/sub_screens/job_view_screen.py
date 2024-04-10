from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date
from ..parent_screens import FullScreen
from .job_progress_instance import RecentJobProgress, AllJobProgress, ProgressInstanceWindow
from .job_notes import AllNotesView, NewJobNote


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

        # list storing possible orders
        self.results_order = ['recent', 'oldest']

        # variable to track selected main screen
        self.progress_application_order = StringVar()
        # set default order type as first in results_order
        self.progress_application_order.set(self.results_order[0])



    def load_sort_menu(self, selected_order):

        # clear old applications from screen
        for widget in self.container.grid_slaves():
            widget.grid_forget()
        
        # update track of ordering value
        self.progress_application_order.set(selected_order)
        # set menu text to current ordering selection
        self.order_box.config(text=selected_order)
        # reload job applications
        self.load_window()


    def load_window(self):

        # retrieve job_application_data
        current_applications = self.db_controller.retrieve_job_application_date_ordered(self.progress_application_order.get())

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

            # track row_count
            row_placement_count = 0

            # add combo box label
            ordering_label = Label(self.container, text="Sort By:")
            ordering_label.grid(row=row_placement_count, column=0, pady=5)

            # add MenuButton for sorting options
            self.order_box = Menubutton(self.container, style='primary', text=self.progress_application_order.get())
            self.menu = Menu(self.order_box)


            # set each ordering option as a radiobutton
            for menu_option in self.results_order:
                self.menu.add_radiobutton(label=menu_option, value=menu_option, variable=self.progress_application_order, 
                                          command=lambda: self.load_sort_menu(self.progress_application_order.get()))
                
            # allows association of menu containing radio buttons for screen to MenuButton Widget
            self.order_box['menu'] = self.menu

            # set display to current selected ordering method
            self.order_box.grid(row=row_placement_count, column=1, pady=5)
            row_placement_count += 1

            for count, application in enumerate(current_applications):
                # Add Column Titles
                if row_placement_count == 1:
                    for col_count, title in enumerate(self.column_titles):
                        # Set reduced width for row count
                        if col_count == 0:
                            current_label = Label(self.container, text=title, width=8, anchor=W)
                        else:
                        # Set longer width for other rows (company, position, etc.)
                            current_label = Label(self.container, text=title, width=20, anchor=W)
                        current_label.grid(row=row_placement_count, column=col_count, pady=2)
                row_placement_count += 1

                # Create Job Instance (with job data) and place on screen
                current_job = Job_Instance(count+1, application, self.container, self.left_sub_window, self.db_controller)
                current_job.place_on_screen(row_placement_count+1)

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

        # SORTING ORDER OF APPPLICATIONS
        # list storing possible orders
        self.results_order = ['recent', 'oldest']
        # variable to track selected ordering method
        self.progress_application_order = StringVar()
        # set default (first) order type as first in results_order
        self.progress_application_order.set(self.results_order[0])

        # check if current job has job progress data
        if self.recent_job_progress != None:
            # Create recent job progress instance
            self.recent_progress = RecentJobProgress(container, self.recent_job_progress, self.left_minor_subscreen.scrollable_screen.scrollable)
            # retrieve recent progress frame containing recent progress data
            self.recent_progress_section = self.recent_progress.retrieve_recent_progress_frame()

                    
        # ----------------------------------------------------------------------------
        # JOB GENERAL NOTES SECTION
        self.notes_title = Label(container, text = "To-Do Notes", anchor='w')
        
        # Buttons
        self.notes_top_btn_container = Frame(container)
        self.add_note_btn = Button(self.notes_top_btn_container, text="Add Note", command=self.add_job_note)
        self.view_all_notes_btn = Button(self.notes_top_btn_container, text="Notes Management", command=self.view_all_to_do_notes)

        # container housing to do notes (summarized)
        self.to_do_notes_container = Frame(container)

        # list of buttons to be disabled during view of job note window
        self.job_notes_button_disable_list = [self.update_application_btn, self.view_all_btn, self.add_progress_btn,
                                             self.add_note_btn, self.view_all_notes_btn]

        # Initialize AllNotesView instance
        self.all_notes_instance = AllNotesView(self.to_do_notes_container, self.db_controller, self.job_id, 
                                               self.job_notes_button_disable_list,
                                               lambda: self.reload_all_notes(), include_all=False,
                                                deletion_functionality= False, view_all_btn = self.view_all_notes_btn)
        self.all_notes_instance.retrieve_note_data(incomplete_only=True)


    def add_job_note(self):

        # retrieve all note data 
        self.note_all_data = self.db_controller.retrieve_all_job_note_data(self.job_id)

        # lists to store retrieved data
        self.add_note_single_list = []
        self.add_note_boolean_list = []
        self.add_note_large_box_list = []
        self.add_note_fk_data = []

        # list of buttons to be disabled during view of job note window
        job_notes_button_disable_list = [self.update_application_btn, self.view_all_btn, self.add_progress_btn,
                                             self.add_note_btn, self.view_all_notes_btn]
  
        self.new_note = NewJobNote(self.note_all_data["categorized_column_names"], self.note_all_data["all_column_names"], 
                              self.db_controller, self.add_note_single_list, self.add_note_boolean_list,
                                self.add_note_large_box_list, self.add_note_fk_data, job_notes_button_disable_list, 
                                lambda: self.reload_all_notes(), 
                                self.retrieve_to_do_data, None)
        self.new_note.configure_window_open()

    def retrieve_to_do_data(self):
        # progress data retrieval order designed to match database format as:
        # single,line inputs, multil-line data-inputs (text boxes), foreign-tables menu inputs, 

        # list to store current progress note data (appended to progress_instance_list at end)
        note_instance = []
        # 1) Current Date Field set by default as first field for note instance
        if self.add_note_single_list:
            note_instance.append(self.add_note_single_list[0].entry.get())

        # 2) Dealine Date Field set by default as second field for note instance
        if self.add_note_single_list:
            note_instance.append(self.add_note_single_list[1].entry.get())

        # 3) Retrieve remaining Single Items
        for item in self.add_note_single_list[2:]:
            note_instance.append(item.get())

        # 4) Retrieve Boolean Items Data
        for item in self.add_note_boolean_list:
            note_instance.append(item.get())

        # 5) Retrieve multi-line input data
        for item in self.add_note_large_box_list:
            note_instance.append(item.get("1.0", END).strip())
                
        # 6) Retrieve Foreign-Key (Menu-Based Data)
        if self.add_note_fk_data:
            for menu_input in self.add_note_fk_data:
                menu_title = menu_input[0].cget('text')
                selected_option = menu_input[1].get()
            
                note_instance.append(self.data_converter.return_id_from_name(selected_option, menu_title,
                                                    self.note_all_data['categorized_column_names']['fk_data']))

        # clear lists
        if self.add_note_single_list:
            self.add_note_single_list.clear()
        if self.add_note_boolean_list:
            self.add_note_boolean_list.clear()
        if self.add_note_large_box_list:
            self.add_note_large_box_list.clear()
        if self.add_note_fk_data:
            self.add_note_fk_data.clear()
        
        # write new job progress(s)
        self.db_controller.write_job_to_do_note(note_instance , self.job_id, False)

        # print message to user that new note instance has been added to list (not saved in db)
        Messagebox.show_info(message='Note has been Saved')

        # re-enable buttons to add note_instance and close progress window
        self.new_note.enable_buttons_close_window()

        self.all_notes_instance.retrieve_note_data()
        self.all_notes_instance.load_all_to_do_notes()

        
    # --------------------------------------------------------------------------------------


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
                                                      lambda: self.reload_window(reload_view_all=False), 
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
        self.reload_window(reload_view_all=True)

        # print message to user that progres instance has been added to list (not saved in db)
        Messagebox.show_info(message='Job Progress has been saved')

        # re-enable buttons to add progress_instance, save new application and close progress window
        self.progress_window.enable_buttons_close_window()


    def back_to_applications(self):
        # remove covering frame holding all job progress info
        self.cover_frame.grid_forget()

        # reset page title for view all job applications
        self.left_minor_subscreen.window_title.config(text="Job Application Details")

            
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
        self.all_job_progress_data = self.db_controller.retrieve_job_progress_data(self.job_id, 
                                                                                   return_one = False,
                                                                                   display_only = False,
                                                                                   order_by = self.progress_application_order.get())
        # print(self.all_job_progress_data)

        # BUTTON to return to job view screen - removes covering frame
        self.back_btn = Button(self.cover_frame, text= "<- Back to Application", command=self.back_to_applications)

        # sort order holder
        sort_container = Frame(self.cover_frame, bootstyle='default')
        # Sort Description label
        sort_label = Label(sort_container, text="Sort By:",anchor=W)
        # add MenuButton for sorting options
        order_box = Menubutton(sort_container, style='primary', text=self.progress_application_order.get())
        menu = Menu(self.order_box)

        # set each ordering option as a radiobutton
        for menu_option in self.results_order:
            self.menu.add_radiobutton(label=menu_option, value=menu_option, variable=self.progress_application_order, 
                                        command = lambda:self.reload_window(reload_view_all=True))
            
         # allows association of menu containing radio buttons for screen to MenuButton Widget
        order_box['menu'] = menu


        # clear boxes and delete selected job progress button
        self.top_level_holder = Frame(self.cover_frame, bootstyle = 'default')
        self.clear_boxes_btn = Button(self.top_level_holder, text="Clear Boxes", command=self.clear_all_boxes)
        self.delete_selected_btn = Button(self.top_level_holder, text = 'Delete Selected', bootstyle='danger')
        
        # Initialize instance of view all job Progress
        self.all_job_progress_instance = AllJobProgress(self.cover_frame, self.db_controller, self.all_job_progress_data, 
                                                        self.clear_boxes_btn, self.delete_selected_btn, self.back_btn, self.job_id,
                                                        lambda: self.reload_window(reload_view_all=True))
        # call for creation of frame housing all job_progress data
        self.all_job_progress_instance.view_all_job_progress_notes()

        # call for load of screen widgets, retrieving last set main row count
        main_row_count = self.load_over_lay_top(self.clear_boxes_btn, self.delete_selected_btn, 
                                                self.top_level_holder, sort_container, 
                                                sort_label, order_box)

        # call for load of recent job progress section - column title and progress rows
        main_row_count = self.all_job_progress_instance.load_all_progress_window(main_row_count)

    def load_over_lay_top(self, clear_box_btn, delete_selected_btn, container, 
                          order_container = None, order_label = None, order_box = None):
        
        # load return to job view button
        main_row_count = 0
        self.back_btn.grid(row = main_row_count, column=0, padx=2, pady=5)
        main_row_count += 1

        # load sorting order frame - housing label and sort menu (if supplied)
        if order_container:
            order_container.grid(row=main_row_count, column=0, padx=10, pady=10, sticky='W')
        if order_label:
            order_label.grid(row=0, column=0)
        if order_box:
            order_box.grid(row=0, column=1)

        # load top holder holding clear boxes and delete selected buttons
        # check for presence of sort feature - determines column placement of clear and deletion buttons
        if order_container:
            container.grid(row=main_row_count, column=1, padx=10, pady=10, sticky='e')
        else:
            container.grid(row=main_row_count, column=0, padx=10, pady=10, sticky='e')
        main_row_count += 1
        clear_box_btn.grid(row=0, column=0)
        delete_selected_btn.grid(row=0, column=1, padx=5)

        main_row_count += 1

         # configure functions for clear_boxes and delete_selected as disabled on window load up
        clear_box_btn.config(state=DISABLED)
        delete_selected_btn.config(state = DISABLED)

        # return incremented main row count for calling method placement of further widgets
        return main_row_count


    def view_all_to_do_notes(self):

        # cover job view screen for view of all job notes data
        self.cover_frame = Frame(self.container, bootstyle = 'default')
        self.cover_frame.grid_columnconfigure(1, weight=1)
        self.cover_frame.grid(row=0, rowspan=self.row_count, columnspan=2, column=0, sticky="NEWS")

        # move scroll window back to top of page
        self.left_minor_subscreen.scrollable_screen.reset_scroll_window()

        # change window title
        self.left_minor_subscreen.window_title.config(text="Job Notes")

        # BUTTON to return to job view screen - removes covering frame
        self.back_btn = Button(self.cover_frame, text= "<- Back to Application", command=self.back_to_applications)

        # clear boxes and delete selected job progress button
        self.top_level_holder = Frame(self.cover_frame, bootstyle = 'default')
        self.clear_notes_btn = Button(self.top_level_holder, text="Clear Boxes")
        self.delete_selected_notes_btn = Button(self.top_level_holder, text = 'Delete Selected', bootstyle='danger')

        # frame for job_info data
        self.job_info_frame = Frame(self.cover_frame, bootstyle='default')

        # Initialize instance of all notes view
        self.deletion_view_instance = AllNotesView(self.job_info_frame, self.db_controller, self.job_id, 
                                               self.job_notes_button_disable_list, 
                                               lambda: self.reload_all_notes(call_location="all_notes_view"),
                                                True, True, self.clear_notes_btn, self.delete_selected_notes_btn, 
                                                self.view_all_notes_btn)
    
        # call for load of screen widgets, retrieving last set main row count
        main_row_count = self.load_over_lay_top(self.clear_notes_btn, self.delete_selected_notes_btn, self.job_info_frame)

        self.deletion_view_instance.retrieve_note_data(incomplete_only=False, is_data_present=True)
        self.deletion_view_instance.load_all_to_do_notes(row_count=main_row_count)



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

        
        # # --- INCOMPLETE TO-DO NOTES ---  
        self.notes_title.grid(row=self.row_count, column=0, sticky="NEWS", padx=5, pady=5)
        self.row_count += 1

        # place notes top button container
        self.notes_top_btn_container.grid(row=self.row_count, column=0, sticky="NEWS", padx=5, pady=5)
        self.row_count += 1
        # place notes top function buttons
        self.add_note_btn.grid(row=0, column=0, sticky="NEWS", padx=5, pady=5)
        self.view_all_notes_btn.grid(row=0, column=1, sticky="NEWS", padx=5, pady=5)

        # place frame holding to_do_notes section
        self.to_do_notes_container.grid(row=self.row_count, column=0, sticky="NEWS")
        self.row_count += 1 

        # call for load of job to_do notes
        self.all_notes_instance.load_all_to_do_notes()
        
        
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

        # 2) Reload overlying view all job progress screen if progress screen is being used
        if self.recent_job_progress is not None and reload_view_all is True:
        # if reload_view_all is True:
            # reload overlying progress window only if there is still progress data
            self.view_all_job_progress()

        # 3) call for reload of job to_do notes data
        self.all_notes_instance.retrieve_note_data()
        self.all_notes_instance.load_all_to_do_notes()


    def reload_all_notes(self, call_location = ""):
        # reload window after any changes have been made

        # clear previous screen
        self.left_minor_subscreen.clear_right_major()

        # reload job view screen for any changes made to do_notes_data
        self.load_window()
        # call for reload of job to_do notes data

        self.all_notes_instance.retrieve_note_data()
        self.all_notes_instance.load_all_to_do_notes()
        
        # allows for reload of all_notes_view overlay screen when viewing from all_notes view screen
        if call_location == "all_notes_view":
            self.view_all_to_do_notes()



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


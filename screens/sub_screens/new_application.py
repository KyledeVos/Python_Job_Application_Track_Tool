from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date
from ..parent_screens import FullScreen
from .job_progress_instance import ProgressInstanceWindow, DataConverter
from .job_notes import NewJobNote

# New Job Application Sub-Screen
class NewApplicationScreen(FullScreen):

    def __init__(self, container, db_controller, left_sub_window):
        super().__init__(container)
        self.db_controller = db_controller
        self.left_sub_window = left_sub_window
        self.data_converter = DataConverter()
        self.container = container

        # create access to outer scroll screen needed to enable and disable outer scrolling during scroll of Textboxes
        self.scrollable = self.left_sub_window.scrollable_screen.scrollable

        self.row_count = 0

        # ---------------------------------------------------------------
        # JOB BASIC INFO
        self.single_data_inputs = []
        self.large_box_inputs = []
        self.menu_data_inputs = []

        self.job_attributes_titles = self.db_controller.retrieve_configured_job_data()

        for val_name in self.job_attributes_titles['single_data']:

            if 'date' in val_name:
               
                # retrieve current date to set as default
                current_date = [int(val) for val in str(date.today()).split("-")]
                current_year = current_date[0]
                current_month=current_date[1]
                current_day=current_date[2]

                # Create Calendar widget for date retrieval
                cal = DateEntry(container, bootstyle='danger', startdate=date(current_year, current_month, current_day))
                self.single_data_inputs.append((Label(container, text="Date:", anchor=W), cal))
            else:
                self.single_data_inputs.append((Label(container, text=val_name.title().replace("_", " "), anchor=W),
                                            Entry(container, width=50, bootstyle="dark")))
            
        # large box data
        for val_name in self.job_attributes_titles['large_box_data']:
            text_box = ScrolledText(self.container, width=80, height=10, wrap=WORD, autohide=True)
            text_box.bind("<Enter>", self.disable_outer_scroll, "+")
            text_box.bind("<Leave>", self.re_enable_outer_scroll, "+")
            self.large_box_inputs.append((Label(self.container, text=val_name.title().replace("_", " "), anchor=W),
                                            text_box))
            
        # Menu Data
        for menu_option in self.job_attributes_titles['menu_data']:
            
            menu_options = [val[1] for val in menu_option[1]]

            box = Combobox(container, bootstyle='success', values = menu_options)
            box.current(0)

            # Form: (Label, input_holder, OptionMenu)
            self.menu_data_inputs.append((Label(container, text=menu_option[0], anchor=W), 
                                     box))
        
        # -------------------------------------------------------------------
        # Lower buttons Text
        progress_text = "Add Progress Note"
        new_note_text = "Add To-Do Note"

        # determine max required width from above buttons, used to make all buttons the same width
        sub_button_width = max(len(progress_text), len(new_note_text)) + 2

        # list of buttons to be disabled/enabled during sub_window opening (progress and job note windows)
        self.buttons_list = []
        
        # ---------------------------------------------------------------
        # JOB PROGRESS TRACK SECTION
        
        # retrieve job progress config data
        self.progress_attributes = self.db_controller.retrieve_job_progress_column_names()

        # hold list of progress data after save  
        self.progress_instance_list = []

        self.job_progress_frame = Frame(container, bootstyle = 'default')
        
        self.add_progress_btn = Button(self.job_progress_frame, text=progress_text, 
                                       command=self.load_progress_window, width=sub_button_width)

        self.buttons_list.append(self.add_progress_btn)

        self.progress_counter = len(self.progress_instance_list)
        self.progress_count_label = Label(self.job_progress_frame, text=f"Progress Notes: {self.progress_counter}")

        # list to store single data inputs (one-line)
        self.single_data_list = []
        # list to store boolean data inputs
        self.boolean_datalist = []
        # list to store foreign key inputs
        self.fk_data = []
        # list to store single data inputs needing larger input box
        self.large_box_data = []

        # ---------------------------------------------------------------
        # JOB NOTES SECTION

        # retrieve column names for job notes window
        self.job_notes_fields = self.db_controller.retrieve_job_notes_column_names()

        # hold list of job note data after save  
        self.job_note_instance_list = []

        # lists to hold inputs recieved from new job note
        self.note_single_data = []
        self.note_boolean_data = []
        self.note_large_box_data = []
        self.note_fk_data = []
        
        # Main frame holding job notes section
        self.job_notes_main_frame = Frame(container, bootstyle='default')

        # frame housing top note buttons - 
        self.new_note_btn = Button(self.job_notes_main_frame, text=new_note_text,
                                   command=self.load_new_note_window, width= sub_button_width)
        
        # add button to list of buttons to disable during new note creation window
        self.buttons_list.append(self.new_note_btn)

        self.to_do_counter = len(self.progress_instance_list)
        self.to_do_counter_label = Label(self.job_notes_main_frame, text=f"To-Do Notes: {self.to_do_counter}")


        # ---------------------------------------------------------------
        # Save Application Button
        text = "Save New Application"
        self.save_new_application = Button(container, text=text, command=self.save_data, width=len(text) + 2)
        self.buttons_list.append(self.save_new_application)

    def disable_outer_scroll(self, event):
        self.scrollable.disable_scrolling()

    def re_enable_outer_scroll(self, event):
        self.scrollable.enable_scrolling()

    def load_progress_window(self):
        # initializes all widgets in progress window and populates single_data_list, large_box_data
        # and fk_data lists with values
        self.progress_window = ProgressInstanceWindow(self.progress_attributes, None, self.db_controller, self.single_data_list, None, 
                                                      self.large_box_data, self.fk_data, self.buttons_list, self.load_window,
                                                      self.retrieve_progress_data, None)  
        self.progress_window.configure_window_open()

    def load_new_note_window(self):
        # initializes all widgets in new_note_screen and populates single_data_list, large_box_data
        # and fk_data lists with values
        self.new_note_screen = NewJobNote(self.job_notes_fields, None, self.db_controller, self.note_single_data, 
                                          self.note_boolean_data, self.note_large_box_data, self.note_fk_data,
                                          self.buttons_list, self.load_window, self.retrieve_to_do_data, None)
        self.new_note_screen.configure_window_open()


    def retrieve_progress_data(self):
        # progress data retrieval order designed to match database format as:
        # single line inputs, boolean_data inputs, multil-line data-inputs (text boxes), foreign-tables menu inputs, 

        # list to store current progress note data (appended to progress_instance_list at end)
        self.progress_counter += 1
        # correct progress count label in main application
        self.progress_count_label.config(text=f"Progress Notes: {self.progress_counter}")
        self.progress_count_label.grid(row=0, column=1, padx=10, pady=2)
        self.row_count += 1

        progress_instance = []
        # 1) Date Field set by default as first field for progress instance
        progress_instance.append(self.single_data_list[0].entry.get())

        # 2) Retrieve remaining Single Items
        for item in self.single_data_list[1:]:
            progress_instance.append(item.get())

        # 3) Retrieve boolean Data Items
            for item in self.boolean_datalist:
                progress_instance.append(item.get())

        # 4) Retrieve multi-line input data
        for item in self.large_box_data:
            progress_instance.append(item.get("1.0", END).strip())
                
        # 5) Retrieve Foreign-Key (Menu-Based Data)
        for menu_input in self.fk_data:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
        
            progress_instance.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.progress_attributes['fk_data']))

        # Add Progress instance to list of instances
        # NOTE - current implementation still needs job_id retrieved only after save of new job application
        self.progress_instance_list.append(progress_instance)

        # clear lists
        if self.single_data_list:
            self.single_data_list.clear()
        if self.boolean_datalist:
            self.boolean_datalist.clear()
        if self.large_box_data:
            self.large_box_data.clear()
        if self.fk_data:
            self.fk_data.clear()

        # print message to user that progres instance has been added to list (not saved in db)
        Messagebox.show_info(message='Job Progress has been added on')

        # re-enable buttons to add progress_instance, save new application and close progress window
        self.progress_window.enable_buttons_close_window()

    def retrieve_to_do_data(self):
        # progress data retrieval order designed to match database format as:
        # single,line inputs, multil-line data-inputs (text boxes), foreign-tables menu inputs, 

        
        self.to_do_counter += 1
        # correct progress count label in main application
        self.to_do_counter_label.config(text=f"To-Do Notes: {self.to_do_counter}")
        self.to_do_counter_label.grid(row=0, column=1, padx=10, pady=2)
        self.row_count += 1

        # list to store current progress note data (appended to progress_instance_list at end)
        note_instance = []
        # 1) Current Date Field set by default as first field for note instance
        note_instance.append(self.note_single_data[0].entry.get())

        # 2) Dealine Date Field set by default as second field for note instance
        note_instance.append(self.note_single_data[1].entry.get())

        # 3) Retrieve remaining Single Items
        for item in self.note_single_data[2:]:
            note_instance.append(item.get())

        # 4) Retrieve Boolean Items Data
        for item in self.note_boolean_data:
            note_instance.append(item.get())

        # 5) Retrieve multi-line input data
        for item in self.note_large_box_data:
            note_instance.append(item.get("1.0", END).strip())
                
        # 6) Retrieve Foreign-Key (Menu-Based Data)
        if self.fk_data:
            for menu_input in self.fk_data:
                menu_title = menu_input[0].cget('text')
                selected_option = menu_input[1].get()
            
                note_instance.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.job_notes_fields['fk_data']))

        # Add Progress instance to list of instances
        # NOTE - current implementation still needs job_id retrieved only after save of new job application
        self.job_note_instance_list.append(note_instance)

        # clear lists
        if self.note_single_data:
            self.single_data_list.clear()
        if self.note_boolean_data:
            self.note_boolean_data.clear()
        if self.note_large_box_data:
            self.note_large_box_data.clear()
        if self.note_fk_data:
            self.note_fk_data.clear()

        # print message to user that new note instance has been added to list (not saved in db)
        Messagebox.show_info(message='Note has been added on')

        # re-enable buttons to add new note instance, save new application and close progress window
        self.new_note_screen.enable_buttons_close_window()


    def save_data(self):

        data_values = []

        for single_input in self.single_data_inputs[1:]:
            # check if input type was for date, if so retrieve date
            if 'date' in single_input[0].cget('text').lower():
                data_values.append(single_input[1].entry.get())
            else:
                data_values.append(single_input[1].get())

        for large_box_value in self.large_box_inputs:
            data_values.append(large_box_value[1].get("1.0", END))

        for menu_input in self.menu_data_inputs:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
            
            data_values.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.job_attributes_titles['menu_data']))
        
        # save new job application and retrieve id
        job_id = self.db_controller.write_single_job_no_id(data_values)
        # write new job progress(s)
        self.db_controller.write_job_progress(self.progress_instance_list , job_id)
        # write new job to_do note(s)
        self.db_controller.write_job_to_do_note(self.job_note_instance_list, job_id)

        # clear input fields after save
        for input_field in self.single_data_inputs:
            # check if input type was for date, if so ret
            if 'date' in input_field[0].cget('text').lower():
                # retrieve current date - default setting
                current_date = [str(val) for val in str(date.today()).split("-")]
                current_year = current_date[0]
                current_month=current_date[1]
                current_day=current_date[2]
                # reset current date
                input_field[1].entry.delete(0, END)
                input_field[1].entry.insert(0, current_year+"/"+current_month+"/"+current_day)
            else:
                # non-date field - clear input box
                input_field[1].delete(0, END)

        # clear combo--box fields
        for input_field in self.large_box_inputs:
            input_field[1].delete("1.0", END)

        # reset menu options to first option
        for menu_option in self.menu_data_inputs:
            menu_option[1].current(0)

        # Display Message to user that Application has been saved
        Messagebox.show_info(message='Application has been saved')

        # move screen back to top of scroll
        self.scrollable.yview_moveto(0.0)

        # clear progress instanc list after job application save
        self.progress_instance_list.clear()
        # reset progress counter
        self.progress_counter = 1
        self.progress_count_label.destroy()
        self.progress_count_label = Label(self.job_progress_frame, text=f"Progress Notes: {self.progress_counter - 1}")
        
        # reset to-do notes counter
        self.to_do_counter = 1
        self.to_do_counter_label.destroy()
        self.to_do_counter_label = Label(self.job_notes_main_frame, text=f"To-Do Notes: {self.to_do_counter}")


        self.load_window()


    def load_window(self):

        # load single data inputs
        for single_tup in self.single_data_inputs[1:]:
            
            # # check for date field
            # if 'date' in single_tup[0].cget('text').lower():   
            #     single_tup[0].grid(row=self.row_count, column = 0, padx=2, pady=10, sticky=W+E)
            #     self.row_count += 1
            # else:
            single_tup[0].grid(row=self.row_count, column = 0, padx=2, pady=10, sticky=W+E)
            
            single_tup[1].grid(row = self.row_count, column = 1 , sticky=W+E)
            self.row_count += 1

        # load large_box data inputs
        for large_box_item_tup in self.large_box_inputs:
            large_box_item_tup[0].grid(row = self.row_count, column = 0, padx = 5, pady = 10, sticky=W+E)
            self.row_count += 1
            large_box_item_tup[1].grid(row = self.row_count, column = 0, columnspan = 2, padx = 5, pady = 2, sticky=W+E)
            self.row_count += 1

        # load menu data inputs
        for menu_tup in self.menu_data_inputs:
            menu_tup[0].grid(row=self.row_count, column = 0, padx=2, pady=5, sticky=W+E)
            menu_tup[1].grid(row = self.row_count, column = 1 , sticky=W)
            self.row_count += 1

        # load job progress section (in main application)
        self.job_progress_frame.grid(row=self.row_count, column=0, columnspan=2, padx=2, pady=5, sticky=W+E)
        self.add_progress_btn.grid(row=0, column=0, padx=2, pady=5)
        if self.progress_counter > 1:
            self.progress_count_label.grid(row=0, column=1, padx=10, pady=2)
        self.row_count += 1

        # load new job note section
        self.job_notes_main_frame.grid(row=self.row_count, column=0, columnspan=2, padx=2, pady=5, sticky=W+E)
        self.row_count += 1

        # load add note button
        self.new_note_btn.grid(row=0, column=0, padx=2, pady=5)

        # ------------------------------------------------------------------------
        # BUTTONS
        self.save_new_application.grid(row=self.row_count, column=0, columnspan=2)
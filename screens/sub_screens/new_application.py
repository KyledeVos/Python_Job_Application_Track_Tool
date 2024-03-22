from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date
from ..parent_screens import FullScreen
from .job_progress_instance import ProgressInstanceWindow, DataConverter

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
        
        # ---------------------------------------------------------------
        # JOB PROGRESS TRACK SECTION
        
        # retrieve job progress config data
        self.progress_attributes = self.db_controller.retrieve_job_progress_column_names()

        # hold list of progress data after save  
        self.progress_instance_list = []
        # list of buttons to be disabled/enabled during progress creation
        self.buttons_list = []

        self.job_progress_frame = Frame(container, bootstyle = 'default')
        self.add_progress_btn = Button(self.job_progress_frame, text='Add Progress Note', command=self.load_progress_window)

        self.buttons_list.append(self.add_progress_btn)

        self.progress_counter = len(self.progress_instance_list) + 1
        self.progress_count_label = Label(self.job_progress_frame, text=f"Progress Notes: {self.progress_counter - 1}")

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
        self.new_note_btn = Button(container, text='Add Job Note')

        # ---------------------------------------------------------------
        # Save Application Button
        self.save_new_application = Button(container, text="Save New Application", command=self.save_data)
        self.buttons_list.append(self.save_new_application)

    def disable_outer_scroll(self, event):
        print('disable outer scroll')
        self.scrollable.disable_scrolling()

        

    def re_enable_outer_scroll(self, event):
        print("enable outer scroll")
        self.scrollable.enable_scrolling()

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

        # 1) Date Field set by default as first field for progress instance
        progress_instance.append(self.single_data_list[0].entry.get())

        # 2) Retrieve remaining Single Items
        for item in self.single_data_list[1:]:
            progress_instance.append(item.get())

        # 3) Retrieve multi-line input data
        for item in self.large_box_data:
            progress_instance.append(item.get("1.0", END).strip())
                
        # 4) Retrieve Foreign-Key (Menu-Based Data)
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
        Messagebox.show_info(message='Job Progress has been added on')

        # re-enable buttons to add progress_instance, save new application and close progress window
        self.progress_window.enable_buttons_close_window()


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
        self.db_controller.write_job_progress(self.progress_instance_list , job_id)

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

        for input_field in self.large_box_inputs:
            input_field[1].delete("1.0", END)

        # Display Message to user that Application has been saved
        Messagebox.show_info(message='Application has been saved')

        # clear progress instanc list after job application save
        self.progress_instance_list.clear()
        # reset progress counter
        self.progress_counter = 1
        self.progress_count_label.destroy()
        self.progress_count_label = Label(self.job_progress_frame, text=f"Progress Notes: {self.progress_counter - 1}")
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

        # ------------------------------------------------------------------------
        # BUTTONS
        self.save_new_application.grid(row=self.row_count, column=0, sticky=W+E)
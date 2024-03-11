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
        self.progress_window.maxsize(500, 700)

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
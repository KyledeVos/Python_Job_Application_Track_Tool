from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date
from .sub_window import SubWindowBasic

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


class RecentJobProgress():

    def __init__(self, outer_frame, recent_job_progress, outer_scrollable) -> None:
        self.outer_frame = outer_frame
        self.recent_job_progress = recent_job_progress
        # Instance of ScrollableScreen (from parent screens) to control enable/disable of outer scrollbar mouse wheel control
        # when scrolling in Recent Progress Text box(s)
        self.outer_scrollable = outer_scrollable

    def retrieve_recent_progress_frame(self):
            
        self.progress_data_frame = Frame(self.outer_frame, bootstyle="default")
        self.progress_data_frame.grid_columnconfigure(1, weight=1)

        # latest progress title
        self.latest_progress_title = Label(self.progress_data_frame, text="Latest Progress Note Review:", anchor='w')
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
                text_box = ScrolledText(self.progress_data_frame, width=80, height=10,wrap=WORD, autohide=True)
                text_box.insert(END, self.recent_job_progress['val_list'][count])

                # add event handler to disable outer scrollbar control from mousewheel when cursor enters textbox
                text_box.bind("<Enter>", self.disable_outer_scroll, "+")
                # add event handler to re-enable outer scrollbar control from mousewheel when cursor leaves textbox
                text_box.bind("<Leave>", self.re_enable_outer_scroll, "+")

                # recent job progress allows for read only - disable edit functionality for text boxes
                # text_box.configure(state=DISABLED)

                self.large_box_labels.append((Label(self.progress_data_frame, text=col.title().replace("_", " "), anchor='w'),
                                                text_box))
                
            # check if column name exists in fk table
            # NOTE: recent job progress does not allow for edits - fk data not set as ComboBox
            elif col in fk_table_cols:
                self.fk_data_labels.append(
                    (Label(self.progress_data_frame, text=col.title().replace("_", " "), anchor='e'), 
                        Label(self.progress_data_frame, text=self.recent_job_progress['val_list'][count],
                            anchor='w')))
                
            # column not in large text box data or fk data - single line data
            else:
                self.single_data_labels.append(
                    (Label(self.progress_data_frame, text=col.title().replace("_", " ") + ":", anchor='e'),
                        Label(self.progress_data_frame, text=self.recent_job_progress['val_list'][count], anchor='w')))

        # return progress frame containing recent job progress info
        return self.progress_data_frame
    
    def disable_outer_scroll(self, event):
        self.outer_scrollable.disable_scrolling()

    def re_enable_outer_scroll(self, event):
        self.outer_scrollable.enable_scrolling()
    
    def place_progress_frame(self, row_count):

        # place main container within outer container
        self.progress_data_frame.grid(row = row_count, column=0, columnspan=2, sticky="NEWS", padx=5, pady=5)
        row_count += 1

        progress_row_count = 0
        self.latest_progress_title.grid(row=progress_row_count, column=0, sticky=W+E)
        progress_row_count += 1

        # place single line data
        for single_line_label_tup in self.single_data_labels:
            single_line_label_tup[0].grid(row = progress_row_count, column = 0, padx = 5, sticky=W+E)
            single_line_label_tup[1].grid(row = progress_row_count, column = 1, padx = 5, sticky=W+E)
            progress_row_count += 1

        # place data from foreign key tables
        for fk_label_tup in self.fk_data_labels:
            fk_label_tup[0].grid(row = progress_row_count, column = 0, padx = 5, sticky=W+E)
            fk_label_tup[1].grid(row = progress_row_count, column = 1, padx = 5, sticky=W+E)
            progress_row_count += 1 

        # place data requiring a larger text box
        for large_box_item_tup in self.large_box_labels:
            large_box_item_tup[0].grid(row = progress_row_count, column = 0, padx = 5, pady = 10, sticky=W+E)
            progress_row_count += 1
            large_box_item_tup[1].grid(row = progress_row_count, column = 0, columnspan = 2, padx = 5, pady = 2, sticky=W+E)
            progress_row_count += 1

        return row_count


class ProgressInstanceWindow(SubWindowBasic):

    def __init__(self, progress_attributes, all_columns, db_controller, single_data_list, boolean_data_list,
                  large_box_data, fk_data, btns_list, outer_window_reload_func = None, 
                  retrieve_progress_data_func = None,  progress_instance = None) -> None:
        
        super().__init__("New Progress Note", progress_attributes, all_columns, db_controller, 
                         single_data_list, boolean_data_list, large_box_data, fk_data, btns_list, "Save Progress Note",
                           outer_window_reload_func, retrieve_progress_data_func, progress_instance)



    def save_progress_data(self):

        self.data_converter = DataConverter()
        self.progress_instance_data = []

        # 1) First field set as date for progress instance by default
        self.progress_instance_data.append(self.single_data_list[0].entry.get())

        # 1) Retrieve Single Items
        for item in self.single_data_list[1:]:
            self.progress_instance_data.append(item.get())

        # 2) Retrieve multi-line input data
        for item in self.large_box_data:
            self.progress_instance_data.append(item.get("1.0", END).strip())
                
        # 3) Retrieve Foreign-Key (Menu-Based Data)
        for menu_input in self.fk_data:
            menu_title = menu_input[0].cget('text')
            selected_option = menu_input[1].get()
        
            self.progress_instance_data.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.columns_categorized['fk_data']))

        # clear lists
        self.single_data_list.clear()
        self.large_box_data.clear()
        self.fk_data.clear()

        # add id to progress_instance
        self.progress_instance_data.append(self.progress_instance[0])

        column_names = self.db_controller.retrieve_job_progress_cols_exact()

        # save new job progress
        self.db_controller.update_job_progress(column_names[1:], self.progress_instance_data)

        # re-enable buttons to add progress_instance and close progress window
        self.enable_buttons_close_window()
        # reload windows - needed for reset of scrollbar
        self.outer_window_reload_func(True)

        # print message to user that progres instance has been added to list (not saved in db)
        Messagebox.show_info(message='Job Progress has been saved')


class JobInstanceQuickViewDeletion():
    # create instance of job progress showing single-line data fields and deletion button with
    # clickable feature to later enter update window for job progress updates
    
    def __init__(self, outer_container, full_data, progress_instance, quick_display_count, column_titles, column_info, db_controller,
                 progress_count,  clear_boxes_btn, delete_selected_btn, return_to_all_jobs_btn, deselect_btns_function,
                 outer_window_reload_func) -> None:

        self.outer_container = outer_container
        self.full_data = full_data
        self.progress_instance = progress_instance
        # slice full data to only use values in single line data list
        self.values_list = progress_instance[:quick_display_count]
        self.column_titles = column_titles
        self.column_info = column_info
        self.db_controller = db_controller
        self.progress_count = progress_count
        self.clear_boxes_btn = clear_boxes_btn
        self.delete_selected__btn = delete_selected_btn
        self.return_to_all_jobs_btn = return_to_all_jobs_btn
        self.deselect_btns_function = deselect_btns_function
        self.outer_window_reload_func = outer_window_reload_func

        # retrieve job progress config data
        self.progress_attributes = self.db_controller.retrieve_job_progress_column_names()
        
        self.id = None
        
        # checkbox allowing for selection and deletion of multiple job progress instances
        self.checked = IntVar()
        self.checkbox = Checkbutton(self.outer_container, variable=self.checked, command=self.deselect_btns_function)
        # list to labels of single line items for job progress identification
        self.single_vals = []
        # individual deletion button
        self.delete_btn = Button(self.outer_container, text = 'Delete', command=self.delete_single_progress)

        # add count of number of job progress instance
        self.progress_count = Label(self.outer_container, text = progress_count, anchor=CENTER)
        # allow click of button label to open new window for job progress update
        self.progress_count.bind("<Button-1>", self.progress_update)

        # populate id and single line data fields
        self.populate_values()

    def populate_values(self):

        # job progress id always first value in values list
        self.id = self.values_list[0]

        for val in self.values_list[1:]:
            label = Label(self.outer_container, text=val, width=15, anchor=CENTER)
            # allow click of single line labels to open window for job progress update
            label.bind("<Button-1>", self.progress_update)

            # correct width for shorter vs longer label content
            if len(val) <= 20:
                label.config(width=15)
            else:
                label.config(width=30)

            self.single_vals.append(label)
        
    def load_row(self, main_row_count, col_total):

        #track column placements
        col_count = 0
        
        # place CheckButton first
        self.checkbox.grid(row=main_row_count, column=col_count, padx=5, pady=5)
        col_count += 1

        # place count of current number of progress instances
        self.progress_count.grid(row=main_row_count, column=col_count, sticky=W+E, padx=5, pady=5)
        col_count += 1

        # place each single line field
        for attribute in self.single_vals:
            attribute.grid(row=main_row_count, column = col_count, sticky=W+E, padx=5, pady=5)
            col_count += 1

        # place individual row deletion button
        self.delete_btn.grid(row=main_row_count, column=col_count, padx=5, pady=5)

    def enable_clear_and_deleted_selected(self):
        # enable clear boxes and delete selected button if checkbox is checked
        self.clear_boxes_btn.config(state=ACTIVE)
        self.delete_selected__btn.config(state=ACTIVE)

    def delete_single_progress(self):

        # Change Colour of Job Instance text to highlight selected job

        self.progress_count.config(bootstyle='inverse-danger')

        for attribute in self.single_vals:
            attribute.configure(bootstyle='inverse-danger')

        # DISPLAY CONFIRMATION MESSAGE BEFORE DELETION
        if(Messagebox.yesno(title = "Permanent Deletion Warning!",
            message="Are you sure you want to delete this job?\nThis action cannot be undone") == "Yes"):
            # delete progress instance
            self.db_controller.delete_job_progress_only([self.id])
            # reload outer window after deletion of job_instance
            self.outer_window_reload_func()

        else:
            # Deletion cancelled, change font colour back to black and background to white
            self.progress_count.configure(bootstyle='default')

            for attribute in self.single_vals:
                attribute.configure(bootstyle='default')

    # Open new window for job progress update
    def progress_update(self, event):

        # list to store single data inputs (one-line)
        self.single_data_list = []
        # list to store foreign key inputs
        self.fk_data = []
        # list to store single data inputs needing larger input box
        self.large_box_data = []

        # list of buttons to be disabled during job progress view/ update
        self.buttons_list = [self.clear_boxes_btn, self.delete_selected__btn, self.return_to_all_jobs_btn]
        self.progress_window = ProgressInstanceWindow(self.progress_attributes, self.full_data['col_list'], self.db_controller, self.single_data_list, self.large_box_data,
                                                      self.fk_data, self.buttons_list, self.outer_window_reload_func, None, self.progress_instance)
        self.progress_window.configure_window_open()

class AllJobProgress():

    def __init__(self, outer_container, db_controller, all_job_progress_data,
                 clear_boxes_btn, delete_selected_btn, return_to_all_jobs_btn, job_id, outer_window_reload_func) -> None:
        self.outer_container = outer_container
        self.db_controller = db_controller
        self.all_job_progress_data = all_job_progress_data
        self.job_id = job_id
        self.outer_window_reload_func = outer_window_reload_func

        # buttons initialized in calling method
        self.clear_boxes_btn = clear_boxes_btn
        self.delete_selected_btn = delete_selected_btn
        self.return_to_all_jobs_btn = return_to_all_jobs_btn

        # configure delete_selected_button to delete selected job instances
        self.delete_selected_btn.config(command = self.delete_selected_progress)

        # create frame to hold column titles
        self.job_progress_frame = Frame(self.outer_container, borderwidth=2, relief='solid')
        # list to hold column names display
        self.display_columns = None


    def view_all_job_progress_notes(self):
        
        # ------------------- DISPLAY COLUMN TITLES ------------------------------------------------------
        # setup of display column names - only add single line data values (not text box or fk data)

        # add blank label for check_box column and number (count) column
        self.display_columns = [Label(self.job_progress_frame, text=''), Label(self.job_progress_frame, text='Number')]
        for column_name in self.all_job_progress_data['col_list']:
            col_found = False
            # remove id column
            if column_name == 'id':
                continue
            else:
                # check column name is not part of longer text box or comes from foreign key table
                for sub_columns in self.all_job_progress_data['column_info']:
                    if column_name in sub_columns[1]:
                        col_found = True
                        break
            
            if col_found == False:
                self.display_columns.append(Label(self.job_progress_frame, text=column_name.title().replace("_", " "), anchor=CENTER))
            col_found = False

        # list to hold each progress instance row
        self.progress_rows = []
        # iterate through progress values data to create individual rows of progress data
        quick_display_count = (len(self.display_columns) - 1)
        for count, progress_instance in enumerate(self.all_job_progress_data['val_list']):
            # only provide id and single line data fields to instance
            self.progress_rows.append(JobInstanceQuickViewDeletion(self.job_progress_frame, self.all_job_progress_data, progress_instance,  
                                                                   quick_display_count, self.all_job_progress_data['col_list'],
                                                                   self.all_job_progress_data['column_info'],self.db_controller, count,
                                                                   self.clear_boxes_btn, self.delete_selected_btn, self.return_to_all_jobs_btn,
                                                                   self.check_box_full_deselection, self.outer_window_reload_func))


    def load_all_progress_window(self, main_row_count):
        
        # --------- Load Column Titles -------------
        # place containing frame
        self.job_progress_frame.grid(row=main_row_count, column=0, columnspan=4, padx=5, sticky=W+E)
        main_row_count += 1

        job_instance_row = 0
        column_count = 0
        for display_col in self.display_columns:
            display_col.grid(row=job_instance_row, column=column_count, padx=5, pady=5, sticky=W+E)
            column_count += 1
        job_instance_row += 1

        # --------- Load Progress Rows -------------
        for progress_row in self.progress_rows:
            progress_row.load_row(main_row_count, len(self.display_columns) + 1)
            main_row_count += 1

        # return incremented main row count to calling method for possible additional
        # frame/widget placement
        return main_row_count
    
    def check_box_full_deselection(self):
        # during ticking of check box, check if all progress instances have been deselected,
        # if so, disable clear_boxes_btn and delete_selected_btn
        instance_selected = False

        # check if any progress instance row has been selected
        for progress_instance in self.progress_rows:
            if progress_instance.checked.get() == 1:
                instance_selected = True
                break
        
        # if all progress instance checkboxes are deselected, disable buttons
        if instance_selected == False:
            self.clear_boxes_btn.config(state=DISABLED)
            self.delete_selected_btn.config(state=DISABLED)
        else:
            self.clear_boxes_btn.config(state=ACTIVE)
            self.delete_selected_btn.config(state=ACTIVE)


    def delete_selected_progress(self):
        # delete all selected job progress instances

        # retrieve id's of selected job instances for deletion and change text and 
        # background colour to highlight selected jobs
        id_list = []

        for val in self.progress_rows:
            if val.checked.get() == 1:
                # add id num to id__list
                id_list.append(val.id)
                # change progress count colour to red (deletion warning)
                val.progress_count.configure(bootstyle = "inverse-danger")

                for attribute in val.single_vals:
                    # change label colour to red (deletion warning)
                    attribute.configure(bootstyle = "inverse-danger")

         # create gramatically correct message for Deletion Warning
        if len(id_list) == 1:
            display_message = "Are you sure you want to delete this job?\nThis action cannot be undone"
        else:
            display_message = f"Are you sure you want to delete {len(id_list)} jobs?\nThis action cannot be undone"

        # Display Yes or No Box to confirm Deletion
        if Messagebox.yesno(title = 'Permanent Deletion Warning!', message=display_message) == "Yes":

            # call for progress instances deletion
            self.db_controller.delete_job_progress_only(id_list)
            # call for job view window and job progress view all windows reload
            self.outer_window_reload_func()

        else:
            # Deletion Cancelled, change colours back to original
            for val in self.progress_rows:
                if val.checked.get() == 1:
                    # add id num to id__list
                    id_list.append(val.id)
                    # Deletion cancelled, change count colour back to normal
                    val.progress_count.configure(bootstyle = "default")

                    for attribute in val.single_vals:
                        # Deletion cancelled, change label colour back to normal
                        attribute.configure(bootstyle = "default")


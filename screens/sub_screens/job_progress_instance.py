from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class RecentJobProgress():

    def __init__(self, outer_frame, recent_job_progress) -> None:
        self.outer_frame = outer_frame
        self.recent_job_progress = recent_job_progress

    def retrieve_recent_progress_frame(self):
            
        self.progress_data_frame = Frame(self.outer_frame, padx=5, pady=5, borderwidth=2, relief='solid')
        self.progress_data_frame.grid_columnconfigure(1, weight=1)

        # latest progress title
        self.latest_progress_title = Label(self.progress_data_frame, text="Latest Progress Note:", anchor='w')
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

                text_box = Text(large_box_frame, width=40, height=10, padx=10, pady=5, 
                                borderwidth=2, relief='solid')
                text_box.grid(row =0, column=0, sticky='w')
                text_box.insert("1.0", self.recent_job_progress['val_list'][count])
                # recent job progress allows for read only - disable edit functionality for text boxes
                text_box.config(state=DISABLED)

                # create and configure text box - scrolls text box
                scrollbar = ttk.Scrollbar(self.progress_data_frame, orient='vertical', command=text_box.yview)
                text_box.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=text_box.yview)
                # allow for scrolling when entering textbox
                large_box_frame.bind('<Enter>', lambda e: text_box.yview_scroll(-1 * int(e.delta / 60), "units"))
                # allow scrolling with the use of trackpad/ mouse scrollwheel
                large_box_frame.bind_all('<MouseWheel>',lambda e: text_box.yview_scroll(-1 * int(e.delta / 60), "units"))
                # add current text box to list of text boxes
                self.large_box_labels.append((Label(self.progress_data_frame, text=col.title().replace("_", " "), anchor='w'),
                                                large_box_frame, scrollbar))
                
            # check if column name exists in fk table
            # NOTE: recent job progress does not allow for edits - fk data not set as MenuOption
            elif col in fk_table_cols:
                self.fk_data_labels.append(
                    (Label(self.progress_data_frame, text=col.title().replace("_", " "), anchor='e'), 
                        Label(self.progress_data_frame, text=self.recent_job_progress['val_list'][count],
                            padx=10, pady=5, anchor='w')))
                
            # column not in large text box data or fk data - single line data
            else:
                self.single_data_labels.append(
                    (Label(self.progress_data_frame, text=col.title().replace("_", " ") + ":", anchor='e'),
                        Label(self.progress_data_frame, text=self.recent_job_progress['val_list'][count], padx=10, pady=5, anchor='w')))

        # return progress frame containing recent job progress info
        return self.progress_data_frame
    
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
            large_box_item_tup[2].grid(row = progress_row_count, column = 1, sticky="NSE")
            progress_row_count += 1

        return row_count
    

class JobInstanceQuickViewDeletion():
    # create instance of job progress showing single-line data fields and deletion button with
    # clickable feature to later enter update window for job progress updates
    
    def __init__(self, outer_container, values_list, db_controller,
                 progress_count, clear_boxes_btn, delete_selected_btn, deselect_btns_function,
                 outer_window_reload_func) -> None:

        self.outer_container = outer_container
        self.values_list = values_list
        self.db_controller = db_controller
        self.progress_count = progress_count
        self.clear_boxes_btn = clear_boxes_btn
        self.delete_selected__btn = delete_selected_btn
        self.deselect_btns_function = deselect_btns_function
        self.outer_window_reload_func = outer_window_reload_func
        
        self.id = None
        
        # checkbox allowing for selection and deletion of multiple job progress instances
        self.checked = IntVar()
        self.checkbox = Checkbutton(self.outer_container, variable=self.checked, command=self.deselect_btns_function)
        # list to labels of single line items for job progress identification
        self.single_vals = []
        # individual deletion button
        self.delete_btn = Button(self.outer_container, text = 'Delete', anchor='e', command=self.delete_single_progress)

        # add count of number of job progress instance
        self.progress_count = Label(self.outer_container, text = progress_count, anchor=CENTER)

        # populate id and single line data fields
        self.populate_values()

    def populate_values(self):

        # job progress id always first value in values list
        self.id = self.values_list[0]

        for val in self.values_list[1:]:
            if len(val) <= 20:
                self.single_vals.append(Label(self.outer_container, text=val, width=15, anchor=CENTER))
            else:
                self.single_vals.append(Label(self.outer_container, text=val, width=30, anchor=CENTER))
        
    def load_row(self, main_row_count, col_total):

        #track column placements
        col_count = 0
        
        # place CheckButton first
        self.checkbox.grid(row=main_row_count, column=col_count, padx=5, pady=2)
        col_count += 1

        # place count of current number of progress instances
        self.progress_count.grid(row=main_row_count, column=col_count, sticky=W+E, padx=5, pady=2)
        col_count += 1

        # place each single line field
        for attribute in self.single_vals:
            attribute.grid(row=main_row_count, column = col_count, sticky=W+E, padx=5, pady=2)
            col_count += 1

        # place individual row deletion button
        self.delete_btn.grid(row=main_row_count, column=col_count, padx=5, pady=2)

    def enable_clear_and_deleted_selected(self):
        # enable clear boxes and delete selected button if checkbox is checked
        self.clear_boxes_btn.config(state=ACTIVE)
        self.delete_selected__btn.config(state=ACTIVE)

    def delete_single_progress(self):
        # delete progress instance
        self.db_controller.delete_job_progress_only([self.id])
        # reload outer window after deletion of job_instance
        self.outer_window_reload_func()


class AllJobProgress():

    def __init__(self, outer_container, db_controller, all_job_progress_data,
                 clear_boxes_btn, delete_selected_btn, job_id, outer_window_reload_func) -> None:
        self.outer_container = outer_container
        self.db_controller = db_controller
        self.all_job_progress_data = all_job_progress_data
        self.job_id = job_id
        self.outer_window_reload_func = outer_window_reload_func

        # buttons initialized in calling method
        self.clear_boxes_btn = clear_boxes_btn
        self.delete_selected_btn = delete_selected_btn

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
        for count, progress_instance in enumerate(self.all_job_progress_data['val_list']):
            # only provide id and single line data fields to instance
            self.progress_rows.append(JobInstanceQuickViewDeletion(self.job_progress_frame, 
                                                                   progress_instance[:len(self.display_columns) - 1], 
                                                                   self.db_controller, count,
                                                                   self.clear_boxes_btn, self.delete_selected_btn, 
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

        # retrieve id's of selected job instances for deletion
        id_list = [val.id for val in self.progress_rows if val.checked.get() ==  1]
        # call for progress instances deletion
        self.db_controller.delete_job_progress_only(id_list)
        # call for job view window and job progress view all windows reload
        self.outer_window_reload_func()


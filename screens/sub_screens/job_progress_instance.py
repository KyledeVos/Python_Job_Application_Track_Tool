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


class AllJobProgress():

    def __init__(self, outer_container, all_job_progress_data, clear_boxes_btn, delete_selected_btn) -> None:
        self.outer_container = outer_container
        self.all_job_progress_data = all_job_progress_data

        # buttons initialized in calling method
        self.clear_boxes_btn = clear_boxes_btn
        self.delete_selected_btn = delete_selected_btn

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
                self.display_columns.append(Label(self.job_progress_frame, text=column_name.title().replace("_", " "), anchor='w'))
            col_found = False

    def load_all_progress_window(self, main_row_count):

        # --------- Load Column Titles

        # place containing frame
        self.job_progress_frame.grid(row=main_row_count, column=0, columnspan=4, padx=5, sticky=W+E)
        main_row_count += 1

        job_instance_row = 0
        column_count = 0
        for display_col in self.display_columns:
            display_col.grid(row=job_instance_row, column=column_count, padx=5, pady=5, sticky=W+E)
            column_count += 1
        job_instance_row += 1

        # return incremented main row count to calling method for possible additional
        # frame/widget placement
        return main_row_count

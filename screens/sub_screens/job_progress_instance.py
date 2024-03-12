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
                text_box.config(state=DISABLED)

                # create and configure text box - scrolls text box
                scrollbar = ttk.Scrollbar(self.progress_data_frame, orient='vertical', command=text_box.yview)
                text_box.config(yscrollcommand=scrollbar.set)
                scrollbar.config(command=text_box.yview)
                large_box_frame.bind('<Enter>', lambda e: text_box.yview_scroll(-1 * int(e.delta / 60), "units"))
                large_box_frame.bind_all('<MouseWheel>',lambda e: text_box.yview_scroll(-1 * int(e.delta / 60), "units"))
                
                

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

        return self.progress_data_frame
    
    def place_progress_frame(self, row_count):

        # place main container within outer container
        self.progress_data_frame.grid(row = row_count, column=0, columnspan=2, sticky="NEWS", padx=5, pady=5)
        row_count += 1

        progress_row_count = 0
        self.latest_progress_title.grid(row=progress_row_count, column=0, sticky=W+E)
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

        return row_count

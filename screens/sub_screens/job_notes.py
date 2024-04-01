from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date
from .sub_window import SubWindowBasic
import copy

class NewJobNote(SubWindowBasic):

    def __init__(self, columns_categorized, all_columns, db_controller, single_data_list,
                 boolean_data_list, large_box_data, fk_data, btns_list, outer_window_reload_func = None, 
                 retrieve_note_data_func = None, current_instance = None,  ) -> None:
        
        # Creating new To_Do Note
        if retrieve_note_data_func is not None:
            super().__init__("New Note", columns_categorized, all_columns, db_controller, 
                             single_data_list, boolean_data_list, large_box_data, fk_data,
                             btns_list, "Save Note", outer_window_reload_func,
                             retrieve_note_data_func, current_instance)
        
        # Updating/Viewing existing Note
        else:
            super().__init__("Viewing Note", columns_categorized, all_columns, db_controller, 
                    single_data_list, boolean_data_list, large_box_data, fk_data,
                    btns_list, "Update Note", outer_window_reload_func,
                    self.save_note_data, current_instance)

    def save_note_data():
        print("save note data")

# --------------------------------------------------------------------------------------
class AllNotesView():

    def __init__(self, outer_container, db_controller, job_id, outer_buttons_list, 
                 outer_window_reload_func, include_all = True) -> None:

        self.outer_container = outer_container
        self.db_controller = db_controller
        self.job_id = job_id
        self.outer_buttons_list = outer_buttons_list
        self.outer_window_reload_func = outer_window_reload_func
        self.include_all = include_all

        self.notes_all_data = None

        self.incomplete_notes_present = None
        

    def retrieve_note_data(self):
        
        # update state of incomplete notes present
        self.incomplete_notes_present = self.db_controller.is_incomplete_notes(self.job_id)

        # Attempt Retrieval of all job to_do notes data -> None indicates no present job notes data
        self.notes_all_data = self.db_controller.retrieve_all_job_note_data(self.job_id)
        print(self.notes_all_data)

    def load_all_to_do_notes(self, incomplete_only = True):

        if self.notes_all_data is None:
            # No present note data, display message
            Label(self.outer_container, text="No To-Do Items").grid(row=0, column=0, padx=5, pady=5, sticky=W+E)

        # if only incomplete notes display is desired, check if there were incomplete notes present
        elif incomplete_only and self.incomplete_notes_present is False:
                Label(self.outer_container, text="No To-Do Items").grid(row=0, column=0, padx=5, pady=5, sticky=W+E)

        # 
        else:

            class JobRow():
                """Inner Class housing row labels and controls load of labels to window. Configures click event handle
                    for label to load job note view window for update of note"""

                def __init__(self, job_note_id, job_note_labels, note_row_placement, 
                             categorized_columns, all_columns, db_controller, outer_buttons_list, 
                             outer_window_reload_func, retrieve_data_func, set_data):
                    self.job_note_id = job_note_id
                    self.job_note_lables = job_note_labels
                    self.note_row_placement = note_row_placement
                    self.column_placement = 0

                    # data for note view window
                    self.categorized_columns = categorized_columns
                    self.all_columns = all_columns
                    self.db_controller = db_controller

                    # lists to hold inputs recieved from new job note
                    self.note_single_data = []
                    self.note_boolean_data = []
                    self.note_large_box_data = []
                    self.note_fk_data = []

                    # list of buttons to be disabled when job view window is open
                    self.outer_buttons_list = outer_buttons_list

                    # function to reload calling window
                    self.outer_window_reload_func = outer_window_reload_func
                    self.retrieve_data_func = retrieve_data_func

                    # current values for job note
                    self.set_data = set_data

                def load_row(self):
                    for label in self.job_note_lables:
                        label.grid(row = self.note_row_placement, column = self.column_placement, padx=5, pady=5, sticky=W+E)
                        label.bind("<Button-1>", lambda e: self.open_job_view_window(e))
                        self.column_placement += 1

                def open_job_view_window(self, event):
                    print(self.job_note_id)

                    job_note_view = NewJobNote(self.categorized_columns, self.all_columns, self.db_controller,
                                               self.note_single_data, self.note_boolean_data, self.note_large_box_data,
                                                self.note_fk_data, self.outer_buttons_list, self.outer_window_reload_func,
                                                  None,  self.set_data)
                    job_note_view.configure_window_open()

                #         def __init__(self, columns_categorized, all_columns, db_controller, single_data_list,
                #  boolean_data_list, large_box_data, fk_data, btns_list, outer_window_reload_func = None, 
                #  retrieve_note_data_func = None, current_instance = None,  ) -> None:


            # retrieve single data columns for summary display of note data
            self.single_data_cols = [val.lower().replace("_", "_") for val in self.notes_all_data['categorized_column_names']['single_data']]

            # track placement of rows
            notes_row_placement = 0
            # track column placements for each rows
            column_placement = 0

            # ----------- COLUMN TITLES ----------- 
            # Add additional column for count of number of to_do notes
            Label(self.outer_container, text="Number").grid(row=notes_row_placement, column = column_placement, padx=5, pady=5, sticky=W+E)
            column_placement += 1

            # load top row showing column names
            for name in self.single_data_cols:
                title_label = Label(self.outer_container, text=name.title().replace("_", " "))
                title_label.grid(row = notes_row_placement, column= column_placement, padx=5, pady=5, sticky=W+E)
                column_placement += 1

            # add additional column for status
            Label(self.outer_container, text="Status").grid(row=notes_row_placement, column = column_placement, padx=5, pady=5, sticky=W+E)
            column_placement += 1

            # reset column placement for next row
            column_placement = 0
            # increment row placement for next row
            notes_row_placement += 1

            # ----------- VALUES -----------

            # Job Note general view only displays single and boolean data view as summary of job note

            # retrieve index positions if single data columns (needed to retrieve values matching index position)
            single_data_col_indices = []
            for single_data_name in self.notes_all_data['categorized_column_names']['single_data']:
                single_data_col_indices.append(self.notes_all_data['all_column_names'].index(single_data_name.lower().replace(" ", "_")))

            # retrieve index positions of boolean data columns
            boolean_col_indices = []
            for boolean_name in self.notes_all_data['categorized_column_names']['boolean_data']:
                boolean_col_indices.append(self.notes_all_data['all_column_names'].index(boolean_name.lower().replace(" ", "_")))

            for count, job_note_instance in enumerate(self.notes_all_data['note_values']):

                # Perform check for incomplete to-do note
                # NOTE: Current implementation has set 'status' within the boolean_col_indices list used
                # to check for completion of to-do note item
                status_index = self.notes_all_data['all_column_names'].index('status')
                if job_note_instance[status_index] == 1 and incomplete_only == True:
                    continue


                current_note = []
                # Add row count column value
                current_label = Label(self.outer_container, text=str(count + 1))
                current_note.append(current_label)

                # add single data item values first
                for data_index in single_data_col_indices:
                    current_label = Label(self.outer_container, text=job_note_instance[data_index])
                    current_note.append(current_label)


                # add boolean data items
                for data_index in boolean_col_indices:

                    # correct data label for status column - ONLY show incomplete tasks in summary
                    # NOTE: Correction of other boolean fields needs to be made here
                    if job_note_instance[data_index] == 0:
                        display_text = "Incomplete"
                    else: 
                        display_text = "Completed"

                    current_label = Label(self.outer_container, text=display_text)
                    current_note.append(current_label)

                # Create job roww instance to uniquely track if of current job note
                # needed to load job note detailed view window, and call for placement of row labels 
                JobRow(job_note_instance[0], current_note, notes_row_placement, 
                       self.notes_all_data['categorized_column_names'], self.notes_all_data['all_column_names'], 
                       self.db_controller, self.outer_buttons_list, self.outer_window_reload_func, None, job_note_instance).load_row()
                notes_row_placement += 1


                # # clear current note list for next job note instance
                current_note.clear()





                            

                    



    def toggle_view_all(self):
        # switch between view all notes and view only incomplete notes
        self.include_all = not self.include_all


from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date
from .sub_window import SubWindowBasic

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

    def __init__(self, outer_container, db_controller, job_id, include_all = True ) -> None:

        self.outer_container = outer_container
        self.db_controller = db_controller
        self.job_id = job_id
        
        # retrieve all job to_do notes data for current job application
        # all_notes_summary form as {'columns' : [column names], 
        #                           'values': [(values for note 1), (values for note 2)}

        self.all_notes_summary_data = self.db_controller.retrieve_to_do_note_summary_data(job_id, include_all)


    def load_all_to_do_notes(self):

        # track placement of rows
        notes_row_placement = 0
        # track column placements for each row
        column_placement = 0

        # Check for present To-Do Notes data
        if len(self.all_notes_summary_data['values']) == 0:

            # NO DATA - PRINT MESSAGE
            Label(self.outer_container, text="No To-Do Notes").grid(row=notes_row_placement, column = column_placement, padx=5, pady=5, sticky=W+E)
        
        else:
          # DATA FOUND - DISPLAY DATA

            # Add additional column for count of number of to_do notes
            Label(self.outer_container, text="Number").grid(row=notes_row_placement, column = column_placement, padx=5, pady=5, sticky=W+E)
            column_placement += 1

            # load top row showing column names
            for name in self.all_notes_summary_data['columns']:
                title_label = Label(self.outer_container, text=name)
                title_label.grid(row = notes_row_placement, column= column_placement, padx=5, pady=5, sticky=W+E)
                column_placement += 1

            # increment row placement for next row, reset column placements
            notes_row_placement += 1
            column_placement = 0

            # place job notes data
            for value_tup in self.all_notes_summary_data['values']:

                # add Label for row count
                count_label = Label(self.outer_container, text=notes_row_placement, width=15)
                count_label.grid(row=notes_row_placement, column=column_placement, padx=5, pady=5, sticky=W+E)
                column_placement += 1



                for count, value in enumerate(value_tup):
                    if count < len(value_tup) - 1:

                        value_label = Label(self.outer_container, text=value, width=15)
                        value_label.grid(row=notes_row_placement, column=column_placement, padx=5, pady=5, sticky=W+E)
                        column_placement += 1

                    else:
                        # last value indicates state of complete boolean
                        if value == 0:
                            value_label = Label(self.outer_container, text="Incomplete")
                            value_label.grid(row=notes_row_placement, column=column_placement, padx=5, pady=5, sticky=W+E)

                        else:
                            value_label = Label(self.outer_container, text="Complete")
                            value_label.grid(row=notes_row_placement, column=column_placement, padx=5, pady=5,sticky=W+E)

                # reset column placement for next row
                column_placement = 0
                
                notes_row_placement += 1



# --------------------------------------------------------------------------------------
class NoteView():

    def __init__(self) -> None:
        pass
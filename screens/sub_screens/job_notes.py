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

    def __init__(self, outer_container, db_controller, job_id ) -> None:

        self.outer_container = outer_container
        self.db_controller = db_controller
        self.job_id = job_id
        
        # retrieve all job to_do notes data for current job application
        self.all_notes_summary_data = self.db_controller.retrieve_to_do_note_summary_data(job_id)
        print(self.all_notes_summary_data)



# --------------------------------------------------------------------------------------
class NoteView():

    def __init__(self) -> None:
        pass
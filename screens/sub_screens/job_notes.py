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
                    self.save_data, current_instance)

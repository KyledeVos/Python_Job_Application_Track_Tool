from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date

class SubWindowBasic():
    """Class to generate new window for sub data retrieval (and display) focused on data types as:
    single line data, boolean data(using toggle buttons), large text box data, ComboBoxes for data
    based on single column options from second table (appilcation refers to as fk_data)"""

    def __init__(self, columns_categorized, all_columns, db_controller, single_data_list, boolean_data, large_box_data,
                 fk_data, btns_list, outer_window_reload_func = None, retrieve_data_func = None, 
                  set_data = None) -> None:
        
        # columns categorized as single_data, boolean_data, large_box_data and fk_data
        self.columns_categorized = columns_categorized
        # all columns for table (order of columns is needed for data save in database)
        self.all_columns = all_columns
        # opening of window with instance already containing data (view of current instance)
        # None value implies this is a new instance
        self.set_data = set_data
        
        # add database controller for data reading/retrieval
        self.db_controller = db_controller

        # lists to be populated with data after save
        self.single_data_list = single_data_list
        self.boolean_data = boolean_data
        self.large_box_data = large_box_data
        self.fk_data = fk_data

        # buttons that may need to be displayed from calling window while sub_window is open
        self.btns_list = btns_list

        # function to potentially reload original calling window after sub_window close
        self.outer_window_reload_func = outer_window_reload_func

        # function to retrieve any information from sub_window widgets
        self.retrieve_data_func = retrieve_data_func
 

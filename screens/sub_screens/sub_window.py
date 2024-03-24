from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date

class SubWindowBasic():
    """Class to generate new window for sub data retrieval (and display) focused on data types as:
    single line data, boolean data(using toggle buttons), large text box data, ComboBoxes for data
    based on single column options from second table (appilcation refers to as fk_data)"""

    def __init__(self, window_title, columns_categorized, all_columns, db_controller, single_data_list, boolean_data_list,
                 large_box_data, fk_data, btns_list, save_btn_text, outer_window_reload_func = None, retrieve_data_func = None, 
                  set_data = None) -> None:
         
        self.window_title = window_title
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
        self.boolean_data_list = boolean_data_list
        self.large_box_data = large_box_data
        self.fk_data = fk_data

        # buttons that may need to be displayed from calling window while sub_window is open
        self.btns_list = btns_list
        # desired text for save button
        self.save_btn_text = save_btn_text

        # function to potentially reload original calling window after sub_window close
        self.outer_window_reload_func = outer_window_reload_func

        # function to retrieve any information from sub_window widgets
        self.retrieve_data_func = retrieve_data_func

        # Create new Window
        self.sub_window = Toplevel()
        self.sub_window.title(window_title)
        self.sub_window.geometry("500x600")
        self.sub_window.minsize(600, 550)
        self.sub_window.maxsize(700, 700)

        # track main rows for grid placements of widgets
        label_row_count = 0

        # --------------------------------------------------------------------------------
        # SINGLE ITEMS - SINGLE LINE
        # create single data labels and input boxes (one-line)
        for single_item in self.columns_categorized['single_data']:
            
            # Add Label
            item_descr = Label(self.sub_window, text=single_item, anchor=W)

            # Configuration for Date Field
            if 'date' in single_item.lower():
                # create 
                item_input = self.add_date_field(single_item)

            # non-date, single_line fields     
            else:
                item_input = self.add_single_line_field(single_item)
        
            # add frame, label and input box to window
            item_descr.grid(row=label_row_count, column=0, sticky=W+E, padx=5, pady=5)
            label_row_count += 1
            item_input.grid(row=label_row_count, column=0, sticky=W+E, padx=(20,0), pady=5)
            label_row_count += 1
        # --------------------------------------------------------------------------------
        # FOREIGN TABLES - SELECTION INPUT FROM MENU
            
        for menu_option in self.columns_categorized['fk_data']:
            # add frame to hold label and ComboBox - necessary for spacing and stylings
            holding_frame = Frame(self.sub_window, bootstyle = 'default')

            # add menu label and ComboBox(contains selection options) to fk_data
            # Form: (Label, OptionMenu)
            current_menu_field = self.add_menu_field(menu_option, holding_frame)
            self.fk_data.append(current_menu_field)

            # place holding frame
            holding_frame.grid(row=label_row_count, column=0, columnspan=2, sticky=W+E)
            label_row_count += 1
            
            # load menu options to sub_window
            # current_menu_field[0] - Column Name, current_menu_field[1] - ComboBox
            current_menu_field[0].grid(row=0, column = 0, sticky=W+E, pady=10)
            current_menu_field[1].grid(row=0, column = 1, padx=5, pady=10, sticky=W)

        # --------------------------------------------------------------------------------
        # SINGLE ITEMS - MULTI LINE
        # create single item data labels and input boxes needing larger box
        for multi_line_item in self.columns_categorized['larger_box_data']:
            
            # request creation of large box item consisting of (label, textbox)
            large_box_item = self.add_large_box_field(multi_line_item)

            # add textbox to list to later retrieve input (large_box_item[1] = textbox)
            self.large_box_data.append(large_box_item[1])

            # place large box item (label and textBox) on window screen
            # large_box_item[0] = label
            large_box_item[0].grid(row=label_row_count, column=0, sticky=W+E, padx=5, pady=(10, 5))
            label_row_count += 1
            # large_box_item[1] = textbox
            large_box_item[1].grid(row=label_row_count, column = 0, columnspan=2, padx=5, pady=5, sticky=W+E)
            label_row_count += 1

        # ------------------------------------------------------------------
        # Save Data Button
        self.save_btn = Button(self.sub_window, text=save_btn_text)
        self.save_btn.grid(row=label_row_count, column=0, pady=10)

        # configure specified commmand to save data
        # NOTE: it is required that 'retrieve_data_func' would be designed
        # to work with parsed lists as single_data, boolean_data, large_box_data and fk_data
        self.save_btn.config(command = self.retrieve_data_func)


# ------------------------------------------------------------------------------------------
    def configure_window_open(self):

        # disable specified calling window buttons whilst new_window is open is being created
        for button in self.btns_list:
            button.config(state='disabled')

        # re-enable buttons if sub_window is closed (without save)
        self.sub_window.protocol("WM_DELETE_WINDOW", self.enable_buttons_close_window)

# ------------------------------------------------------------------------------------------
    def add_date_field(self, date_item):
        # check for existing data for date (update/view of progress instance)
        if self.set_data is None: 
            # retrieve current date to set as default
            current_date = [int(val) for val in str(date.today()).split("-")]
            set_year = current_date[0]
            set_month=current_date[1]
            set_day=current_date[2]

        # existing data for date field - retrieve data for initial display
        else:
            # retrieve index of current single data item
            col_index = self.all_columns.index(date_item.lower().replace(" ", "_"))
            # retrieve date
            split_date = [int(val) for val in self.set_data[col_index].split("/")]
            set_year = split_date[0]
            set_month = split_date[1]
            set_day = split_date[2]
        
        # Create Calendar widget for date retrieval
        item_input = DateEntry(self.sub_window, bootstyle='danger', startdate=date(set_year, set_month, set_day))

        # add date item to single_data_list
        self.single_data_list.append(item_input)

        # return date item for placement on window
        return item_input


# ------------------------------------------------------------------------------------------
    def add_single_line_field(self, single_item):
        item_input = Entry(self.sub_window, width=30)

        # POPULATE SINGLE LINE ENTRY BOX - UPDATE ONLY
        # check if current input field has a value to be assigned (when updating job progress instance)
        if self.set_data is not None:
            # retrieve index of current single data item
            col_index = self.all_columns.index(single_item.lower().replace(" ", "_"))
            # Add value to input box
            item_input.insert(0, self.set_data[col_index])
        
        # add single_line item to single_data_list
        self.single_data_list.append(item_input)
        
        # return single-line item for placement on window
        return item_input
    
# ------------------------------------------------------------------------------------------
    def add_menu_field(self, menu_item, holding_frame):

        label = Label(holding_frame, text=menu_item[0], anchor=W)

        menu_options = [val[1] for val in menu_item[1]]
        box = Combobox(holding_frame, bootstyle="success", values=menu_options)

        # POPULATE OPTION MENU WITH CURRENT SET VALUE - UPDATE ONLY
        # check if current input field has a value to be assigned (when updating job progress instance)
        if self.set_data is not None:
            # retrieve index of current single data item
            col_index = self.all_columns.index(menu_item[0].lower().replace(" ", "_"))
            # retrieve name of current set option
            set_val_name = self.set_data[col_index][0]

            for count, data_tup in enumerate(menu_item[1]):
                # iterate through options for menu comparing names until match is found
                if set_val_name == data_tup[1]:
                    box.current(count) 
                    break
        else:
            box.current(0)

        return (label, box)
    
# ------------------------------------------------------------------------------------------
    def add_large_box_field(self, large_box_item):
        label = Label(self.sub_window, text=large_box_item, anchor=W)

        # add textbox for larger text input
        text_box = ScrolledText(self.sub_window, width=80, height=10,wrap=WORD, autohide=True)

        # POPULATE MULTI-LINE TEXT BOX - UPDATE ONLY
        # check if current input field has a value to be assigned (when updating job progress instance)
        if self.set_data is not None:
            # retrieve index of current single data item
            col_index = self.all_columns.index(large_box_item.lower().replace(" ", "_"))
            # Add value to input box
            text_box.insert(END, self.set_data[col_index])

        return (label, text_box)

# ------------------------------------------------------------------------------------------
    def enable_buttons_close_window(self):
        # re-enable main windows buttons if progress window is closed (without save)
        for button in self.btns_list:
            button.config(state='active')

        # clear lists
            if self.single_data_list:
                self.single_data_list.clear()
            if self.boolean_data_list:
                self.boolean_data_list.clear()
            if self.large_box_data:
                self.large_box_data.clear()
            if self.fk_data:
                self.fk_data.clear()

        self.close_sub_window()

# ------------------------------------------------------------------------------------------
    def close_sub_window(self):
        # close sub_window
        self.sub_window.destroy()
        # reload calling window
        self.outer_window_reload_func()

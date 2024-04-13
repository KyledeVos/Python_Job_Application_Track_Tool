from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox, MessageDialog
from datetime import date
from .sub_window import SubWindowBasic
from .job_progress_instance import DataConverter

class NewJobNote(SubWindowBasic):

    def __init__(self, columns_categorized, all_columns, db_controller, single_data_list,
                 boolean_data_list, large_box_data, fk_data, btns_list, outer_window_reload_func = None, 
                 retrieve_note_data_func = None, current_instance = None,  ) -> None:
        
        # Creating new To_Do Note
        if current_instance is None:
            super().__init__("New Note", columns_categorized, all_columns, db_controller, 
                             single_data_list, boolean_data_list, large_box_data, fk_data,
                             btns_list, "Save Note", outer_window_reload_func,
                             retrieve_note_data_func, current_instance)
        
        # Updating/Viewing existing Note
        else:
            super().__init__("Viewing Note", columns_categorized, all_columns, db_controller, 
                    single_data_list, boolean_data_list, large_box_data, fk_data,
                    btns_list, "Update Note", outer_window_reload_func,
                    retrieve_note_data_func, current_instance)

# --------------------------------------------------------------------------------------
class AllNotesView():

    def __init__(self, outer_container, db_controller, job_id, outer_buttons_list, 
                 outer_window_reload_func, include_all = True, deletion_functionality = False,
                 clear_boxes_btn = None, delete_all_btn = None, view_all_btn = None,
                 application_order_var = None) -> None:

        self.outer_container = outer_container
        self.db_controller = db_controller
        self.job_id = job_id
        self.outer_buttons_list = outer_buttons_list
        self.outer_window_reload_func = outer_window_reload_func
        self.include_all = include_all

        # possible arguments for deletion functionality of window
        # NOTE: deletion_functionality of True must have supplied clr_boxes_btn and delete_all_btn
        self.deletion_functionality = deletion_functionality
        self.clear_boxes_btn = clear_boxes_btn
        self.delete_all_btn = delete_all_btn

        # possible outer button for view of all notes
        self.view_all_btn = view_all_btn
        # possible variable tracking application order specification
        self.application_order_var = application_order_var

        self.notes_all_data = None

        self.incomplete_notes_present = None

        # if deletion of job notes functionality is required
        if deletion_functionality:
            # create list to house all job notes checkbuttons and variables
            self.all_notes_deletion_check_data = []
            # configure clear boxes button
            self.clear_boxes_btn.configure(command = self.clear_notes_boxes)
            # configure delete selected notes button
            self.delete_all_btn.configure(command = self.delete_selected_job_notes)

        

    def retrieve_note_data(self, incomplete_only = False, is_data_present=False):

        # update state of incomplete notes present
        self.incomplete_notes_present = self.db_controller.is_incomplete_notes(self.job_id)
        # update state of any job notes present
        self.note_data_present = self.db_controller.is_note_data_present(self.job_id)

        if self.incomplete_notes_present is False and incomplete_only is True:
            self.notes_all_data == None
            return
        
        # Attempt Retrieval of all job to_do notes data -> None indicates no present job notes data
        self.notes_all_data = self.db_controller.retrieve_all_job_note_data(self.job_id, is_data_present, self.application_order_var )

    def load_all_to_do_notes(self, row_count = 0):


        for label in self.outer_container.grid_slaves():
            label.grid_remove()
            
        # check for view all button - disable if there are no notes to display
        if self.view_all_btn is not None:
                if self.note_data_present is False:
                    self.view_all_btn.configure(state='disabled')

        if self.notes_all_data is None:
            # No present note data, display message
            Label(self.outer_container, text="No To-Do Items").grid(row=row_count, column=0, padx=5, pady=5, sticky=W+E)

        # if only incomplete notes display is desired, check if there were incomplete notes present
        elif self.include_all and self.notes_all_data is None:
            Label(self.outer_container, text="No To-Do Items").grid(row=row_count, column=0, padx=5, pady=5, sticky=W+E)
        # 
        else:

            # track placement of rows
            notes_row_placement = row_count

            # if load of notes in done in a seperate window (deletion_functionality is True),
            # outer container must be placed here
            if self.deletion_functionality:
                self.outer_container.grid(row=row_count, column = 0)
                # reset row placement for placement within outer container
                notes_row_placement = 0

            # check for view all button - ensure button is enabled if there are notes to display
            if self.view_all_btn is not None:
                self.view_all_btn.configure(state='active')
                
            
            class JobRow():
                """Inner Class housing row labels and controls load of labels to window. Configures click event handle
                    for label to load job note view window for update of note"""

                def __init__(self, job_note_id, job_note_labels, note_row_placement, 
                             categorized_columns, all_columns, db_controller, outer_buttons_list, 
                             outer_window_reload_func, retrieve_data_func, set_data, delete_window = False,
                            retrieve_note_data = None, load_note_window = None):
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

                    # boolean specifying if row includes deletion functionality
                    self.delete_window = delete_window

                    # functions to reload notes window (application only with deletion functionality)
                    self.retrieve_note_data = retrieve_note_data
                    self.load_note_window = load_note_window

                    # converter for menu based data
                    self.data_converter = DataConverter()

                def load_row(self):

                    # index to start loading data labels
                    start_index = 0
                    end_index = len(self.job_note_lables)
                    
                    # check if job_note deletion functionality is required
                    if self.delete_window:
                        # place checkbutton
                        self.job_note_lables[0][1].grid(row = self.note_row_placement, column = self.column_placement, padx=5, pady=5, sticky=W+E)
                        self.column_placement += 1
                        start_index += 1

                        # final item will be row deletion button, decrement end index by one (stops open_job_view_function being
                        # assigned to deletion button below)
                        end_index -=1

                        self.row_deletion_btn = self.job_note_lables[end_index]
                        self.row_deletion_btn.grid(row = self.note_row_placement, column = end_index, padx=5, pady=5, sticky=W+E)
                        self.row_deletion_btn.configure(command = self.delete_row)

                    for label in self.job_note_lables[start_index:end_index]:
                        label.grid(row = self.note_row_placement, column = self.column_placement, padx=5, pady=5, sticky=W+E)
                        label.bind("<Button-1>", lambda e: self.open_job_view_window(e))
                        self.column_placement += 1

                def open_job_view_window(self, event):

                    self.job_note_view = NewJobNote(self.categorized_columns, self.all_columns, self.db_controller,
                                               self.note_single_data, self.note_boolean_data, self.note_large_box_data,
                                                self.note_fk_data, self.outer_buttons_list, self.outer_window_reload_func,
                                                  self.retrieve_job_note_data_update,  self.set_data)
                    self.job_note_view.configure_window_open()

                def retrieve_job_note_data_update(self):
                    # list to store current progress note data (appended to progress_instance_list at end)
                    note_instance = []
                    # 1) Current Date Field set by default as first field for note instance
                    note_instance.append(self.note_single_data[0].entry.get())

                    # 2) Dealine Date Field set by default as second field for note instance
                    note_instance.append(self.note_single_data[1].entry.get())

                    # 3) Retrieve remaining Single Items
                    for item in self.note_single_data[2:]:
                        note_instance.append(item.get())

                    # 4) Retrieve Boolean Items Data
                    for item in self.note_boolean_data:
                        note_instance.append(item.get())

                    # 5) Retrieve multi-line input data
                    for item in self.note_large_box_data:
                        note_instance.append(item.get("1.0", END).strip())
                            
                    # 6) Retrieve Foreign-Key (Menu-Based Data)
                    for menu_input in self.note_fk_data:
                        menu_title = menu_input[0].cget('text')
                        selected_option = menu_input[1].get()
                    
                        note_instance.append(self.data_converter.return_id_from_name(selected_option, menu_title, self.note_fk_data['fk_data']))


                    # clear lists
                    if self.note_single_data:
                        self.note_single_data.clear()
                    if self.note_boolean_data:
                        self.note_boolean_data.clear()
                    if self.note_large_box_data:
                        self.note_large_box_data.clear()
                    if self.note_fk_data:
                        self.note_fk_data.clear()

                    # update job_note_instance in database
                    self.db_controller.update_job_note_instance(self.all_columns[1:], note_instance + [self.job_note_id])

                    # re-enable buttons to add progress_instance, save new application and close progress window
                    self.job_note_view.enable_buttons_close_window()

                    # print message to user that new note instance has been added to list (not saved in db)
                    Messagebox.show_info(message='Note has been updated')

                def delete_row(self):

                    # Create A deletion warning window (set No as default option)
                    deletion_box = MessageDialog(title="Permanent Deletion Warning", 
                                     message="Deletion cannot be undone\nAre you sure you want to delete?", 
                                    parent=None, buttons=["Yes","No:Primary"])
                    deletion_box.show()

                    # Check for Deletion Confirmation
                    if deletion_box.result== "Yes":

                        # delete row
                        self.db_controller.delete_only_job_note([self.job_note_id])

                        # call for reload of job notes screen
                        self.retrieve_note_data(incomplete_only=False, is_data_present=True)
                        self.load_note_window()
                        # reload outer screen to remove deleted notes from screen view
                        self.outer_window_reload_func()


            # retrieve single data columns for summary display of note data
            self.single_data_cols = [val.lower().replace("_", "_") for val in self.notes_all_data['categorized_column_names']['single_data']]

            # track column placements for each rows
            column_placement = 0

            # check for remaining incomplete notes
            # Check required here when updating notes
            if not self.db_controller.is_incomplete_notes(self.job_id) and self.include_all is False:
                Label(self.outer_container, text="No To-Do Items").grid(row=notes_row_placement, column=0, padx=5, pady=5, sticky=W+E)
                notes_row_placement += 1
                return notes_row_placement

            # ----------- COLUMN TITLES ----------- 
            
            if self.deletion_functionality:
                # Add additional empty column to hold checkbox for selction of job notes for deletion
                column_placement += 1

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

            # keep track of row count
            count = 1

            for job_note_instance in self.notes_all_data['note_values']:
                
                # Perform check for incomplete to-do note
                # NOTE: Current implementation has set 'status' within the boolean_col_indices list used
                # to check for completion of to-do note item
                status_index = self.notes_all_data['all_column_names'].index('status')
                if job_note_instance[status_index] == 1 and self.include_all == False:
                    continue

                current_note = []

                # check if row needs to include checkbox for multiple row deletions
                if self.deletion_functionality:

                    checked = IntVar()
                    checkBox = Checkbutton(self.outer_container, variable=checked, onvalue=1, offvalue=0, 
                                           command=self.enable_disable_clear_deleted_btns)
                    current_note.append((checked, checkBox))
                    # add checked, checkbox and note id (job_instance[0] to list)
                    self.all_notes_deletion_check_data.append([checked, checkBox, job_note_instance[0]])

                # Add row count column value
                current_label = Label(self.outer_container, text=str(count))
                current_note.append(current_label)
                count += 1

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

                # check if deletion functionality is required, if so add button for row deletion
                if self.deletion_functionality:
                    row_deletion_btn = Button(self.outer_container, text="Delete", bootstyle='danger')
                    current_note.append(row_deletion_btn)

                # Create job row instance to uniquely track if of current job note
                # needed to load job note detailed view window, and call for placement of row labels 
                JobRow(job_note_instance[0], current_note, notes_row_placement, 
                       self.notes_all_data['categorized_column_names'], self.notes_all_data['all_column_names'], 
                       self.db_controller, self.outer_buttons_list, self.outer_window_reload_func, 
                       None, job_note_instance, self.deletion_functionality, self.retrieve_note_data,
                       self.load_all_to_do_notes).load_row()
                notes_row_placement += 1

                # # clear current note list for next job note instance
                current_note.clear()

            # return final row placement for possible additional widgets after job rows
            return notes_row_placement


    def enable_disable_clear_deleted_btns(self):

        btns_enable = False

        # perform check if any note deletion checkbuttons have been selected
        for deletion_item in self.all_notes_deletion_check_data:
            if deletion_item[0].get() == 1:
                btns_enable = True
                break
        
        # if at least one note has been selected, enable clear and delete_selected btns
        if btns_enable:
            self.clear_boxes_btn.configure(state='active')
            self.delete_all_btn.configure(state='active')
        else:
            self.clear_boxes_btn.configure(state='disabled')
            self.delete_all_btn.configure(state='disabled')

    def clear_notes_boxes(self):

        # check if checkbutton is on, if so switch off
        for deletion_item in self.all_notes_deletion_check_data:
            if deletion_item[0].get() == 1:
                deletion_item[0].set(0)

        # disable clear boxes button and delete_all_button
        self.clear_boxes_btn.configure(state='disabled')
        self.delete_all_btn.configure(state='disabled')

    def delete_selected_job_notes(self):

        # Create A deletion warning window (set No as default option)
        deletion_box = MessageDialog(title="Permanent Deletion Warning", 
                                     message="Deletion cannot be undone\nAre you sure you want to delete?", 
                                    parent=None, buttons=["Yes","No:Primary"])
        deletion_box.show()

        # Check for Deletion Confirmation
        if deletion_box.result== "Yes":

            delete_id_list = []

            # iterate through all job notes retrieving id's for notes selected for deletion
            for deletion_item in self.all_notes_deletion_check_data:
                if deletion_item[0].get() == 1:
                    # add id of selected job note to deletion list
                    delete_id_list.append(deletion_item[2])

            self.db_controller.delete_only_job_note(delete_id_list)

            # call for reload of job notes screen
            self.retrieve_note_data(incomplete_only=False, is_data_present=True)
            self.load_all_to_do_notes()
            # reload outer screen to remove deleted notes from screen view
            self.outer_window_reload_func()

            # disable clear boxes button and delete_all_button after deletion
            self.clear_boxes_btn.configure(state='disabled')
            self.delete_all_btn.configure(state='disabled')


    def toggle_view_all(self):
        # switch between view all notes and view only incomplete notes
        self.include_all = not self.include_all



from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox, MessageDialog
from ..parent_screens import FullScreen

# Delete an Application
class DeleteApplication(FullScreen):

    def __init__(self, container, db_controller) -> None:
        super().__init__(container)
        self.container = container
        self.db_controller = db_controller
        self.empty_label = Label(container)

        self.container.grid_columnconfigure(0, weight=1)

        self.deletion_items = []

        # top-level buttons
        self.top_level_holder = Frame(container, bootstyle = 'default')
        self.clear_boxes_btn = Button(self.top_level_holder, text="Clear Boxes", bootstyle='primary')
        self.delete_selected_btn = Button(self.top_level_holder, text = 'Delete Selected', bootstyle='danger')

        # list storing possible orders
        self.results_order = ['recent', 'oldest']

        # variable to track selected main screen
        self.application_order = StringVar()
        # set default order type as first in results_order
        self.application_order.set(self.results_order[0])

    def deselect_all(self):
        for item in self.deletion_items:
            item.uncheck_box()
        # disbaled clear box and delete all buttons
        self.clear_boxes_btn.configure(state='disabled')
        self.delete_selected_btn.configure(state='disabled')

    def delete_selected_jobs(self):

        id_list = [item.get_job_id() for item in self.deletion_items if item.checked.get() == 1]
        
        # create gramatically correct message
        if len(id_list) == 1:
            display_message = "Are you sure you want to delete this job?\nThis action cannot be undone"
        else:
            display_message = f"Are you sure you want to delete {len(id_list)} jobs?\nThis action cannot be undone"

        # Create New Window to display deletion warning message before deleting jobs with 'No' set as Primary
        deletion_box = MessageDialog(title="Permanent Deletion Warning", message=display_message,
                                     buttons=["Yes", "No:Primary"])
        deletion_box.show()

        # Display Yes or No Box to confirm Deletion
        if deletion_box.result == "Yes":
            # delete all job progress notes associated with job_id
            self.db_controller.delete_job_progress_data(id_list)
            # delete all job progress notes associated with job_id
            self.db_controller.delete_job_notes(id_list)
            # delete job application data
            self.db_controller.delete_job_data(id_list)

            # reload window after deletion
            for screen in self.container.grid_slaves():
                screen.grid_forget()

            self.load_window()

    def delete_clear_box_disable(self):
        
        selected_box = False
        for item in self.deletion_items:
            if item.get_selection() == 1:
                selected_box = True
                break

        if selected_box == True:
            self.clear_boxes_btn.configure(state='active')
            self.delete_selected_btn.configure(state='active')

        elif selected_box == False:
            self.clear_boxes_btn.configure(state='disabled')
            self.delete_selected_btn.configure(state='disabled')


    def load_window(self):
        
        # configure functions for clear_boxes and delete_selected
        self.clear_boxes_btn.configure(command=self.deselect_all, state='disabled')
        self.delete_selected_btn.configure(command=self.delete_selected_jobs, state = 'disabled')

        # ---------------------------------------------------------------
        # DATA RETRIEVAL
        # retrieve all application data - id and desired columns specified by database controller
        current_applications = self.db_controller.retrieve_job_application_date_ordered(self.application_order.get())
        

        if len(current_applications) == 0:
            Label(self.container, text="No Job Applications").grid(row=0, column=0)
        
        else:
            # Application Sort Order Elements --------------------------------------------

            # Frame to house sorting label and menubutton
            sort_frame = Frame(self.container, bootstyle='default')

        
            # add combo box label
            ordering_label = Label(sort_frame, text="Sort By:", anchor=W)
            
            # add MenuButton for sorting options
            self.order_box = Menubutton(sort_frame, style='primary', text=self.application_order.get())
            self.menu = Menu(self.order_box)

            # set each ordering option as a radiobutton
            for menu_option in self.results_order:
                self.menu.add_radiobutton(label=menu_option, value=menu_option, variable=self.application_order, 
                                          command=lambda: self.load_sort_menu(self.application_order.get()))
                
            # allows association of menu containing radio buttons for screen to MenuButton Widget
            self.order_box['menu'] = self.menu

            # Column Titles --------------------------------------------------------------
            self.column_titles = [name.title().replace("_", " ") for name in self.db_controller.retrieve_job_column_names()[1:len(current_applications[0])]]

            # ---------------------------------------------------------------
            # DELETION ITEM CLASS
            class DeletionItem():

                def __init__(self, container, job_data_tup, db_controller, reload_window_func, delete_clear_box_disable) -> None:
                    self.db_controller = db_controller
                    self.reload_window_func = reload_window_func
                    self.delete_clear_box_disable = delete_clear_box_disable
                    self.container = container

                    self.containing_box = Frame(container, bootstyle = 'default')

                    self.checked = IntVar()
                    self.checkBox = Checkbutton(self.containing_box, variable=self.checked, onvalue=1, offvalue=0, command=delete_clear_box_disable)
                    self.delete_job_btn = Button(self.containing_box, text='Delete', bootstyle='danger')

                    self.id = job_data_tup[0]
                    self.label_list = []

                    for job_entry in list(job_data_tup)[1:]:
                        self.label_list.append(Label(self.containing_box, text = job_entry, width=20, anchor=W))

                    
                def place_on_screen(self, row):

                    # configure individual deletion button command
                    self.delete_job_btn.config(command=self.delete_job)

                    self.containing_box.grid(row=row, column=0, pady=5)
                    column_count = 0
                    self.checkBox.grid(row=row, column=column_count, pady=2)
                    column_count += 1

                    for label in self.label_list:
                        label.grid(row=row_count, column=column_count, padx=5, pady=2)
                        column_count +=1

                    self.delete_job_btn.grid(row=row_count, column=column_count)

                def delete_job(self):
                    
                    # Create A deletion warning window (set No as default option)
                    deletion_box = MessageDialog(title="Deletion Warning", message="Sure you want to delete", 
                                                 parent=None, buttons=["No:Primary", "Yes"])
                    deletion_box.show()

                    # Check for Deletion Confirmation
                    if deletion_box.result== "Yes":
                        
                        # delete all job progress notes associated with job_id
                        self.db_controller.delete_job_progress_data([self.id])
                        # delete all job progress notes associated with job_id
                        self.db_controller.delete_job_notes([self.id])
                        # delete job application data
                        self.db_controller.delete_job_data([self.id])
                    # reload window after row deletion
                        for screen in self.container.grid_slaves():
                            screen.grid_forget()
                        self.reload_window_func()


                def get_job_id(self):
                    return self.id
                
                def get_selection(self):
                    return self.checked.get()
                
                def uncheck_box(self):
                    self.checked.set(0)

            # ---------------------------------------------------------------
            # ELEMENT PLACEMENT ON SCREEN

            # Track row placements
            row_count = 0

            # Application Ordering Label and Menu
            sort_frame.grid(row=row_count, column=0, columnspan=4, sticky = W+E)
            ordering_label.grid(row=0, column=0, pady=5)
            self.order_box.grid(row=0, column=1, pady=5)
            row_count += 1


            # load top-level buttons
            self.top_level_holder.grid(row=row_count, column=0, pady=10, sticky = W+E)
            row_count += 1
            self.clear_boxes_btn.grid(row=0, column=0)
            self.delete_selected_btn.grid(row=0, column=1, padx=5)

            # column count track for titles
            column_count = 0

            # container for column title
            titles_container = Frame(self.container, bootstyle='default')
            titles_container.grid(row=row_count, column=0, columnspan=4, sticky = W+E)
            row_count += 1

            # place column titles
            for title in self.column_titles:

                # add empty label as space for checkbox buttons
                if column_count == 0:
                    Label(titles_container, text="", width=5).grid(row=0, column=0)
                    column_count += 1
                Label(titles_container, text=title, width=20, anchor=W).grid(row=0, column = column_count)
                column_count += 1

                    
            # clear deletion items from potential previous screen load
            self.deletion_items.clear()
            for application in current_applications:
                item = DeletionItem(self.container, application, self.db_controller, self.load_window, self.delete_clear_box_disable)
                item.place_on_screen(row_count)
                self.deletion_items.append(item)
                row_count+=1


    def load_sort_menu(self, selected_order):

        # clear old applications from screen
        for widget in self.container.grid_slaves():
            widget.grid_forget()
        
        # update track of ordering value
        self.application_order.set(selected_order)
        # set menu text to current ordering selection
        self.order_box.config(text=selected_order)
        # reload job applications
        self.load_window()
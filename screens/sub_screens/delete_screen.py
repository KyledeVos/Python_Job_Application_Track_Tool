from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox
from ..parent_screens import FullScreen

# Delete an Application
class DeleteApplication(FullScreen):

    def __init__(self, container, db_controller) -> None:
        super().__init__(container)
        self.container = container
        self.db_controller = db_controller
        self.empty_label = Label(container)

        self.deletion_items = []

        # top-level buttons
        self.top_level_holder = Frame(container, bootstyle = 'default')
        self.clear_boxes_btn = Button(self.top_level_holder, text="Clear Boxes", bootstyle='primary')
        self.delete_selected_btn = Button(self.top_level_holder, text = 'Delete Selected', bootstyle='danger')

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

        # Display Yes or No Box to confirm Deletion
        if(Messagebox.yesno(title='Permanent Deletion Warning!', 
                               message=display_message)) == "Yes":
            # delete all job progress notes associated with job_id
            self.db_controller.delete_job_progress_data(id_list)
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
        current_applications = self.db_controller.retrieve_job_display_cols()
        

        if len(current_applications) == 0:
            Label(self.container, text="No Job Applications").grid(row=0, column=0)
        
        else:
            # retrieve column titles
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

                    
                def place_on_screen(self, row, column):

                    # configure individual deletion button command
                    self.delete_job_btn.config(command=self.delete_job)

                    self.containing_box.grid(row=row, column=0, pady=5)
                    column_count = column
                    self.checkBox.grid(row=row, column=column_count, pady=2)
                    column_count += 1

                    for label in self.label_list:
                        label.grid(row=row_count, column=column_count, padx=5, pady=2)
                        column_count +=1

                    self.delete_job_btn.grid(row=row_count, column=column_count)

                def delete_job(self):
                    # Display Yes or No Box to confirm Deletion
                    if(Messagebox.yesno(title='Permanent Deletion Warning!', 
                               message="Are you sure you want to delete this job?\nThis action cannot be undone") == "Yes"):
                        
                        # delete all job progress notes associated with job_id
                        self.db_controller.delete_job_progress_data([self.id])
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

            # load top-level buttons
            self.top_level_holder.grid(row=0, column=0, pady=10)
            self.clear_boxes_btn.grid(row=0, column=0)
            self.delete_selected_btn.grid(row=0, column=1, padx=5)

            # Job Instance Placements
            row_count = 2
            
            # clear deletion items from potential previous screen load
            self.deletion_items.clear()
            for application in current_applications:
                item = DeletionItem(self.container, application, self.db_controller, self.load_window, self.delete_clear_box_disable)
                item.place_on_screen(row_count, 0)
                self.deletion_items.append(item)
                row_count+=1
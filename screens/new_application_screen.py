from tkinter import *
from .parent_screens import FullScreen

class NewApplicationScreen(FullScreen):

    def __init__(self, container):
        super().__init__(container)

        # ----------------------------------------------------------------
        # company name
        self.company_name_lbl = Label(container, text="'Company:")
        

        self.company_name = Entry(container, width=50, borderwidth=1)
        self.company_name.insert(0, "Company")
        

        # ----------------------------------------------------------------
        # Job Position
        self.position_lbl = Label(container, text="Position")
        

        self.position = Entry(container, width=50, borderwidth=2)
        self.position.insert(0, "Position")
        

        # ----------------------------------------------------------------
        # Salary
        self.salary_lbl = Label(container, text="Salary")
        

        self.salary = Entry(container, width=50, borderwidth=2)
        self.salary.insert(0, "Salary")
        

        # ----------------------------------------------------------------
        # Date Applied
        self.application_date_lbl = Label(container, text="Date Applied")
        
        self.application_date = Entry(container, width=50, borderwidth=2)
        self.application_date.insert(0, "Application Date")
        

        # ----------------------------------------------------------------
        # Location
        self.location_lbl = Label(container, text="Location")
        

        self.location = Entry(container, width=50, borderwidth=2)
        self.location.insert(0, "Location")
        

        # ----------------------------------------------------------------
        # Description
        self.description_lbl = Label(container, text="Description")
       

        self.description = Entry(container, width=50, borderwidth=2)
        self.description.insert(0, "Description")
        

    def load_window(self):
        
        self.company_name_lbl.grid(row=0, column=0, padx=2, pady=2, sticky=W+E)
        self.company_name.grid(row=0, column=1, sticky=W+E)
        self.position_lbl.grid(row=1, column=0, padx=2, pady=2, sticky=W+E)
        self.position.grid(row=1, column=1, sticky=W+E)
        self.salary_lbl.grid(row=2, column=0, padx=2, pady=2, sticky=W+E)
        self.salary.grid(row=2, column=1, sticky=W+E)
        self.application_date_lbl.grid(row=3, column=0, padx=2, pady=2, sticky=W+E)
        self.application_date.grid(row=3, column=1, sticky=W+E)
        self.location_lbl.grid(row=4, column=0, padx=2, pady=2, sticky=W+E)
        self.location.grid(row=4, column=1, sticky=W+E)
        self.description_lbl.grid(row=5, column=0, padx=2, pady=2, sticky=W+E)
        self.description.grid(row=5, column=1, sticky=W+E)





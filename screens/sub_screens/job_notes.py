from ttkbootstrap import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.dialogs import Messagebox
from datetime import date

class NewJobNote():

    def __init__(self, db_controller, job_note_attributes, job_id) -> None:

        self.db_controller = db_controller
        self.job_note_attributes = job_note_attributes
        self.job_id = job_id

    def create_note_window(self):

        # Create New Window when adding job (to-do) note
        self.note_window= Toplevel()
        self.note_window.title("New Job Note")
        self.note_window.geometry("500x600")
        self.note_window.minsize(600, 550)
        self.note_window.maxsize(700, 700)
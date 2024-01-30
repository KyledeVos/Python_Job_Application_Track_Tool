from tkinter import *

from controllers.application_controller import ApplicationController

def start_application():
    database = 'test.db'
    app_control = ApplicationController(database)
    app_control.start_app()

start_application()
# import sub controllers
from .screen_controller import ScreenController
from .database_controller import DatabaseController

# DATABASE COMPONENTS
# -------------------------------------------------
from persistence_modules.db_initializer import DbInitializer

class ApplicationController():

    def __init__(self, database) -> None:
        self.db_initializer = DbInitializer()
        
        # initialize controllers
        self.screen_controller = ScreenController()
        self.database_controller = DatabaseController(database, self.db_initializer)

    def start_app(self):
        self.database_controller.initialize_database()
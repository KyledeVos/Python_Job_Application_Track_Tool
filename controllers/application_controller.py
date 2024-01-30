# import sub controllers
from .screen_controller import ScreenController
from .database_controller import DatabaseController

# DATABASE COMPONENTS
# -------------------------------------------------
from persistence_modules.db_initializer import DbInitializer

class ApplicationController():

    def __init__(self, database) -> None:
        self.db_initializer = DbInitializer()
        
        # initialize database controller and perform database configuration
        self.database_controller = DatabaseController(database, self.db_initializer)
        self.database_controller.initialize_database()

        # initialize application controller - creates main app screen
        self.screen_controller = ScreenController()

    def start_app(self):
        # start application
        self.screen_controller.start_main_screen()
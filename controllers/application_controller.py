# import sub controllers
from .screen_controller import ScreenController
from .database_controller import DatabaseController

# DATABASE COMPONENTS
# -------------------------------------------------
from persistence_modules.db_initializer import DbInitializer
from persistence_modules.db_reader import DbReader

class ApplicationController():

    def __init__(self, database) -> None:

        # initialize Database Controller Components
        self.db_initializer = DbInitializer()
        self.db_reader = DbReader()
        
        # initialize database controller and perform database configuration
        self.database_controller = DatabaseController(database, self.db_initializer, self.db_reader)
        self.database_controller.initialize_database()

        # initialize application controller - creates main app screen
        self.screen_controller = ScreenController(self.database_controller)

    def start_app(self):
        # start application
        self.screen_controller.start_main_screen()
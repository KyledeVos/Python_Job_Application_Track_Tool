from .screen_controller import ScreenController
from .database_controller import DatabaseController

class ApplicationController():

    def __init__(self, database) -> None:
        
        self.screen_controller = ScreenController()
        self.database_controller = DatabaseController(database)
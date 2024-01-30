import sqlite3
from persistence_modules.parents.initialize_db_parent import InitializeDbParent

class DatabaseController():

    def __init__(self, database, InitializeDbParent) -> None:
        self.database = database
        self.connection = None
        self.cursor = None
        self.db_initializer = InitializeDbParent

    def create_all_tables(self):

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        self.db_initializer.create_all_tables(self.connection, self.cursor)

        self.connection.close()
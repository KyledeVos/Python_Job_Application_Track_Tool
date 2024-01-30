import sqlite3

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
        self.db_initializer.set_default_values(self.connection, self.cursor)

        # testing population
        # print(self.db_initializer.retrieve_all_single_col(self.cursor, "employment_types", "type"))

        self.connection.close()
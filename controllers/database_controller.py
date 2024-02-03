import sqlite3

class DatabaseController():

    def __init__(self, database, InitializeDbParent, DbReader) -> None:
        self.database = database
        self.connection = None
        self.cursor = None
        self.db_initializer = InitializeDbParent
        self.db_reader = DbReader

    def initialize_database(self):

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        self.db_initializer.create_all_tables(self.connection, self.cursor)
        self.db_initializer.set_default_values(self.connection, self.cursor)

        # testing population
        # print(self.db_initializer.retrieve_all_single_col(self.cursor, "employment_types", "type"))

        self.connection.close()

    def retrieve_single_col(self, column_name, table_name):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_single_col_list(self.cursor, column_name, table_name)
        self.connection.close()

        return data
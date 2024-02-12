import sqlite3

class DatabaseController():

    def __init__(self, database, InitializeDbParent, DbReader, DbWriter) -> None:
        self.database = database
        self.connection = None
        self.cursor = None
        self.db_initializer = InitializeDbParent
        self.db_reader = DbReader
        self.db_writer = DbWriter

    # -----------------------------------------------------------------
    # Database and/or Table Initialization

    def initialize_database(self):

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        self.db_initializer.create_all_tables(self.connection, self.cursor)
        self.db_initializer.set_default_values(self.connection, self.cursor)

        # testing population
        # print(self.db_initializer.retrieve_all_single_col(self.cursor, "employment_types", "type"))

        self.connection.close()

    # -----------------------------------------------------------------
    # Database Reading

    def retrieve_single_col(self, column_name, table_name):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_single_col_list(self.cursor, column_name, table_name)
        self.connection.close()

        return data


    def retrieve_id_single_col(self, column_name, table_name): 
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_id_single_col(self.cursor, column_name, table_name)
        self.connection.close()

        return data
    

    def retrieve_single_row(self, id, table_name):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_single_row(self.cursor, id, table_name)
        self.connection.close()

        return data
    

    def retrieve_column_names_no_id(self, table_name):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_column_names(self.cursor, table_name)
        self.connection.close()

        return data
    

    def retrieve_col_specific(self, columns, table_name):
        
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_col_specific(self.cursor, columns, table_name)
        self.connection.close()

        return data


    def retrieve_all_data(self, table_name):

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_all_data(self.cursor, table_name)
        self.connection.close()

        return data
    
    def retrieve_job_data_configured(self, job_id=None):
        
        # Set Default Values
        table_name = 'job_applications'
        # set end of number of columns containing single data (not menu option)
        single_end_index = 7

        # names of tables linked with foreign key
        fk_tables = ['employment_types', 'contract_period', 'application_status']

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_and_config_data(self.cursor, table_name, fk_tables, single_end_index, job_id,)
        self.connection.close()

        return data


    # -----------------------------------------------------------------
    # Database Writing

    def write_single_row_no_id(self, table_name, value_list):

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        # retrieve all column names (except id) for table
        column_names = self.db_reader.retrieve_column_names(self.cursor, table_name)[1:]

        self.db_writer.write_single_row(self.connection, self.cursor, table_name, column_names, value_list )
        self.connection.close()

    def update_row(self, table_name, column_list, values):

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.update_row(self.connection, self.cursor, table_name, column_list, values)
        self.connection.close()

        
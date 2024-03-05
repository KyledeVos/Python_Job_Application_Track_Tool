import sqlite3

class JobProgressDefaults():
    # Class allows for centralized control of job progress attributes

    def __init__(self):
        # Set Default Table Name
        self.table_name = 'progress'
        # set names of columns with data for one line
        self.single_data = ['date']
        # set column names for data needing larger area input box
        self.larger_data_inputs = ['description']
        # set names of foreign key tables with corresponding column name
        self.fk_tables = {'progress_table_cols': ['comm_id'], "fk_table_data": [('communication_types', 'communication_type')]}
        # set names of columns to not be displayed (none must be blank list)
        self.col_not_display = ["job_id"]
        

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
        self.populate_table_defaults()

        self.connection.close()


    def populate_table_defaults(self):
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        # Employment Types Table
        emp_columns = ["type"]
        emp_values = [('Full Time',), ('Part Time',), ('Temporary',), ('Contractor',), ('Freelance',)]
        self.db_initializer.def_table_populate(self.connection, self.cursor, "employment_types", emp_columns, emp_values)

        # Contract Duration Table
        cont_duration_cols = ["duration"]
        cont_duration_vals = [('3 Months',), ('6 Months',), ('12 Months',), ('24 Months',), ('Permanent',), ('Not Specified',)]
        self.db_initializer.def_table_populate(self.connection, self.cursor, "contract_period", cont_duration_cols, cont_duration_vals)

        # Application Status Table
        app_status_cols = ["status"]
        app_status_vals = [('Applied',), ('Testing',), ('First Interview',), ('Second Interview',),
                                ('Received Offer',), ("Declined", ), ("Rejected", ), ("Accepted",)]
        self.db_initializer.def_table_populate(self.connection, self.cursor, "application_status", app_status_cols, app_status_vals)

        # Communication Type Table - Job Application Progress
        comm_type_cols = ['communication_type']
        comm_type_vals =  [('Email',), ('Telephone',), ('Cellphone',), ('SMS',), ('WhatsApp',), ('Company System',)]
        self.db_initializer.def_table_populate(self.connection, self.cursor, "communication_types", comm_type_cols, comm_type_vals)

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
    

    def retrieve_job_column_names(self):

        # Set Default Values
        table_name = "job_applications"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_column_names(self.cursor, table_name)
        self.connection.close()

        return data
    
    # --------------------------------------------------------------------------------------------------
    # Job Progress Section
    def retrieve_job_progress_column_names(self):

        # Use of this method assumes columns in table are ordered as:
        # id column, Single Data, Singe Data needing larger area input box, foreign key id's

        # Retrieve default values for job_progress instance
        progress_default_instance = JobProgressDefaults()
        
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        # retrieve configured table column names data
        # Data to be configured as:
        # {'single_data': [()], 'larger_box_data':[()], 'fk_data':[[()]]}
        data = self.db_reader.retrieve_configured_job_progress_columns(
            self.cursor, progress_default_instance.table_name, progress_default_instance.single_data,
                progress_default_instance.larger_data_inputs, progress_default_instance.fk_tables)
        self.connection.close()

        return data
    

    def retrieve_recent_job_progress(self, search_id):

        progress_instance = JobProgressDefaults()

        # set column used as most recent reference 
        # will use the most recent (highest) id
        search_column = "id"
        identify_column = "job_id"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        data = self.db_reader.retrieve_progress_rows_complex(self.cursor, progress_instance.table_name, 
                                                    identify_column, search_id, progress_instance.larger_data_inputs,
                                                    progress_instance.fk_tables, progress_instance.col_not_display,
                                                    order_by_col = search_column, return_one = True, display_only = True)

        self.connection.close()
        return data
        # --------------------------------------------------------------------------------------------------


    def retrieve_job_display_cols(self):

        # Set Default Values
        # Specify columns to be displayed when displaying all applications (summary)
        title_columns = ['company, position']
        table_name = 'job_applications'
        
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_col_specific(self.cursor, title_columns, table_name)
        self.connection.close()

        return data


    def retrieve_all_job_data(self):

        # Set Default Values
        table_name = "job_applications"

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
    # Database Writing and Deletion

    def write_single_job_no_id(self, value_list):

        # Set Default Values
        table_name = "job_applications"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        # retrieve all column names (except id) for table
        column_names = self.db_reader.retrieve_column_names(self.cursor, table_name)[1:]

        lastid = self.db_writer.write_single_row(self.connection, self.cursor, table_name, column_names, value_list )
        self.connection.close()
        return lastid
    

    def write_job_progress(self, progress_data, job_id):

        # Set Default Values
        table_name = "progress"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        # retrieve all column names (except id) for table
        column_names = self.db_reader.retrieve_column_names(self.cursor, table_name)[1:]
        # ['date', 'description', 'comm_id', 'job_id']

        # seperate and write individual progress instances
        for progress_instance in progress_data:
            self.db_writer.write_single_row(self.connection, self.cursor, table_name, column_names, progress_instance + [job_id])
        self.connection.close()


    def update_job_application(self, column_list, values):

        # Set default Values
        table_name = "job_applications"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.update_row(self.connection, self.cursor, table_name, column_list, values)
        self.connection.close()

    def delete_job_data(self, id_values):

        # Set default values
        table_name = "job_applications"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.delete_job_application(self.connection, self.cursor, table_name, id_values)
        self.connection.close()

    def delete_job_progress_data(self, id_list):

        # Set default values
        table_name = "progress"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.delete_job_progress(self.connection, self.cursor, table_name, id_list)
        self.connection.close()
        
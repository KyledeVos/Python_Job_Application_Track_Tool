import sqlite3

class JobApplicationDefault():

    def __init__(self) -> None:

        # NOTE: Fields that require calendar widget for display MUST include 'date' as a substring 
        # of field name

        # Set Default Table Name
        self.table_name = 'job_applications'
        # set names of columns with data for one line
        self.single_data = ['id', 'date', 'company', 'position', 'salary', 'location']
        # set column names for data needing larger area input box
        self.larger_data_inputs = ['description']
        # set names of foreign key tables with corresponding column name
        # NOTE: ORDER OF DATA IS COMPULSORY
        self.fk_tables_data = {'job_application_cols': ['type_id', 'period_id', 'status_id'],
                          "fk_table_data": [('employment_types', 'type'),
                                            ('contract_period', 'duration'),
                                            ('application_status', 'status')]}
        # set names of columns to not be displayed (none must be blank list)
        self.col_not_display = ["id"]
        # Data Update - set columns that can be updated
        self.update_cols = ['date', 'company', 'position', 'salary', 'location', 'description',
                            'type_id', 'period_id', 'status_id']


class JobProgressDefaults():
    # Class allows for centralized control of job progress attributes

    def __init__(self):

        # NOTE: Fields that require calendar widget for display MUST include 'date' as a substring 
        # of field name

        # Set Default Table Name
        self.table_name = 'progress'
        # set names of columns with data for one line
        self.single_data = ['date', 'title']
        # set names of columns for boolean data
        self.boolean_data = []
        # set column names for data needing larger area input box
        self.larger_data_inputs = ['description']
        # set names of foreign key tables with corresponding column name
        self.fk_tables = {'progress_table_cols': ['comm_id'], "fk_table_data": [('communication_types', 'communication_type')]}
        # set names of columns to not be displayed (none must be blank list)
        self.col_not_display = ["job_id"]
        # Data Update - set columns that can be updated
        self.update_cols = ['date', 'description', 'comm_id']

class JobNotesDefaults():
    # Class allows for centralized control of job progress attributes

    def __init__(self):

        # NOTE: Fields that require calendar widget for display MUST include 'date' as a substring 
        # of field name

        # Set Default Table Name
        self.table_name = 'job_notes'
        # set names of columns with data for one line
        self.single_data = ['date', 'due_date', 'title']
        # set names of columns holding booleans
        self.boolean_data = ['status']
        # set column names for data needing larger area input box
        self.larger_data_inputs = ['description']
        # set names of foreign key tables with corresponding column name
        self.fk_tables = None
        # set names of columns to not be displayed (none must be blank list)
        self.col_not_display = ["job_id"]
        # Data Update - set columns that can be updated
        self.update_cols = ['date',  'due_date', 'title', 'description']
        

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
    # Database Reading General

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

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        # Use of this method assumes columns in table are ordered as:
        # id column, Single Data, Boolean Data, Single Data needing larger area input box, foreign key Data

        # Retrieve default values for job_progress instance
        progress_default_instance = JobProgressDefaults()

        # dictionary to hold summarized data
        column_names_dict = {}
        # retrieve single data column names
        column_names_dict['single_data'] = tuple([val.title().replace("_", " ") for val in progress_default_instance.single_data])
        # retrieve boolean data column names
        column_names_dict['boolean_data'] = tuple([val.title().replace("_", " ") for val in progress_default_instance.boolean_data])
        # retrieve large box dat column names
        column_names_dict['larger_box_data'] = tuple([val.title().replace("_", " ") for val in progress_default_instance.larger_data_inputs])
        
        

        # retrieve fk_data
        data = self.db_reader.retrieve_fk_data_columns(
            self.cursor, progress_default_instance.fk_tables)
        self.connection.close()

        column_names_dict['fk_data'] = tuple(data)
        return column_names_dict
    

    def retrieve_job_progress_cols_exact(self):

        table_name = 'progress'

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_column_names(self.cursor, table_name)
        self.connection.close()

        return data
    

    def retrieve_job_progress_data(self, search_id, return_one, display_only):

        progress_instance = JobProgressDefaults()

        # set column used as most recent reference 
        # will use the most recent (highest) id
        search_column = "id"
        identify_column = "job_id"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        data = self.db_reader.retrieve_progress_rows_complex(self.cursor, progress_instance.table_name, 
                                                    identify_column, search_id, progress_instance.fk_tables,
                                                    progress_instance.larger_data_inputs, progress_instance.col_not_display,
                                                    return_one, display_only, order_by_col = search_column)

        self.connection.close()
        return data
        
    # -------------------------------------------------------------------------------------------------
    # Job Notes (To-Do) Section
    def retrieve_job_notes_column_names(self):
        
        job_notes_default = JobNotesDefaults()
        
        # dictionary to hold summarized data
        column_names_dict = {}
        # retrieve single data column names
        column_names_dict['single_data'] = tuple([val.title().replace("_", " ") for val in job_notes_default.single_data])
        # retrieve boolean columns
        column_names_dict['boolean_data'] = tuple([val.title().replace("_", " ") for val in job_notes_default.boolean_data])
        # retrieve large box dat column names
        column_names_dict['larger_box_data'] = tuple([val.title().replace("_", " ") for val in job_notes_default.larger_data_inputs])

        # set fk_data to empty list
        column_names_dict['fk_data'] = []

        return column_names_dict
    
    def retrieve_all_job_note_data(self, job_id):
        # Default values
        table_name = "job_notes"
        # data dict to hold column names and associated values
        col_val_data = {}
        # columns to not include in display
        cols_not_display = JobNotesDefaults().col_not_display

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        # retrieve and check if note data exists for job application
        note_data = self.db_reader.retrieve_job_notes_data(self.cursor, table_name, 'job_id', job_id)

        if not note_data:
                self.connection.close()
                return None

        # At this point, job application has existing note data
        col_val_data['note_values'] = note_data

        # retrieve categorized column names
        col_val_data['categorized_column_names'] = self.retrieve_job_notes_column_names()
        

        # retrieve all column names and remove columns to not be displayed
        col_val_data['all_column_names'] = [val for val in 
                                            self.db_reader.retrieve_column_names(self.cursor, table_name)
                                            if val not in cols_not_display]

        self.connection.close()

        return col_val_data


    def is_incomplete_notes(self, job_id):

        # Set Defaults
        table_name = "job_notes"
        # name of field marked for status 
        status_field = "status"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        is_incomplete_data = self.db_reader.check_incomplete_notes(self.cursor, table_name, status_field, "job_id", job_id)

        self.connection.close()

        return is_incomplete_data
    

    # -------------------------------------------------------------------------------------------------
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
    
    def retrieve_configured_job_data(self, job_id=None):

        job_application_defaults = JobApplicationDefault()
        
        # Set Default Values
        table_name = job_application_defaults.table_name
        # retrieve columns designated as single_data
        single_data = job_application_defaults.single_data
        # retrieve columns designated to hold large box (textbox) data
        large_box_data = job_application_defaults.larger_data_inputs
        # retrieve fk_data
        fk_tables_data = job_application_defaults.fk_tables_data

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        data = self.db_reader.retrieve_configured_job_data(self.cursor, table_name, single_data, large_box_data, fk_tables_data, job_id,)
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
        # ['date', 'title', 'description', 'comm_id', 'job_id']

        # seperate and write individual progress instances
        for progress_instance in progress_data:
            self.db_writer.write_single_row(self.connection, self.cursor, table_name, column_names, progress_instance + [job_id])
        self.connection.close()

    def write_job_to_do_note(self, note_data, job_id):
        # Set Default Values
        table_name = "job_notes"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()

        # retrieve all column names (except id) for table
        column_names = self.db_reader.retrieve_column_names(self.cursor, table_name)[1:]
        # ['date', 'title', 'description', 'comm_id', 'job_id']

        # seperate and write individual progress instances
        for note_instance in note_data:
            self.db_writer.write_single_row(self.connection, self.cursor, table_name, column_names, note_instance + [job_id])
            print(note_instance)
        self.connection.close()

    def update_job_application(self, column_list, values):

        # Set default Values
        table_name = "job_applications"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.update_row(self.connection, self.cursor, table_name, column_list, values)
        self.connection.close()

    def update_job_progress(self, column_list, values):

        # Set default Values
        table_name = "progress"

        # remove columns that may be in column list that are not to be updated
        job_progress_controller = JobProgressDefaults()

        for column in column_list:
            if column in job_progress_controller.col_not_display:
                column_list.remove(column)

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.update_row(self.connection, self.cursor, table_name, column_list, values)
        self.connection.close()

    def update_job_note_instance(self, column_list, values):

        # Set Defaults
        table_name = "job_notes"

        job_note_defaults = JobNotesDefaults()
        for column in column_list:
            if column in job_note_defaults.col_not_display:
                column_list.remove(column)

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.update_row(self.connection, self.cursor, table_name, column_list, values)

        self.connection.close()

    # ----------------------------------------------------------------
    # JOB APPLICATION DELETION

    def delete_job_data(self, id_values):

        # Set default values
        table_name = "job_applications"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.delete_job_application(self.connection, self.cursor, table_name, id_values)
        self.connection.close()

    # ----------------------------------------------------------------
    # JOB PROGRESS DELETION
    
    # Delete All Job Progress data for associated job instance
    def delete_job_progress_data(self, id_list):

        # Set default values
        table_name = "progress"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.delete_job_progress(self.connection, self.cursor, table_name, id_list)
        self.connection.close()

    # Delete job progress (not associated job instance)
    def delete_job_progress_only(self, id_list):

        # Set default values
        table_name = "progress"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.delete_single_job_progress(self.connection, self.cursor, table_name, id_list)
        self.connection.close()

    
    # ----------------------------------------------------------------
    # JOB NOTES DELETION
        
    def delete_job_notes(self, id_list):

        # Set default values
        table_name = "job_notes"

        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
        self.db_writer.delete_job_progress(self.connection, self.cursor, table_name, id_list)
        self.connection.close()
        
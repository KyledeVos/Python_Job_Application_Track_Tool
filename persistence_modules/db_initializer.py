
class DbInitializer():

    def __init__(self):
       pass

    def create_all_tables(self, connection, cursor):

        # ===========================================================================
        # JOB APPLICATION TABLES
        # ===========================================================================

        # CREATE Employment Type Table
        cursor.execute("""CREATE TABLE IF NOT EXISTS employment_types(
        id INTEGER PRIMARY KEY,
        type TEXT NOT NULL)""")
        connection.commit()

        # ---------------------------------------------------------------------
        # CREATE Contract Duration Tables
        cursor.execute("""CREATE TABLE IF NOT EXISTS contract_period(
        id INTEGER PRIMARY KEY,
        duration TEXT NOT NULL)""")
        connection.commit()
        
        # ---------------------------------------------------------------------
        # CREATE Application Status Table
        cursor.execute("""CREATE TABLE IF NOT EXISTS application_status(
        id INTEGER PRIMARY KEY,
        status TEXT NOT NULL)""")
        connection.commit()

        # ---------------------------------------------------------------------
        # CREATE Main Job Application Table

        cursor.execute("""CREATE TABLE IF NOT EXISTS job_applications(
        id INTEGER PRIMARY KEY,
        company TEXT NOT NULL,
        position TEXT NOT NULL,
        salary TEXT,
        date_applied TEXT NOT NULL,
        location TEXT NOT NULL,
        description TEXT,
        type_id INT,
        period_id INT,
        status_id INT,
        FOREIGN KEY(type_id) REFERENCES employment_types(id),
        FOREIGN KEY(period_id) REFERENCES contract_period(id),
        FOREIGN KEY(status_id) REFERENCES application_status(id)         
        )""")

        connection.commit()

        # ---------------------------------------------------------------------
        # CREATE communication type table for Application Progress Table

        cursor.execute("""CREATE TABLE IF NOT EXISTS communication_type(
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL
        )""")
        connection.commit()


        # ---------------------------------------------------------------------
        # CREATE Job Application Progress Table
        cursor.execute("""CREATE TABLE IF NOT EXISTS progress(
            id INTEGER PRIMARY KEY,
            job_id INTEGER NOT NULL, 
            description TEXT NOT NULL,
            comm_id INTEGER NOT NULL,
            FOREIGN KEY(job_id) REFERENCES job_applications(id),
            FOREIGN KEY(comm_id) REFERENCES communication_type(id)
        )""")
        connection.commit()

        # ---------------------------------------------------------------------
        # CREATE Job Notes Table

        cursor.execute("""CREATE TABLE IF NOT EXISTS job_notes(
        id INTEGER PRIMARY KEY,
        job_id INTEGER NOT NULL,
        description TEXT NOT NULL,
        to_do BOOLEAN,
        complete BOOLEAN,
        FOREIGN KEY(job_id) REFERENCES job_applications(id)
        )""")
        connection.commit()

    
        # ===========================================================================
        # GENERAL NOTES TABLE
        # ===========================================================================

        # CREATE General Notes Table

        cursor.execute("""CREATE TABLE IF NOT EXISTS general_notes(
        id INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        to_do BOOLEAN,
        complete BOOLEAN
        )""")
        connection.commit()


    # Helper Function
    def def_table_populate(self, connection, cursor, table_name, columns, values):

        if len(cursor.execute(f"SELECT * FROM {table_name}").fetchall()) == 0:
        
            # begin query construction for row(s) insertion
            query = f"INSERT INTO {table_name}({' '.join(columns)}) VALUES("
            for i in range(len(columns)):
                # create corresponding number of '?' according to number of fields in table
                query += "?"
                # stop adding commas for '?' separation
                if i != (len(columns) - 1):
                    query += ", "
            # close query string
            query += ")"

            cursor.executemany(query, values)
            connection.commit()


    def set_default_values(self, connection, cursor):
        emp_columns = ["type"]
        emp_values = [('Full Time',), ('Part Time',), ('Temporary',), ('Contractor',), ('Freelance',)]
        self.def_table_populate(connection, cursor, "employment_types", emp_columns, emp_values)

        cont_duration_cols = ["duration"]
        cont_duration_vals = [('3 months',), ('6 months',), ('12 months',), ('24 months',), ('permanent',)]
        self.def_table_populate(connection, cursor, "contract_period", cont_duration_cols, cont_duration_vals)

        app_status_cols = ["status"]
        app_status_vals = [('Applied',), ('Testing',), ('First Interview',), ('Second Interview',),
                                ('Received Offer',), ("Declined", ), ("Rejected", ), ("Accepted", )]
        self.def_table_populate(connection, cursor, "application_status", app_status_cols, app_status_vals)


    # def retrieve_all_single_col(self, cursor, table_name, column):
    #     return cursor.execute(f"Select {column} from {table_name}").fetchall() 


# connection = sqlite3.connect('test.db')
# cursor = connection.cursor()
# initial = DbInitializer()
# # initial.create_all_tables(connection, cursor)
# initial.set_default_values(connection, cursor)
# print(initial.retrieve_all_single_col(cursor, "employment_types", "type"))













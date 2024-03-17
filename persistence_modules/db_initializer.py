import sqlite3

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
        date TEXT NOT NULL,
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

        cursor.execute("""CREATE TABLE IF NOT EXISTS communication_types(
            id INTEGER PRIMARY KEY,
            communication_type TEXT NOT NULL
        )""")
        connection.commit()


        # ---------------------------------------------------------------------
        # CREATE Job Application Progress Table
        # STANDARD ORDER TO FOLLOW FOR NEW COLUMNS:
        # 1) Single-Line Inputs
        # 2) Multi-line Inputs
        # 3) Foreign Key ID's (available before job progress instance is created) - comm_id
        # 4) Foreign Key ID's (only available after job progress instance is created) - job_id
        cursor.execute("""CREATE TABLE IF NOT EXISTS progress(
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            comm_id INTEGER NOT NULL,
            job_id INTEGER NOT NULL,
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


    # Function To Populate a Specified Table with Default Values
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
















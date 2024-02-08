

class DbReader():

    def __init__(self):
        pass
    
    # ----------------------------------------------------------------------------------
    # Generic Functions

    def retrieve_all_data(self, cursor, table_name):
        return cursor.execute(f"SELECT * FROM {table_name}").fetchall()
    
    def retrieve_single_col_list(self, cursor, column, table_name):
        return [item[0] for item in cursor.execute(f"SELECT {column} FROM {table_name}").fetchall()]
    
    def retrieve_single_col(self, cursor, id, column_name, table_name):
        return cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE id={id}").fetchone()

    def retrieve_id_single_col(self, cursor, column, table_name):
         return cursor.execute(f"SELECT id, {column} FROM {table_name}").fetchall()
    
    def retrieve_single_row(self, cursor, id, table_name):
        return cursor.execute(f"SELECT * FROM {table_name} WHERE id={id}").fetchone()
    
    def retrieve_col_names(self, cursor, table_name):
        # column name method retrieval from stackoverflow on 07/02/2024: Author: 'do-me'
        # Available from: 
        """https://stackoverflow.com/questions/947215/how-to-get-a-list-of-column-names-on-sqlite3-database#:~:
        text=To%20find%20the%20column%20name,following%20code%20for%20the%20same.&text=This%20will%20print%20all
        %20the%20column%20names%20of%20the%20result%20set.
        """
        data =  cursor.execute("PRAGMA table_info({}) ".format(table_name)).fetchall()
        return [i[1] for i in data]
    
    def retrieve_col_specific(self, cursor, columns, table_name):
        return cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name}").fetchall()
    
    def retrieve_all_column_names(self, cursor, table_name):
        cursor.execute(F"SELECT * FROM {table_name}")
        return [name[0] for name in cursor.description][1:]
    
    # ----------------------------------------------------------------------------------
    # Data Specific Functions

    def retrieve_and_config_job_data(self, cursor, id):
        
        # retrieve all column names and raw job data incl. id's of linked tables
        job_columns = [name.title().replace("_", " ") for name in self.retrieve_col_names(cursor, 'job_applications')]
        job_data_raw = list(self.retrieve_single_row(cursor, id, 'job_applications'))

        # set end of single data
        single_end = 7

        # list holding single data (not based on Foreign Key)
        single_data = list(zip(job_columns[1:single_end], job_data_raw[1:single_end]))

        # names of tables linked with foreign key
        fk_tables = ['employment_types', 'contract_period', 'application_status']

        # list holding data based on Foreign Key (Used for Option Menus)
        menu_data = []
        current_data = []
        for name in fk_tables:
            current_data = [val[1] for val in self.retrieve_all_data(cursor, name)]
            set_value = self.retrieve_single_row(cursor, job_data_raw[single_end], name)[1]
            menu_data.append((name.title().replace("_", " "), current_data, set_value))
            single_end += 1

        job_data = {'single_data': single_data, 'menu_data':menu_data}
        print(job_data)

        
        # NEEDS TO BE REMOVED FROM HERE

        # correct data in job data from foreign key id to correct data name
        job_data_raw[7] = list(self.retrieve_single_col(cursor, job_data_raw[7], 'type', 'employment_types'))[0]
        job_data_raw[8] = list(self.retrieve_single_col(cursor, job_data_raw[8], 'duration', 'contract_period'))[0]
        job_data_raw[9] = list(self.retrieve_single_col(cursor, job_data_raw[9], 'status', 'application_status'))[0]

        # correct column names: id link to other table -> actual column name
        job_columns[7] = "Employment Type"
        job_columns[8] = "Employment Duration"
        job_columns[9] = "Application Status"

        # correct column name style to Title Format and remove underscores
        for i in range(len(job_columns)):
            job_columns[i] = job_columns[i].title().replace("_", " ")

        # remove job id from data and zip column name and job data into single list
        return list(zip(job_columns[1:], job_data_raw[1:]))
        
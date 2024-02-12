

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
        
    def retrieve_col_specific(self, cursor, columns, table_name):
        return cursor.execute(f"SELECT id, {', '.join(columns)} FROM {table_name}").fetchall()
    
    def retrieve_column_names(self, cursor, table_name):
        cursor.execute(f"SELECT * FROM {table_name}")
        return [name[0] for name in cursor.description]

    
    # ----------------------------------------------------------------------------------
    # Data Specific Functions

    def retrieve_and_config_data(self, cursor, table_name, fk_tables, single_end_index, id=None):
        
        # retrieve all column names and raw data incl. id's of linked tables
        column_names = [name.title().replace("_", " ") for name in self.retrieve_column_names(cursor, table_name)]
        if id != None:
            raw_data = list(self.retrieve_single_row(cursor, id, table_name))

        # list holding single data (not based on Foreign Key)
        if id != None:
            single_data = list(zip(column_names[:single_end_index], raw_data[:single_end_index]))
        else:
            single_data = column_names[1:single_end_index]

        # list holding data based on Foreign Key (Used for Option Menus)
        menu_data = []
        current_data = []
        for table_name in fk_tables:
            # get menu option values
            current_data = [val for val in self.retrieve_all_data(cursor, table_name)]

            if id != None:
                set_value = self.retrieve_single_row(cursor, raw_data[single_end_index], table_name)[1]
                menu_data.append((table_name.title().replace("_", " "), current_data, set_value))
                single_end_index += 1
            else:
                menu_data.append((table_name.title().replace("_", " "), current_data))

        combined_data = {'single_data': single_data, 'menu_data':menu_data}
        return combined_data
        

        


class DbReader():

    def __init__(self):
        pass

    def retrieve_all_data(self, cursor, table_name):
        return cursor.execute(f"Select * from {table_name}").fetchall()
    
    def retrieve_single_col_list(self, cursor, column, table_name):
        return [item[0] for item in cursor.execute(f"Select {column} from {table_name}").fetchall()]

    def retrieve_id_single_col(self, cursor, column, table_name):
         return cursor.execute(f"Select id, {column} from {table_name}").fetchall()
    
    def retrieve_col_specific(self, cursor, columns, table_name):
        return cursor.execute(f"Select id, {', '.join(columns)} from {table_name}").fetchall()
    
    def retrieve_all_column_names(self, cursor, table_name):
        cursor.execute(F"SELECT * FROM {table_name}")
        return [name[0] for name in cursor.description][1:]

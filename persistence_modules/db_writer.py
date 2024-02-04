

class DbWriter():
        
    def __init__(self):
        pass

    def write_single_row(self, connection, cursor, table_name, column_list, value_list):
                
        # begin query construction for row(s) insertion
        query = f"INSERT INTO {table_name}({', '.join(column_list)}) VALUES("
        for i in range(len(column_list)):
            # create corresponding number of '?' according to number of fields in table
            query += "?"
            # stop adding commas for '?' separation
            if i != (len(column_list) - 1):
                query += ", "
        # close query string
        query += ")"

        cursor.execute(query, value_list)
        connection.commit()


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
        return cursor.lastrowid

    def update_row(self, connection, cursor, table_name, column_list, values):
     
        # construct column name section of query
        column_query = ""
        for index in range(len(column_list)):
            if index != len(column_list) - 1:
                column_query += column_list[index] + "= ?, "
            else:
                column_query += column_list[index] + "= ? "

        update_query = f"UPDATE {table_name} SET {column_query} WHERE id = ?"
        cursor.execute(update_query, values)
        connection.commit()


    def delete_job_application(self, connection, cursor, table_name, id_values):
        for id in id_values:
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (id,))
            connection.commit()

    def delete_job_progress(self, connection, cursor, table_name, id_list):
        for id in id_list:
            cursor.execute(f"DELETE FROM {table_name} WHERE job_id = ?", (id,))
            connection.commit()

    def delete_single_job_progress(self, connection, cursor, table_name, id_list):
        for id in id_list:
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (id,))
            connection.commit()

    def delete_job_notes(self, connection, cursor, table_name, id_list):
        for id in id_list:
            cursor.execute(f"DELETE FROM {table_name} WHERE job_id = ?", (id,))
            connection.commit()

    def delete_only_job_note(self, connection, cursor, table_name, id_list):
        for id in id_list:
            cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (id,))
            connection.commit()


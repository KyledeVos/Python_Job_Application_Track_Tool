

class DbReader():

    def __init__(self):
        pass

    def retrieve_all_data(self, connection, cursor, table_name):
        return cursor.execute(f"Select * from {table_name}").fetchall() 

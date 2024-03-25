import sqlite3
from persistence_modules.db_reader import DbReader

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

reader = DbReader()

print(cursor.execute("SELECT * FROM job_notes").fetchall())

# print(reader.retrieve_column_names(cursor, 'job_applications'))
# print(cursor.execute('SELECT * FROM progress').fetchall())
# print(cursor.execute('SELECT * FROM progress where job_id=6 order by id DESC LIMIT 1').fetchall())


# # print(cursor.execute('SELECT * FROM job_applications').fetchall())
# cursor.execute("DELETE FROM progress WHERE id=2")
# connection.commit()

# cursor.execute("UPDATE job_applications SET location = ?, salary = ? where id = ?", ("Ghana", 130000, 1))
# connection.commit()

# print(cursor.execute("SELECT * FROM job_applications").fetchall())

# # cursor.execute(F"SELECT * FROM job_applications")
# # print([name[0] for name in cursor.description])
    

connection.close()






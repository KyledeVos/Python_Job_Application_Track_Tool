import sqlite3

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

# print(cursor.execute('SELECT * FROM job_applications').fetchall())
# cursor.execute("DELETE FROM job_applications")
# connection.commit()

# print(cursor.execute("SELECT * FROM job_applications").fetchall())

connection.close()
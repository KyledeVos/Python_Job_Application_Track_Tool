import sqlite3

connection = sqlite3.connect("test.db")
cursor = connection.cursor()

# # print(cursor.execute('SELECT * FROM job_applications').fetchall())
# # cursor.execute("DELETE FROM job_applications")
# # connection.commit()

# cursor.execute("UPDATE job_applications SET location = ?, salary = ? where id = ?", ("Ghana", 130000, 1))
# connection.commit()

# print(cursor.execute("SELECT * FROM job_applications").fetchall())

# # cursor.execute(F"SELECT * FROM job_applications")
# # print([name[0] for name in cursor.description])
    

connection.close()






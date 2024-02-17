# import sqlite3

# connection = sqlite3.connect("test.db")
# cursor = connection.cursor()

# # print(cursor.execute('SELECT * FROM job_applications').fetchall())
# # cursor.execute("DELETE FROM job_applications")
# # connection.commit()

# cursor.execute("UPDATE job_applications SET location = ?, salary = ? where id = ?", ("Ghana", 130000, 1))
# connection.commit()

# print(cursor.execute("SELECT * FROM job_applications").fetchall())

# # cursor.execute(F"SELECT * FROM job_applications")
# # print([name[0] for name in cursor.description])
    

# connection.close()

# ----------------------------------------------------------------------
# SCROLLABLE SCREEN TESTING

from tkinter import *
from tkinter import ttk

root = Tk()

root.geometry("400x400")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# canvas = Canvas(root, bg='blue')
# child_frame = Frame(canvas)
# canvas.create_window(0, 0, window=child_frame, anchor="nw")
# def update_size(e=None):
#     canvas["scrollregion"] = canvas.bbox("all")
#     canvas.configure(yscrollcommand=my_scrollbar.set)
# my_scrollbar = ttk.Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)



# canvas.bind('<Configure>', update_size)
# canvas.after_idle(update_size)
# canvas.pack()
# child_frame.pack()



# my_scrollbar.pack(side=RIGHT, fill=Y)

# for element in range(100):
#     Button(child_frame, text = f'button: {element}').grid(row=element, column=0, pady=10, padx = 10)



main_frame = Frame(root, bg='green')
main_frame.grid(row=0, column=0, sticky="news")
main_frame.grid_rowconfigure(0, weight = 1)
main_frame.grid_columnconfigure(0, weight= 1)

main_canvas = Canvas(main_frame, bg='purple')
main_canvas.grid(row=0, column = 0, sticky="news")
main_canvas.grid_rowconfigure(0, weight=1)
main_canvas.grid_columnconfigure(0, weight=1)

second_frame = Frame(main_canvas, bg='yellow')
second_frame.grid_columnconfigure(0, weight=1)

# 3) Add the Scrollbar to the Canvas (it goes to the mainframe)
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=main_canvas.yview)
my_scrollbar.grid(row = 0, column=0, sticky='NSE')
# my_scrollbar.pack(side=RIGHT, fill=Y)


# 4) Configure the Canvas
main_canvas.configure(yscrollcommand=my_scrollbar.set)
main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))



second_frame.grid(row=0, column=0, sticky = "NEWS")



for element in range(100):
    Button(second_frame, text = f'button: {element}').grid(row=element, column=0, pady=10, padx = 10)


root.mainloop()
# ----------------------------------------------------------------------

# from tkinter import *

# root = Tk()
# root.geometry("500x500")
# root.grid_rowconfigure(0, weight = 1)
# root.grid_columnconfigure(0, weight = 1)

# outer_frame = Frame(root)
# outer_frame.grid(row=0, column=0, sticky="NEWS")

# label = Label(outer_frame, text = "Hello")
# label.grid(row=0, column=0)



# root.mainloop()





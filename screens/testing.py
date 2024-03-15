from tkinter import *
from tkinter import ttk
from tkinter import messagebox



# Create an instance of tkinter frame
root=Tk()


root.geometry("500x600")
root.minsize(500, 550)
root.maxsize(500, 700)


main_frame = Frame(root, bg="yellow")
main_frame.grid(row=0, column=0, sticky="NEWS", padx=5, pady=5)

my_canvas = Canvas(main_frame)
my_canvas.grid(row = 0, column=0, sticky="NEWS")

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL)
my_scrollbar.config(command=my_canvas.yview)
my_scrollbar.grid(row = 0, column=0, sticky='NSE')

second_frame = Frame(my_canvas)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))
my_canvas.bind_all('<MouseWheel>', lambda e: my_canvas.yview_scroll(-1 * int(e.delta / 60), "units"))
# 6) Add a new window to the canvas
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")


inner_frame = Frame(second_frame, borderwidth=2, relief='solid', padx=20, pady=20)
inner_frame.grid(row=0, column=0)

for i in range(0, 20):
    Button(inner_frame, text=i).grid(row=i, column=0)

root.mainloop()
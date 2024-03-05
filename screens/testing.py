from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Create an instance of tkinter frame
win=Tk()

second = None

def open_new_window(second):
    second = Toplevel(win)

    lbl = Label(second, text="Hello").grid(row=0, column=0)

   
    holder = Frame(second)
    holder.grid(row=1, column=0)
    input = Text(holder)
    input.grid(row=0, column = 0)

    close_btn = Button(second, text="Close Window", command=lambda: close_window(second, input))
    close_btn.grid(row=2, column=0)

def close_window(second, input):
    print(input.get("1.0", END))
    second.destroy()
    

open_window = Button(win, text = "Open Window", command=lambda: open_new_window(second))
open_window.grid(row=0, column=0)



win.mainloop()
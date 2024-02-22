from tkinter import *

root = Tk()

class DeletionItem():

    def __init__(self, container, company, position, id) -> None:
        self.container = container
        self.id = id
        self.selected = IntVar()

        self.checkbox = Checkbutton(container, variable=self.selected)
        self.companyLabel = Label(container, text = position)
        self.positionLabel = Label(container, text=position)
        self.delete_btn = Button(container, text="Delete")


    def checked(self):
        pass



var = IntVar()

def update():
    label = Label(root, text = var.get()).pack()

checkbox1 = Checkbutton(root, text = "First Box", variable=var)
checkbox1.pack()

btn = Button(root, text = "Submit", command=update).pack()



root.mainloop()
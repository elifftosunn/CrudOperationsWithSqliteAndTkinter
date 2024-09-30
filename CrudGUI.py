from tkinter import *
import tkinter as tk

class GUICrud:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('600x600')
        self.root.title('Crud Operations with Tkinter')
        self.root.iconphoto(False, PhotoImage(file=r"C:\Users\dptos\Downloads\database.png"))
        self.root.resizable(False, False)
        self.root.configure(background="#FFCCFF")
        self.createCrudGUI()
        self.menubar = self.MenuBar()
    def doNothing(self):
        pass
    def MenuBar(self):
        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="New", command=self.doNothing)
        self.filemenu.add_command(label="Open", command=self.doNothing)
        self.filemenu.add_command(label="Save", command=self.doNothing)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.doNothing)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.root.config(menu=self.menubar)
    def createCrudGUI(self):
        self.f_name = Entry(self.root, width=30)
        self.f_name.grid(row=1, column=1)

        self.l_name = Entry(self.root, width=30)
        self.l_name.grid(row=2, column=1)

        self.address = Entry(self.root, width=30)
        self.address.grid(row=3, column=1)

        self.city = Entry(self.root, width=30)
        self.city.grid(row=4, column=1)

        self.state = Entry(self.root, width=30)
        self.state.grid(row=5, column=1)

        self.zipCode = Entry(self.root, width=30)
        self.zipCode.grid(row=6, column=1)

        # Create Text Box Label
        titleLabel = Label(self.root, text="Crud Operations")
        titleLabel.grid(row=0, column=0, columnspan=2, ipadx=175, padx=20, pady=10, sticky=W)
        titleLabel.configure(background="#FFCCFF", font=("Helvetica", 16, "bold"))

        f_name_label = Label(self.root, text='First Name')
        f_name_label.grid(row=1, column=0, padx=5, pady=10)
        self.colorLabel(f_name_label)

        l_name_label = Label(self.root, text='Last Name')
        l_name_label.grid(row=2, column=0, padx=5, pady=10)
        self.colorLabel(l_name_label)

        address_label = Label(self.root, text='Address')
        address_label.grid(row=3, column=0, padx=5, pady=10)
        self.colorLabel(address_label)

        city_label = Label(self.root, text='City')
        city_label.grid(row=4, column=0, padx=5, pady=10)
        self.colorLabel(city_label)

        state_label = Label(self.root, text='State')
        state_label.grid(row=5, column=0, padx=5, pady=10)
        self.colorLabel(state_label)

        zipCode_label = Label(self.root, text='Zip Code')
        zipCode_label.grid(row=6, column=0, padx=5, pady=10)
        self.colorLabel(zipCode_label)

    def colorButton(self, button):
        button.configure(bg="#990099", fg="white", height=2, font=("Arial", 10, "bold"))
    def colorLabel(self, label):
        label.configure(bg="#CCE5FF", fg="black", font=("Arial", 10, "bold"), highlightbackground="#990099", highlightthickness=0.5)

    def createBtn(self, insertData, query, delete, update):
        # Create Record Button
        self.add_btn = Button(self.root, text='Add record the database', command=insertData)
        self.add_btn.grid(row=7, column=0, pady=20, padx=10)
        self.colorButton(self.add_btn)

        # Create a query button
        self.query_btn = Button(self.root, text='Show Records', command=query)
        self.query_btn.grid(row=7, column=1, pady=20, padx=10)
        self.colorButton(self.query_btn)

        self.updateOrDeleteRecordLabel = Label(self.root, text='Enter first name the record to be deleted or updated')
        self.updateOrDeleteRecordLabel.grid(row=8, column=0, padx=10, pady=10)
        self.colorLabel(self.updateOrDeleteRecordLabel)
        self.updateOrDeleteRecordEntry = Entry(self.root, width=30)
        self.updateOrDeleteRecordEntry.grid(row=8, column=1, padx=10, pady=10)

        # Delete record
        self.delete_btn = Button(self.root, text="Delete Record", command=delete)
        self.delete_btn.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=127)
        self.colorButton(self.delete_btn)

        # Update record
        self.update_btn = Button(self.root, text="Update Record", command=update)
        self.update_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=126)
        self.colorButton(self.update_btn)

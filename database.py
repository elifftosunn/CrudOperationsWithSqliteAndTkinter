import sqlite3
from tkinter import messagebox
from tkinter import *
import tkinter as tk
from tkinter import ttk
from CrudGUI import GUICrud

class DBSQlite(GUICrud):
    def __init__(self):
        self.conn = sqlite3.connect('crm_customers.db')
        self.c = self.conn.cursor()
        self.createTable()
        super().__init__()
        self.createBtn(self.insertData, self.query, self.delete, self.update)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def close(self):
        if messagebox.askyesno(title="Quit", message="Are you sure you want to quit?"):
            self.root.destroy()
            self.conn.close()

    def __del__(self):
        if self.conn:
            self.conn.close()
            print("Connection closed (destructor)")
    def createTable(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS Customers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            first_name VARCHAR(50),
                            last_name VARCHAR(50),
                            address text,
                            city VARCHAR(50),
                            state VARCHAR(50),
                            zipcode INTEGER
            )""")
            self.conn.commit()
        except Exception as e:
            return e


    def insertData(self):
        try:
            self.c.execute("""INSERT INTO Customers (first_name, last_name, address, city, state, zipcode) 
                         VALUES (:f_name, :l_name, :address, :city, :state, :zipCode)""",
                      {
                          'f_name': self.f_name.get(),
                          'l_name': self.l_name.get(),
                          'address': self.address.get(),
                          'city': self.city.get(),
                          'state': self.state.get(),
                          'zipCode': self.zipCode.get()
                      })
            self.customer_id = self.c.lastrowid
            # commit changes
            if self.conn.commit() == None:
                messagebox.showinfo(title="Added Record", message="Record added successfully!")
                self.new_window.destroy()

        except Exception as e:
            print(e)

        # clear the text boxed
        self.f_name.delete(0, END)
        self.l_name.delete(0, END)
        self.address.delete(0, END)
        self.city.delete(0, END)
        self.state.delete(0, END)
        self.zipCode.delete(0, END)

    def query(self):
        try:
            # query the database
            self.c.execute("SELECT * FROM Customers")
            # fetch the requested records
            records = self.c.fetchall()  # c.fetchone(), c.fetchmany(30)
            # commit changes
            self.conn.commit()
            self.showAllRecords(records)
        except Exception as e:
            print(e)
    def move_row_up(self):
        rows = self.my_tree.selection()
        for row in rows:
            self.my_tree.move(row, self.my_tree.parent(row), self.my_tree.index(row) - 1)
    def move_row_down(self):
        rows = self.my_tree.selection()
        for row in reversed(rows):
            self.my_tree.move(row, self.my_tree.parent(row), self.my_tree.index(row) + 1)
    def remove_one_record(self):
        self.c.execute(f"DELETE FROM Customers WHERE id = {self.customer_id}")
        if self.conn.commit() == None:
            messagebox.showinfo(title="Delete Record", message="Record deleted successfully!")
            self.new_window.destroy()
        # self.my_tree.delete(self.my_tree.selection()[0])
    def remove_many_records(self):
        customer_id_list = []
        for record in self.my_tree.selection():
            customer_id_list.append(self.my_tree.item(record, "values")[0])
        id_string_query = ', '.join(id for id in customer_id_list)
        try:
            self.c.execute(f"DELETE FROM Customers WHERE id IN ({id_string_query})")
            if self.conn.commit() == None:
                messagebox.showinfo(title="Delete Records", message="Records deleted successfully!")
                self.new_window.destroy()
            else:
                messagebox.showinfo(title="Records not deleted", message="Records weren't deleted")
        except Exception as e:
            print(e)
    def remove_all_records(self):
        response = messagebox.askyesno("Delete All Records", "Are you sure you want to delete all records?")
        if response == True:
            self.c.execute("DROP TABLE Customers;")
            if self.conn.commit() == None:
                messagebox.showinfo(title="Records deleted", message="Records deleted successfully!")
                self.createTable()
        else:
            messagebox.showinfo(title="Records not deleted", message="Records weren't deleted")
        # for record in self.my_tree.get_children():
        #     self.my_tree.delete(record)
    def showAllRecords(self, records):
        self.new_window = tk.Tk()
        self.new_window.title("All Records")
        self.new_window.geometry("710x500")
        self.new_window.configure(background="#FFCCFF")

        # create ttk Style window
        self.style = ttk.Style(self.new_window)
        self.style.theme_use("classic")
        # change background color
        self.style.configure("Treeview.Heading", background="#808080", foreground="black", font=("Arial", 10, "bold"),
                        highlightbackground="black", highlightthickness=0.5, fieldbackground="#FFCCFF")
        # change selected color
        self.style.map("Treeview", background=[("selected", "#003366")], foreground=[("selected", "white")])
        # create a treeview frame
        self.tree_frame = Frame(self.new_window)
        self.tree_frame.pack(pady=10)
        # create a treeview scrollbar
        self.tree_scrollbar = Scrollbar(self.tree_frame)
        self.tree_scrollbar.pack(side=RIGHT, fill=Y)
        # create the treeview
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scrollbar.set, selectmode="extended", show="headings")
        self.my_tree.pack()
        # configure the scrollbar
        self.tree_scrollbar.config(command=self.my_tree.yview)
        # define columns
        self.my_tree["columns"] = ("Id", "First Name", "Last Name", "Address", "City", "State", "Zip Code")
        # format columns
        self.my_tree.column("Id", width=0, stretch=NO)
        self.my_tree.column("First Name", width=100, minwidth=20, anchor="center")
        self.my_tree.column("Last Name", width=100, minwidth=20, anchor="center")
        self.my_tree.column("Address", width=100, minwidth=20, anchor="center")
        self.my_tree.column("City", width=100, minwidth=20, anchor="center")
        self.my_tree.column("State", width=100, minwidth=20, anchor="center")
        self.my_tree.column("Zip Code", width=100, minwidth=20, anchor="center")
        # create headings
        self.my_tree.heading("Id", text="id")
        self.my_tree.heading("First Name", text="first name")
        self.my_tree.heading("Last Name", text="last name")
        self.my_tree.heading("Address", text="address")
        self.my_tree.heading("City", text="city")
        self.my_tree.heading("State", text="state")
        self.my_tree.heading("Zip Code", text="zip code")
        # create striped row tags
        self.my_tree.tag_configure("oddrow", background="white")
        self.my_tree.tag_configure("evenrow", background="#C0C0C0")
        # add data to the screen
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                self.my_tree.insert('', 'end', values=(record[0], record[1], record[2], record[3], record[4],
                                                  record[5], record[6]), tags=("evenrow", ))
            else:
                self.my_tree.insert('', 'end', values=(record[0], record[1], record[2], record[3], record[4],
                                                  record[5], record[6]), tags=("oddrow", ))
            count += 1
        print(records)
        self.operationsOnData()

        self.new_window.mainloop()
    def clear_entries(self):
        # clear entry boxes
        self.f_name.delete(0, END)
        self.l_name.delete(0, END)
        self.address.delete(0, END)
        self.city.delete(0, END)
        self.state.delete(0, END)
        self.zipCode.delete(0, END)
    def select_record(self, e):
        # clear entry boxes
        self.f_name.delete(0, END)
        self.l_name.delete(0, END)
        self.address.delete(0, END)
        self.city.delete(0, END)
        self.state.delete(0, END)
        self.zipCode.delete(0, END)
        # grab record number
        selected = self.my_tree.focus()
        # grab record values
        values = self.my_tree.item(selected, "values")
        # output to entry boxes
        self.f_name.insert(0, values[1])
        self.l_name.insert(0, values[2])
        self.address.insert(0, values[3])
        self.city.insert(0, values[4])
        self.state.insert(0, values[5])
        self.zipCode.insert(0, values[6])
    def operationsOnData(self):
        # add button for crud operations
        button_frame = LabelFrame(self.new_window, text="Operations on Data")
        button_frame.pack(fill=X, expand=True, padx=20)
        remove_all_records = Button(button_frame, text="Remove All Records", command=self.remove_all_records)
        remove_all_records.grid(row=0, column=0, padx=5, pady=5)
        remove_one_record = Button(button_frame, text="Remove One Record", command=self.remove_one_record)
        remove_one_record.grid(row=0, column=1, padx=5, pady=5)
        remove_many_selected = Button(button_frame, text="Remove Many Records", command=self.remove_many_records)
        remove_many_selected.grid(row=0, column=2, padx=5, pady=5)
        move_up = Button(button_frame, text="Move Up", command=self.move_row_up)
        move_up.grid(row=0, column=3, padx=5, pady=5)
        move_down = Button(button_frame, text="Move Down", command=self.move_row_down)
        move_down.grid(row=0, column=4, padx=5, pady=5)
        select_record = Button(button_frame, text="Clear Entry Boxes", command=self.clear_entries)
        select_record.grid(row=0, column=5, padx=5, pady=5)
        # bind the treeview
        self.my_tree.bind("<<TreeviewSelect>>", self.select_record)
    def delete(self):
        try:
            self.c.execute("DELETE FROM Customers WHERE first_name = ?",
                      [self.updateOrDeleteRecordEntry.get()])
            if self.conn.commit() == None:
                messagebox.showinfo(title="Delete Record", message="Record deleted successfully!")
                self.new_window.destroy()
        except Exception as e:
            print(e)
    def update(self):
        try:
            # Create a list of all fields and their corresponding values
            fields = {"first_name": self.f_name.get(), "last_name": self.l_name.get(), "address": self.address.get(),
                      "city": self.city.get(), "state": self.state.get(), "zipCode": self.zipCode.get()}
            valid_fields = [fieldName for fieldName, value in fields.items() if value != ""]  # Filter out empty fields
            valid_field_values = [value for fieldName, value in fields.items() if value != ""]
            # Construct the SQL query based on valid fields
            sql_query = "UPDATE Customers SET "
            set_clause = ", ".join(f"{field} = ?" for field in valid_fields)
            sql_query += set_clause + f" WHERE first_name = ?"
            # Execute the query with the valid values
            self.c.execute(sql_query, valid_field_values + [self.updateOrDeleteRecordEntry.get()])
            if self.conn.commit() == None:
                messagebox.showinfo(title="Update Record", message="Record updated successfully!")
                self.new_window.destroy()
        except Exception as e:
            print(e)

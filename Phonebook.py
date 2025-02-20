""" Gui program for accessing contacts """

import sqlite3 as sql
import tkinter as tk
from tkinter import ttk

# DB Setup
contactdb = sql.connect("contacts.db")
dbcursor = contactdb.cursor()

# SQL that tests and creates table
tableCreation = """CREATE TABLE IF NOT EXISTS contacts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    middle_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    email TEXT)"""
dbcursor.execute(tableCreation)

class listbox(ttk.Treeview):
    def __init__(self, dbcursor: sql.Cursor, contactWindow: "function", master = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.dbcursor = dbcursor
        self.heading("#0", text="")
        self.heading("name", text="Name")
        self.heading("number", text="Phone Number")
        self.heading("email", text="Email Address")
        self.bind("<Double-1>", lambda e: contactWindow(self.item(self.selection()[0], "tags")))
        self.imageList = []
        self.grid()

    def updateContacts(self, firstName="", middleName="", lastName="", number="", email=""):
        self.clear()
        query =  """ SELECT * FROM contacts
                    WHERE first_name LIKE ? 
                        AND middle_name LIKE ?
                        AND last_name LIKE ?
                        AND phone LIKE ? 
                        AND email LIKE ? """

        info = (f"%{firstName}%", f"%{middleName}%", f"%{lastName}%", f"%{number}%", f"%{email}%")

        results = self.dbcursor.execute(query, info)
        results = results.fetchall()

        for contact in results:
            contact = list(contact)
            fullName = f"{contact[1]} {contact[2]} {contact[3]}"
            del contact[1:4]
            contact.insert(1, fullName)
            image = tk.PhotoImage(file="./images/blank_person.png")
            image = image.subsample(4)
            self.imageList.append(image)
            self.insert("", ["end"], values=contact[1:], image=image, tags=contact[0])
        self.update()

    def clear(self):
        for child in self.get_children():
            self.delete(child)
        self.imageList.clear()


class newWindow(tk.Toplevel):
    def __init__(self, id: int, master = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.id = id

        query = """ SELECT * FROM contacts WHERE id = ? """
        contact = dbcursor.execute(query, (id))
        contact = contact.fetchall()
        contact = contact[0]
        formatedName = f"{contact[1]} {contact[3]}"
        self.title(formatedName)

        photoImage = ttk.Label(self, image=contactImage)
        frame = ttk.Frame(self, padding=framePadding)
        firstLabel = ttk.Label(frame, text="First:")
        middleLabel = ttk.Label(frame, text="Middle:")
        lastLabel = ttk.Label(frame, text="Last:")
        fullNameLabel = ttk.Label(frame, text="Full Name:")
        firstName = ttk.Label(frame, text=contact[1])
        middleName = ttk.Label(frame, text=contact[2])
        lastName = ttk.Label(frame, text=contact[3])
        fullName = ttk.Label(frame, text=formatedName)

        # Grid
        photoImage.grid(column=0, row=0)
        frame.grid(column=1, row=0)
        firstLabel.grid(column=0, row=0)
        middleLabel.grid(column=0, row=1)
        lastLabel.grid(column=0, row=2)
        fullNameLabel.grid(column=0, row=3)
        firstName.grid(column=1, row=0)
        middleName.grid(column=1, row=1)
        lastName.grid(column=1, row=2)
        fullName.grid(column=1, row=3)


root = tk.Tk()
root.title("Phonebook")
root.iconphoto(True, tk.PhotoImage(file="./images/phonebook.png"))
contactImage = tk.PhotoImage(file="./images/blank_person.png")
imageList = []

style = ttk.Style()
style.configure("Treeview", rowheight=60)

def addContact() -> None:
    query = """ INSERT INTO contacts (first_name, middle_name, last_name, phone, email)
                             VALUES (?, ?, ?, ?, ?) """
    dbcursor.execute(query,\
         (firstName.get(), middleName.get(), lastName.get(), number.get(), email.get()))
    contactdb.commit()
    contactList.updateContacts()
    
def deleteContact() -> None:
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE first_name = ?", (firstName.get(), ))
    contactdb.commit()
    contactList.updateContacts()

def getInput() -> list:
    return [firstName.get(), middleName.get(), lastName.get(), number.get(), email.get()]

def contactWindow(id: int):
    query = """ SELECT * FROM contacts WHERE id = ? """
    contact = dbcursor.execute(query, (id))
    contact = contact.fetchall()
    contact = contact[0]

    newWindow = tk.Toplevel(root)
    newWindow.title(contact[1])

    frame = ttk.Frame(newWindow, padding=framePadding)
    photoImage = ttk.Label(frame, image=contactImage)
    firstName = ttk.Label(frame, text="first")
    middleName = ttk.Label(frame, text="middle")
    lastName = ttk.Label(frame, text="last")
    # fullName = ttk.Label(frame, text=contactInfo[1])

    # Grid info
    frame.grid()
    photoImage.grid(sticky="e")
    firstName.grid()
    middleName.grid()
    lastName.grid()
    # fullName.grid()

def createWindow(id: int):
    contactWindow = newWindow(id)

menubar = tk.Menu(root)
root["menu"] = menubar
menubar.add_command(label="Home", command=contactWindow)
menubar.add_command(label="Add", command=lambda: createWindow(0))
menubar.add_command(label="Settings", command=contactWindow)

# Variables
firstName = tk.StringVar()
middleName = tk.StringVar()
lastName = tk.StringVar()
number = tk.StringVar()
email = tk.StringVar()
listForTable = tk.StringVar()
lastQuery = []
framePadding = 20
borderwidth = 5

# Menu for listing, searching, adding, and deleting contacts
menu = ttk.Frame(root, padding=framePadding, borderwidth=borderwidth, relief="raised")

firstNameEntry = ttk.Entry(menu, textvariable=firstName)
firstNameLabel = ttk.Label(menu, text="First name: ")
middleNameEntry = ttk.Entry(menu, textvariable=middleName)
middleNameLabel = ttk.Label(menu, text="Middle name: ")
lastNameEntry = ttk.Entry(menu, textvariable=lastName)
lastNameLabel = ttk.Label(menu, text="Last name: ")
numberEntry = ttk.Entry(menu, textvariable=number)
numberLabel = ttk.Label(menu, text="Phone Number:")
emailEntry = ttk.Entry(menu, textvariable=email)
emailLabel = ttk.Label(menu, text="Email Address:")

listButton = ttk.Button(menu, text="List all", command=lambda: contactList.updateContacts())
searchButton = ttk.Button(menu, text="Search", command=lambda: contactList.updateContacts(*getInput()))
addButton = ttk.Button(menu, text="Add Contact", command=lambda: addContact())
deleteButton = ttk.Button(menu, text="Delete Contact", command=lambda: deleteContact())

# Search result table
content = ttk.Frame(root, padding=framePadding)
contactList = listbox(dbcursor, createWindow, content, columns=["name","number","email"], height=8)

# Grid info - Menu
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.configure(padx=framePadding/2, pady=framePadding/2)

menu.grid(column=1, row=0)
firstNameLabel.grid(column=0, row=0)
middleNameLabel.grid(column=0, row=1)
lastNameLabel.grid(column=0, row=2)
numberLabel.grid(column=0, row=3)
emailLabel.grid(column=0, row=4)

firstNameEntry.grid(column=1, row=0)
middleNameEntry.grid(column=1, row=1)
lastNameEntry.grid(column=1, row=2)
numberEntry.grid(column=1, row=3)
emailEntry.grid(column=1, row=4)

addButton.grid(column=2, row=0)
deleteButton.grid(column=2, row=1)
searchButton.grid(column=2, row=2)
listButton.grid(column=2, row=3)

content.grid(column=0, row=0)

# Setting up listbox
contactList.updateContacts()

# GUI Startpoint
root.mainloop()

contactdb.commit()
contactdb.close()

# TODO add column for more data function, make presentation prettier, etc.

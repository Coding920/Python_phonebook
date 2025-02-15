#This is a phonebook that allows easy access to a DB

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

root = tk.Tk()
root.title("Phonebook")
root.iconphoto(True, tk.PhotoImage(file="./images/phonebook.png"))
contactImage = tk.PhotoImage(file="./images/blank_person.png")

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

listButton = ttk.Button(menu, text="List all", command=lambda:\
                         (getContacts("","","","",""), updateTable()))
searchButton = ttk.Button(menu, text="Search", command=lambda: \
    (getContacts(firstName.get(), middleName.get(), lastName.get(), number.get(), email.get())\
                                                                              , updateTable()))
addButton = ttk.Button(menu, text="Add Contact", command=lambda: addContact())
deleteButton = ttk.Button(menu, text="Delete Contact", command=lambda: deleteContact())

# Search result table
content = ttk.Frame(root, padding=framePadding)
table = tk.Listbox(content, height=8, listvariable=listForTable, width=100)
table.bind("<Double-1>", lambda _: contactWindow(table.get(table.curselection())))
scroll = tk.Scrollbar(content, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scroll.set)

# Grid info 
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
table.grid(column=0, row=0) 
scroll.grid(column=1, row=0, sticky="NS")


def addContact():
    query = """ INSERT INTO contacts (first_name, middle_name, last_name, phone, email)
                             VALUES (?, ?, ?, ?, ?) """
    dbcursor.execute(query,\
         (firstName.get(), middleName.get(), lastName.get(), number.get(), email.get()))
    contactdb.commit()
    getContacts("","","","","")
    updateTable()
    
def deleteContact():
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE first_name = ?", (firstName.get(), ))
    contactdb.commit()
    getContacts("","","","","")
    updateTable()
    
def getContacts(firstName, middleName, lastName, number, email):
    query =  """ SELECT * FROM contacts 
                  WHERE first_name LIKE ? 
                    AND middle_name LIKE ?
                    AND last_name LIKE ?
                    AND phone LIKE ? 
                    AND email LIKE ? """

    global lastQuery; lastQuery = dbcursor.execute(query,\
                (f"%{firstName}%", f"%{middleName}%", f"%{lastName}%", f"%{number}%", f"%{email}%"))
    lastQuery = lastQuery.fetchall()

def updateTable():
    nameList = []
    for contact in lastQuery:
       nameList.append(contact[1])

    listForTable.set(value=nameList)
    table.update()

def contactWindow(firstName):
    newWindow = tk.Toplevel(root)
    newWindow.title(firstName)
    newWindow.grid()
    getContacts(firstName,"","","","")
    contactInfo = lastQuery[0]
    frame = ttk.Frame(newWindow, padding=framePadding)
    photoImage = ttk.Label(frame, image=contactImage)
    firstName = ttk.Label(frame, text="first")
    middleName = ttk.Label(frame, text="middle")
    lastName = ttk.Label(frame, text="last")
    fullName = ttk.Label(frame, text=contactInfo[1])

    # Grid info
    frame.grid()
    photoImage.grid(sticky="e")
    firstName.grid()
    middleName.grid()
    lastName.grid()
    fullName.grid()
    
# Setting up listbox
getContacts("","","","","")
updateTable()

# GUI Startpoint
root.mainloop()

contactdb.commit()
contactdb.close()
# End Code

# TODO add column for more data function, make presentation prettier, etc.

# def pageSwitch(index):
#     # Clearing things
#     for page in pages:
#         page.grid_forget()
#     for label in listOfConInfo:
#         label.destroy()
#     for var in stringvars:
#         var.set(value = "")
#     pages[index].grid(sticky="nsew")

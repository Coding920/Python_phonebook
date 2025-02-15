#This is a phonebook that allows easy access to a DB

import sqlite3 as sql
import tkinter as tk 
from tkinter import ttk

# DB Setup
contactdb = sql.connect("contacts.db")
dbcursor = contactdb.cursor()

# SQL that tests and creates table
tableCreation = """CREATE TABLE IF NOT EXISTS contacts(
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    notes TEXT)"""
dbcursor.execute(tableCreation)

root = tk.Tk()
root.title("Phonebook")
root.iconphoto(True, tk.PhotoImage(file="./images/phonebook.png"))
contactImage = tk.PhotoImage(file="./images/blank_person.png")

# Variables
name = tk.StringVar()
number = tk.StringVar()
email = tk.StringVar()
notes = tk.StringVar()
listForTable = tk.StringVar()
lastQuery = []
framePadding = 20
borderwidth = 5
# *100 to bring MS in Seconds with first int having the first place being in tenths of seconds
sleepTime = 15 * 100

# Menu for listing, searching, adding, and deleting contacts
menu = ttk.Frame(root, padding=framePadding, borderwidth=borderwidth, relief="raised")

nameEntry = ttk.Entry(menu, textvariable=name)
nameLabel = ttk.Label(menu, text="Name: ")
numberEntry = ttk.Entry(menu, textvariable=number)
numberLabel = ttk.Label(menu, text="Phone Number:")
emailEntry = ttk.Entry(menu, textvariable=email)
emailLabel = ttk.Label(menu, text="Email Address:")
notesEntry = ttk.Entry(menu, textvariable=notes)
notesLabel = ttk.Label(menu, text="Notes: ")

listButton = ttk.Button(menu, text="List all", command=lambda:\
                         [getContacts("","",""), updateTable()])
searchButton = ttk.Button(menu, text="Search", command=lambda: \
                           (getContacts(name.get(), number.get(), email.get()), updateTable()))
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
nameLabel.grid(column=0, row=0)
numberLabel.grid(column=0, row=1)
emailLabel.grid(column=0, row=2)
notesLabel.grid(column=0, row=3)

nameEntry.grid(column=1, row=0)
numberEntry.grid(column=1, row=1)
emailEntry.grid(column=1, row=2)
notesEntry.grid(column=1, row=3)

addButton.grid(column=2, row=0)
deleteButton.grid(column=2, row=1)
searchButton.grid(column=2, row=2)
listButton.grid(column=2, row=3)


content.grid(column=0, row=0)
table.grid(column=0, row=0) 
scroll.grid(column=1, row=0, sticky="NS")


def addContact():
    dbcursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)",\
                      (name.get(), number.get(), email.get(), notes.get()))
    contactdb.commit()
    getContacts("","","")
    updateTable()
    
def deleteContact():
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE name = ?", (name.get(), ))
    contactdb.commit()
    getContacts("","","")
    updateTable()
    
def getContacts(name, number, email):
    # If left blank, turn into a wildcard character
    if name == "":
        name = "%"
    if number == "":
        number = "%"
    if email == "":
        email = "%"

    global lastQuery; lastQuery = dbcursor.execute(""" SELECT * FROM contacts 
                                    WHERE name LIKE ? AND phone LIKE ? AND email LIKE ? """,\
                                          (f"%{name}%", f"%{number}%", f"%{email}%"))
    lastQuery = lastQuery.fetchall()

def updateTable():
    nameList = []
    for contact in lastQuery:
       nameList.append(contact[0])

    listForTable.set(value=nameList)
    table.update()

def contactWindow(name):
    newWindow = tk.Toplevel(root)
    newWindow.title(name)
    newWindow.grid()
    getContacts(name, "", "")
    contactInfo = lastQuery[0]
    frame = ttk.Frame(newWindow, padding=framePadding)
    photoImage = ttk.Label(frame, image=contactImage)
    firstName = ttk.Label(frame, text="first")
    middleName = ttk.Label(frame, text="middle")
    lastName = ttk.Label(frame, text="last")
    fullName = ttk.Label(frame, text=contactInfo[0])

    # Grid info
    frame.grid()
    photoImage.grid(sticky="e")
    firstName.grid()
    middleName.grid()
    lastName.grid()
    fullName.grid()
    
# Setting up listbox
getContacts("","","")
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

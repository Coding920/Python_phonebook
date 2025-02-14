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
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Variables
name = tk.StringVar()
number = tk.StringVar()
email = tk.StringVar()
notes = tk.StringVar()
framePadding = 20
sleeptime = 15 * 100 # *100 to bring MS in Seconds with first int having the first place being in tenths of seconds

# Menu for listing, searching, adding, and deleting contacts
menu = ttk.Frame(root, padding=framePadding)

nameEntry = ttk.Entry(menu, textvariable=name)
nameLabel = ttk.Label(menu, text="Name: ")
numberEntry = ttk.Entry(menu, textvariable=number)
numberLabel = ttk.Label(menu, text="Phone Number:")
emailEntry = ttk.Entry(menu, textvariable=email)
emailLabel = ttk.Label(menu, text="Email Address:")
notesEntry = ttk.Entry(menu, textvariable=notes)
notesLabel = ttk.Label(menu, text="Notes: ")

listButton = ttk.Button(menu, text="List all", command=lambda: displayContacts("","",""))
searchButton = ttk.Button(menu, text="Search", command=lambda: displayContacts(name.get(), number.get(), email.get()))
addButton = ttk.Button(menu, text="Add Contact", command=lambda: addContact())
deleteButton = ttk.Button(menu, text="Delete Contact", command=lambda: deleteContact())

# Search result table
content = ttk.Frame(root, padding=framePadding)
listForTable = tk.StringVar(value=dbcursor.execute(""" SELECT * FROM contacts """).fetchall())
table = tk.Listbox(content, height=8, listvariable=listForTable, width=100)
table.bind("<Double-1>", lambda _: contactWindow())
scroll = tk.Scrollbar(content, orient="vertical", command=table.yview)
table.configure(yscrollcommand=scroll.set)

# Grid info 
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
    dbcursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (name.get(), number.get(), email.get(), notes.get()))
    contactdb.commit()
    
def deleteContact():
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE name = ?", (name.get(), ))
    contactdb.commit()
    
def displayContacts(name, number, email):
    # If left blank, turn to any character, Which works only with like
    if name == "":
        name = "%"
    if number == "":
        number = "%"
    if email == "":
        email = "%"

    searchQuery = f"""SELECT * FROM contacts WHERE name LIKE ? AND phone LIKE ? AND email LIKE ?"""
    
    searchResult = dbcursor.execute(searchQuery, (f"%{name}%", f"%{number}%", f"%{email}%"))
    listForTable.set(value=searchResult.fetchall())
    table.update()

def contactWindow():
    contactWindow = tk.Toplevel(root)
    contactWindow.title("Set name of contact here")

# GUI Startpoint
root.mainloop()

contactdb.commit()
contactdb.close()
# End Code 


# TODO add column for more data function, make presentation prettier, etc.

# def editContact():
#     # TODO FIX currently doesn't work
#     nameIndex = input("Who's contact would you like to change? ")
#     name = input("New name: ")
#     phone = input("New phone: ")
#     email = input("New email: ")
#     notes = input("New notes: ")

#     dbcursor.execute("UPDATE contacts SET name=?, phone=?, email=?, notes=? WHERE name=?", (name, phone, email, notes, nameIndex))
#     contactdb.commit()

# def pageSwitch(index):
#     # Clearing things
#     for page in pages:
#         page.grid_forget()
#     for label in listOfConInfo:
#         label.destroy()
#     for var in stringvars:
#         var.set(value = "")
#     pages[index].grid(sticky="nsew")

# responseLabel.configure(text="Contact Added!")
# responseLabel.update()
# menu.after(sleeptime, lambda: responseLabel.configure(text=""))
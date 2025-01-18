#This is a phonebook that allows easy access to a DB

import sqlite3 as sql
import tkinter as tk 
from tkinter import ttk

# GUI Setup
root = tk.Tk()
root.title("Phonebook")
# root.wm_iconphoto() Mess with for new window icon in top left

# Variables
name = tk.StringVar()
number = tk.StringVar()
email = tk.StringVar()
notes = tk.StringVar()
stringvars = [name, number, email, notes]
framePadding = 20
sleeptime = 15 * 100 # *100 to bring MS in Seconds with first int having the first place being in tenths of seconds

# Main Menu
fMainMenu = ttk.Frame(root, padding=framePadding)

mainLabel = ttk.Label(fMainMenu, text="Hello, What would you like to do today?")
EntryAndDeletion = ttk.Button(fMainMenu, text="Contact Entry and Deletion", command=lambda: pageSwitch(pages.index(fCreateDelete)))
displayAndSearch = ttk.Button(fMainMenu, text="List and Search Contacts", command=lambda: pageSwitch(pages.index(fDisplay)))

mainLabel.grid(row=0)
EntryAndDeletion.grid(row=1)
displayAndSearch.grid(row=2)
fMainMenu.pack(expand=True, anchor="n")

# Creation and Deletion page
fCreateDelete = ttk.Frame(root, padding=framePadding)

addNameEntry = ttk.Entry(fCreateDelete, textvariable=name)
addNameLabel = ttk.Label(fCreateDelete, text="Name: ")
addNumberEntry = ttk.Entry(fCreateDelete, textvariable=number)
addNumberLabel = ttk.Label(fCreateDelete, text="Phone Number:")
addEmailEntry = ttk.Entry(fCreateDelete, textvariable=email)
addEmailLabel = ttk.Label(fCreateDelete, text="Email Address:")
addNotesEntry = ttk.Entry(fCreateDelete, textvariable=notes)
addNotesLabel = ttk.Label(fCreateDelete, text="Notes: ")

responseLabel = ttk.Label(fCreateDelete, text="")
addButton = ttk.Button(fCreateDelete, text="Add Contact", command=lambda: addContact())
deleteButton = ttk.Button(fCreateDelete, text="Delete Contact", command=lambda: deleteContact())
addBackButton = ttk.Button(fCreateDelete, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))

# Grid info 
addNameLabel.grid(column=0, row=0)
addNumberLabel.grid(column=0, row=1)
addEmailLabel.grid(column=0, row=2)
addNotesLabel.grid(column=0, row=3)
addNameEntry.grid(column=1, row=0)
addNumberEntry.grid(column=1, row=1)
addEmailEntry.grid(column=1, row=2)
addNotesEntry.grid(column=1, row=3)

responseLabel.grid(row=2, column=2)
addButton.grid(column=2, row=0)
deleteButton.grid(column=2, row=1)
addBackButton.grid(column=2, row=3)

# Display and Search Page

fDisplay = ttk.Frame(root, padding=framePadding)

searchNameEntry = ttk.Entry(fDisplay, textvariable=name)
searchNameLabel = ttk.Label(fDisplay, text="Name: ")
searchNumberEntry = ttk.Entry(fDisplay, textvariable=number)
searchNumberLabel = ttk.Label(fDisplay, text="Phone Number:")
searchEmailEntry = ttk.Entry(fDisplay, textvariable=email)
searchEmailLabel = ttk.Label(fDisplay, text="Email Address:")
searchBackButton = ttk.Button(fDisplay, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))
searchButton = ttk.Button(fDisplay, text="Search", command=lambda: displayContacts(name.get(), number.get(), email.get()))
fSearchResult = ttk.Frame(fDisplay, padding=framePadding)
listOfConInfo = []

# Grid info
searchNameLabel.grid(column=0, row=0)
searchNameEntry.grid(column=1, row=0)
searchNumberLabel.grid(column=0, row=1)
searchNumberEntry.grid(column=1, row=1)
searchEmailLabel.grid(column=0, row=2)
searchEmailEntry.grid(column=1, row=2)
searchButton.grid(column=2, row=1)
searchBackButton.grid(column=2, row=3)
fSearchResult.grid(column=0, row=4, columnspan=4)

pages = [fMainMenu, fCreateDelete, fDisplay]

def addContact():
    dbcursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (name.get(), number.get(), email.get(), notes.get()))
    contactdb.commit()

    responseLabel.configure(text="Contact Added!")
    responseLabel.update()
    fCreateDelete.after(sleeptime, lambda: responseLabel.configure(text=""))
    
def deleteContact():
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE name = ?", (name.get(), ))
    contactdb.commit()

    responseLabel.configure(text="Contact Deleted!")
    responseLabel.update()
    fCreateDelete.after(sleeptime, lambda: responseLabel.configure(text=""))
    
def displayContacts(name, number, email):
    # TODO Add search sorting functions, search by other columns
    for label in listOfConInfo:
        label.destroy()

    # If left blank, turn to any character, Which works only with like
    if name == "":
        name = "%"
    if number == "":
        number = "%"
    if email == "":
        email = "%"

    searchQuery = f"""SELECT * FROM contacts WHERE name LIKE ? AND phone LIKE ? AND email LIKE ?"""
    
    searchResult = dbcursor.execute(searchQuery, (name, number, email))
    results = searchResult.fetchall()

    if results == []:
        label = ttk.Label(fSearchResult, text="No results found")
        fDisplay.after(sleeptime, lambda: label.destroy())
    else:
        for idx, contact in enumerate(results):
            for idx2, info in enumerate(contact):
                label = ttk.Label(fSearchResult, text=info)
                label.grid(column=idx2, row=idx)
                listOfConInfo.append(label)

def editContact():
    # TODO FIX currently doesn't work
    nameIndex = input("Who's contact would you like to change? ")
    name = input("New name: ")
    phone = input("New phone: ")
    email = input("New email: ")
    notes = input("New notes: ")

    dbcursor.execute("UPDATE contacts SET name=?, phone=?, email=?, notes=? WHERE name=?", (name, phone, email, notes, nameIndex))
    contactdb.commit()

def pageSwitch(index):
    # Clearing things
    for page in pages:
        page.pack_forget()
    for label in listOfConInfo:
        label.destroy()
    for var in stringvars:
        var.set(value = "")

    pages[index].pack(expand=True, anchor="n")

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

# GUI Startpoint
root.mainloop()

contactdb.commit()
contactdb.close()
# TODO add column for more data function, make presentation prettier, etc.

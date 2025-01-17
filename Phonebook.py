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
addButton = ttk.Button(fMainMenu, text="Add contact", command=lambda: pageSwitch(pages.index(fAdd)))
delButton = ttk.Button(fMainMenu, text="Delete contact", command=lambda: pageSwitch(pages.index(fDelete)))
listButton = ttk.Button(fMainMenu, text="List contacts", command=lambda: pageSwitch(pages.index(fList)))
searchButton = ttk.Button(fMainMenu, text="Search contacts", command=lambda: pageSwitch(pages.index(fSearch)))
editButton = ttk.Button(fMainMenu, text="Edit contact", command=None)

mainLabel.grid(row=0, sticky="NS")
addButton.grid(row=1, sticky="NS")
delButton.grid(row=2, sticky="NS")
listButton.grid(row=3, sticky="NS")
searchButton.grid(row=4, sticky="NS")
editButton.grid(row=5, sticky="NS")
fMainMenu.pack(expand=1)

# Add page
fAdd = ttk.Frame(root, padding=framePadding)

addNameEntry = ttk.Entry(fAdd, textvariable=name)
addNameLabel = ttk.Label(fAdd, text="Name: ")
addNumberEntry = ttk.Entry(fAdd, textvariable=number)
addNumberLabel = ttk.Label(fAdd, text="Phone Number:")
addEmailEntry = ttk.Entry(fAdd, textvariable=email)
addEmailLabel = ttk.Label(fAdd, text="Email Address:")
addNotesEntry = ttk.Entry(fAdd, textvariable=notes)
addNotesLabel = ttk.Label(fAdd, text="Notes: ")
addConfirmButton = ttk.Button(fAdd, text="Add Contact", command=lambda: addContact())
deleteButton = ttk.Button(fAdd, text="Delete Contact", command=lambda: deleteContact())
addBackButton = ttk.Button(fAdd, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))

addNameLabel.grid(column=0, row=0)
addNumberLabel.grid(column=0, row=1)
addEmailLabel.grid(column=0, row=2)
addNotesLabel.grid(column=0, row=3)
addNameEntry.grid(column=1, row=0)
addNumberEntry.grid(column=1, row=1)
addEmailEntry.grid(column=1, row=2)
addNotesEntry.grid(column=1, row=3)
addConfirmButton.grid(column=2, row=0)
deleteButton.grid(column=2, row=1)
addBackButton.grid(column=2, row=3)

# Delete Page
fDelete = ttk.Frame(root, padding=framePadding)

delNameEntry = ttk.Entry(fDelete, textvariable=name)
delConfirmButton = ttk.Button(fDelete, text="Delete Contact", command=lambda: deleteContact())
delBackButton = ttk.Button(fDelete, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))

delNameEntry.grid(row=0, column=0, rowspan=2)
delConfirmButton.grid(row=0, column=1)
delBackButton.grid(row=2, column=1)

# List Page

fList = ttk.Frame(root, padding=framePadding)

listBackButton = ttk.Button(fList, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))
listBackButton.grid(column=0, row=0)
listListerButton = ttk.Button(fList, text="List Contacts", command=lambda: listContacts())
listListerButton.grid(column=0, row=1)
fListResponseTable = ttk.Frame(fList, padding=framePadding)
fListResponseTable.grid(column=0, row=2, columnspan=4)
listResponseLabel = []

# Search Page

fSearch = ttk.Frame(root, padding=framePadding)

searchNameEntry = ttk.Entry(fSearch, textvariable=name)
searchNameLabel = ttk.Label(fSearch, text="Name: ")
searchNumberEntry = ttk.Entry(fSearch, textvariable=number)
searchNumberLabel = ttk.Label(fSearch, text="Phone Number:")
searchEmailEntry = ttk.Entry(fSearch, textvariable=email)
searchEmailLabel = ttk.Label(fSearch, text="Email Address:")
searchBackButton = ttk.Button(fSearch, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))
searchButton = ttk.Button(fSearch, text="Search", command=lambda: searchContacts(name.get(), number.get(), email.get()))
fSearchResult = ttk.Frame(fSearch, padding=framePadding)

searchNameLabel.grid(column=0, row=0)
searchNameEntry.grid(column=1, row=0)
searchNumberLabel.grid(column=0, row=1)
searchNumberEntry.grid(column=1, row=1)
searchEmailLabel.grid(column=0, row=2)
searchEmailEntry.grid(column=1, row=2)
searchButton.grid(column=2, row=1)
searchBackButton.grid(column=2, row=3)
fSearchResult.grid(column=0, row=4, columnspan=4)
searchResultLabel = ttk.Label(fSearchResult, text="")

pages = [fMainMenu, fAdd, fDelete, fList, fSearch]

def addContact():
    dbcursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (name.get(), number.get(), email.get(), notes.get()))
    contactdb.commit()
    
    addResponseLabel = ttk.Label(fAdd, text="Contact Added!")
    addResponseLabel.grid(row=2, column=2)
    fAdd.after(sleeptime, lambda: addResponseLabel.grid_forget())
    
def listContacts():
    # TODO Add functionality to sort and filter items
    fListResponseTable.grid(column=0, row=2)
    wholeTable = dbcursor.execute("SELECT * FROM contacts").fetchall()
    for index, contact in enumerate(wholeTable):
        for listIndex, item in enumerate(wholeTable[index]):
            displayableContact = [*wholeTable[index]]
            
            contactInfo = ttk.Label(fListResponseTable, text=displayableContact[listIndex])
            contactInfo.grid(column=listIndex, row=index)
            listResponseLabel.append(contactInfo)

def searchContacts(name, number, email):
    # TODO Add search sorting functions, search by other columns
    # If left blank, turn to any character, Which works only with like
    if name == "":
        name = "%"
    if number == "":
        number = "%"
    if email == "":
        email = "%"

    searchQuery = f"""SELECT * FROM contacts WHERE name LIKE ? AND phone LIKE ? AND email LIKE ?"""
    
    searchResult = dbcursor.execute(searchQuery, (name, number, email))
    results = searchResult.fetchone()
    
    if results == None:
        searchResultLabel.configure(text="No Results")
        searchResultLabel.update()    
    else:
        searchResultLabel.configure(text=results)
        searchResultLabel.update()

    searchResultLabel.grid(column=0, row=0)

def deleteContact():
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE name = ?", (name.get(), ))
    contactdb.commit()
     
    delResponseLabel = ttk.Label(fAdd, text="Contact deleted!")
    delResponseLabel.grid(column=2, row=2)
    fDelete.after(sleeptime, lambda: delResponseLabel.grid_forget())

def editContact():
    # TODO FIX currently doesn't work
    nameIndex = input("Who's contact would you like to change? ")
    name = input("New name: ")
    phone = input("New phone: ")
    email = input("New email: ")
    notes = input("New notes: ")

    dbcursor.execute("UPDATE contacts SET name=?, phone=?, email=?, notes=? WHERE name=?", (name, phone, email, notes, nameIndex))
    contactdb.commit()

def save():
    # TODO Determine if save function is neccesary, and how to better implement it 
    contactdb.commit()
    dbcursor.close()

def pageSwitch(index):
    for page in pages:
        page.pack_forget()
    fListResponseTable.grid_forget()
    for label in listResponseLabel:
        label.destroy() 
    for var in stringvars:
        var.set(value = "")

    pages[index].pack(expand=1)

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

contactdb.close()
# TODO add column for more data function, make presentation prettier, etc.

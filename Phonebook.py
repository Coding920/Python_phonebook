#This is a phonebook program 

import sqlite3 as sql
import tkinter as tk 
from tkinter import ttk

# GUI Setup
root = tk.Tk()
root.title("Phonebook")

# Variables
name = tk.StringVar()
number = tk.StringVar()
email = tk.StringVar()
notes = tk.StringVar()
framePadding = 20
sleeptime = 10 * 100 # *100 to bring MS in Seconds with first int having the first place being in tenths of seconds

# Main Menu
fMainMenu = ttk.Frame(root, padding=framePadding)

mainLabel = ttk.Label(fMainMenu, text="Hello, What would you like to do today?")
addButton = ttk.Button(fMainMenu, text="Add contact", command=lambda: pageSwitch(pages.index(fAdd)))
delButton = ttk.Button(fMainMenu, text="Delete contact", command=lambda: pageSwitch(pages.index(fDelete)))
listButton = ttk.Button(fMainMenu, text="List contacts", command=lambda: pageSwitch(pages.index(fList)))
searchButton = ttk.Button(fMainMenu, text="Search contacts", command=None)
editButton = ttk.Button(fMainMenu, text="Edit contact", command=None)

mainLabel.grid(row=0)
addButton.grid(row=1)
delButton.grid(row=2)
listButton.grid(row=3)
searchButton.grid(row=4)
editButton.grid(row=5)
fMainMenu.pack(expand=1)

# Add page
fAdd = ttk.Frame(root, padding=framePadding)

addNameEntry = ttk.Entry(fAdd, textvariable=name)
addNumberEntry = ttk.Entry(fAdd, textvariable=number)
addEmailEntry = ttk.Entry(fAdd, textvariable=email)
addNotesEntry = ttk.Entry(fAdd, textvariable=notes)
addConfirmButton = ttk.Button(fAdd, text="Add Contact", command=lambda: addContact())
addBackButton = ttk.Button(fAdd, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))

addNameEntry.grid(column=0, row=0)
addNameEntry.insert(index=0, string="Name")
addNumberEntry.grid(column=0, row=1)
addNumberEntry.insert(index=1, string="Number")
addEmailEntry.grid(column=0, row=2)
addEmailEntry.insert(index=2, string="Email")
addNotesEntry.grid(column=0, row=3)
addNotesEntry.insert(index=3, string="Notes")
addConfirmButton.grid(column=1, row=0)
addBackButton.grid(column=1, row=3)

# Delete Page
fDelete = ttk.Frame(root, padding=framePadding)

delNameEntry = ttk.Entry(fDelete, textvariable=name)
delConfirmButton = ttk.Button(fDelete, text="Delete Contact", command=lambda: deleteContact())
delBackButton = ttk.Button(fDelete, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))

delNameEntry.grid(row=0, column=0, rowspan=2)
delNameEntry.insert(index=4, string="Name")
delConfirmButton.grid(row=0, column=1)
delBackButton.grid(row=2, column=1)

# List Page

fList = ttk.Frame(root, padding=framePadding)

listBackButton = ttk.Button(fList, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))
listBackButton.grid(column=0, row=0)
listListerButton = ttk.Button(fList, text="List Contacts", command=lambda: listContacts())
listListerButton.grid(column=0, row=1)
fListResponseTable = ttk.Frame(fList, padding=framePadding)
fListResponseTable.grid(column=0, row=2)

pages = [fMainMenu, fAdd, fDelete, fList]

def addContact():
    dbcursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (name.get(), number.get(), email.get(), notes.get()))
    contactdb.commit()
    
    addResponseLabel = ttk.Label(fAdd, text="Contact Added!")
    addResponseLabel.grid(row=2, column=1)
    fAdd.after(sleeptime, lambda: addResponseLabel.grid_forget())
    
def listContacts():
    # TODO Add functionality to sort and filter items
    wholeTable = dbcursor.execute("SELECT * FROM contacts").fetchall()
    for index, contact in enumerate(wholeTable):
        for listIndex, item in enumerate(wholeTable[index]):
            displayableContact = [*wholeTable[index]]
            print(displayableContact[listIndex], end="\t")

            listResponseLabel = []
            listResponseLabel[index][listIndex] = ttk.Label(fListResponseTable, text=f"{displayableContact[listIndex]}")
            listResponseLabel[index][listIndex].grid(column=listIndex, row=index + 2)
        print()
        while fList:
            pass

def searchContacts():
    # TODO Add search sorting functions, search by other columns
    name = input("Who would you like to search for? ")

    searchResult = dbcursor.execute("SELECT * FROM contacts WHERE Name = ?", (name, ))
    results = searchResult.fetchone()
    
    if results == None:
        print("Couldn't find any contacts by that name")
    else:
        contactDisplayer(*results).displayer()

def deleteContact():
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE Name = ?", (name.get(), ))
    contactdb.commit()
     
    delResponseLabel = ttk.Label(fDelete, text="Contact deleted!")
    delResponseLabel.grid(column=1, row=1)
    fDelete.after(sleeptime, lambda: delResponseLabel.grid_forget())

def editContact():
    # TODO FIX currently doesn't work
    nameIndex = input("Who's contact would you like to change? ")
    name = input("New name: ")
    phone = input("New phone: ")
    email = input("New email: ")
    notes = input("New notes: ")

    dbcursor.execute("UPDATE contacts SET Name=?, Phone=?, Email=?, Notes=? WHERE Name=?", (name, phone, email, notes, nameIndex))
    contactdb.commit()

def save():
    # TODO Determine if save function is neccesary, and how to better implement it 
    contactdb.commit()
    dbcursor.close()

def pageSwitch(index):
    for page in pages:
        page.pack_forget()
    fListResponseTable.grid_forget()

    pages[index].pack(expand=1)

# DB Setup
contactdb = sql.connect("contacts.db")
dbcursor = contactdb.cursor()

# SQL entry that tests and creates table
tableCreation = """CREATE TABLE IF NOT EXISTS contacts(
                    Name TEXT,
                    Phone TEXT,
                    Email TEXT,
                    Notes TEXT)"""
dbcursor.execute(tableCreation)

# /DB Setup

# GUI Startpoint
root.mainloop()
# TODO add column for more data function, make presentation prettier, etc.







# Old CLI menu

# Menu and prompts

# print("Hello!", end=' ')

# def main():
    
#     while True:
#             print()
#             choice = input("Add or delete a contact (add/del), edit a contact (edit), list contacts (list), search contacts (search), quit (q): ")
#             print()

#             match choice.lower():
#                 case "add":
#                     add()

#                 case "edit":
#                     edit()
               
#                 case "del":
#                     delete()

#                 case "list":
#                     lister()

#                 case "search":
#                     search()

#                 case "quit" | "q":
#                     save()
#                     break
# main()
# 
# Also Phased out contact displayer
# class contactDisplayer:
#     def __init__(self, name, phone, email, notes):
#         self.name = name
#         self.phone = phone
#         self.email = email
#         self.notes = notes
#         pass

#     def displayer(self):
#         print(f"Name: {self.name}, Phone number: {self.phone}, Email: {self.email}, Notes: {self.notes}")
#         pass
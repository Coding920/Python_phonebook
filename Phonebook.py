#This is a phonebook program 

import sqlite3 as sql
import tkinter as tk 
from tkinter import ttk

class GUI():
    def __init__(self):
                        
        def pageSwitch(index):
            for page in pages:
                page.grid_forget()

                pages[index].grid()

        # GUI Setup
        root = tk.Tk()
        root.title("Phonebook")

        # Regularly Reused Variables
        name = None
        number = None
        email = None
        notes = None
        
        # Main Menu
        fMainMenu = ttk.Frame(root, padding=20)

        mainLabel = ttk.Label(fMainMenu, text="Hello, What would you like to do today?")
        addButton = ttk.Button(fMainMenu, text="Add contact", command=lambda: pageSwitch(pages.index(fAdd)))
        delButton = ttk.Button(fMainMenu, text="Delete contact", command=lambda: pageSwitch(pages.index(fDelete)))
        listButton = ttk.Button(fMainMenu, text="List contacts", command=None)
        searchButton = ttk.Button(fMainMenu, text="Search contacts", command=None)
        editButton = ttk.Button(fMainMenu, text="Edit contact", command=None)

        mainLabel.grid(row=0)
        addButton.grid(row=1)
        delButton.grid(row=2)
        listButton.grid(row=3)
        searchButton.grid(row=4)
        editButton.grid(row=5)
        fMainMenu.grid()

        # Add page
        fAdd = ttk.Frame(root, padding=20)

        addNameEntry = ttk.Entry(fAdd, textvariable=name)
        addNumberEntry = ttk.Entry(fAdd, textvariable=number)
        addEmailEntry = ttk.Entry(fAdd, textvariable=email)
        addNotesEntry = ttk.Entry(fAdd, textvariable=notes)
        addConfirmButton = ttk.Button(fAdd, text="Add Contact", command=lambda: add(name, number, email, notes))
        addBackButton = ttk.Button(fAdd, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))

        addNameEntry.grid(column=0, row=0)
        addNameEntry.insert(index=0, string="Name")
        addNumberEntry.grid(column=0, row=1)
        addNumberEntry.insert(index=1, string="Number")
        addEmailEntry.grid(column=0, row=2)
        addEmailEntry.insert(index=2, string="Email")
        addNotesEntry.grid(column=0, row=3)
        addNotesEntry.insert(index=3, string="Notes")
        addConfirmButton.grid(column=1, row=1, rowspan=2)
        addBackButton.grid(column=1, row=3, rowspan=2)

        # Delete Page
        fDelete = ttk.Frame(root, padding=20)

        delNameEntry = ttk.Entry(fDelete, textvariable=name)
        delConfirmButton = ttk.Button(fDelete, text="Delete Contact", command=lambda: delete(name))
        delBackButton = ttk.Button(fDelete, text="Back to Main Menu", command=lambda: pageSwitch(pages.index(fMainMenu)))

        delNameEntry.grid(row=0, column=0, rowspan=2)
        delNameEntry.insert(index=0, string="Name")
        delConfirmButton.grid(row=0, column=1)
        delBackButton.grid(row=1, column=1)

        pages = [fMainMenu, fAdd, fDelete]

        # GUI Startpoint
        root.mainloop()


class contactDisplayer:
    def __init__(self, name, phone, email, notes):
        self.name = name
        self.phone = phone
        self.email = email
        self.notes = notes
        pass

    def displayer(self):
        print(f"Name: {self.name}, Phone number: {self.phone}, Email: {self.email}, Notes: {self.notes}")
        pass

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

def add(name, number, email, notes):
    dbcursor.execute("INSERT INTO contacts VALUES (?, ?, ?, ?)", (name, number, email, notes))
    contactdb.commit()
    print("Contact has been added!")

def lister():
    # TODO Add functionality to sort and filter items
    wholeTable = dbcursor.execute("SELECT * FROM contacts").fetchall()
    for i in range(len(wholeTable)):
        contactDisplayer(*wholeTable[i]).displayer()
    pass 

def search():
    # TODO Add search sorting functions, search by other columns
    name = input("Who would you like to search for? ")

    searchResult = dbcursor.execute("SELECT * FROM contacts WHERE Name = ?", [name])
    results = searchResult.fetchone()
    
    if results == None:
        print("Couldn't find any contacts by that name")
    else:
        contactDisplayer(*results).displayer()
    pass

def delete(name):
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE Name = ?", [name])
    contactdb.commit()
    print("Deletion successful!")
    pass

def edit():
    # TODO FIX currently doesn't work
    nameIndex = input("Who's contact would you like to change? ")
    name = input("New name: ")
    phone = input("New phone: ")
    email = input("New email: ")
    notes = input("New notes: ")

    dbcursor.execute("UPDATE contacts SET Name=?, Phone=?, Email=?, Notes=? WHERE Name=?", (name, phone, email, notes, nameIndex))
    contactdb.commit()
    pass

def save():
    # TODO Determine if save function is neccesary, and how to better implement it 
    contactdb.commit()
    dbcursor.close()
    pass

gui = GUI()

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
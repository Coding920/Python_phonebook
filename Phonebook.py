""" Gui program for accessing contacts based off of the Windows 7 program """

import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# DB Setup
contactdb = sql.connect("contacts.db")
dbcursor = contactdb.cursor()

# SQL that tests and creates table
tableCreation = """CREATE TABLE IF NOT EXISTS contacts(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    image TEXT,
                    first_name TEXT,
                    middle_name TEXT,
                    last_name TEXT,
                    phone TEXT,
                    email TEXT)"""
dbcursor.execute(tableCreation)

root = tk.Tk()
root.title("Phonebook")
root.iconphoto(True, tk.PhotoImage(file="./Contact_images/program_images/phonebook.png"))
contactPlaceholder = tk.PhotoImage(file="./Contact_images/program_images/blank_person.png")
style = ttk.Style()
style.configure("Treeview", rowheight=60)

# Variables
ID = 0
PATH = 1
FIRSTNAME = 2
MIDDLENAME = 3
LASTNAME = 4
PHONE = 5
EMAIL = 6

FRAMEPADDING = 20
BORDERWIDTH = 5

file = ""
firstName = tk.StringVar()
middleName = tk.StringVar()
lastName = tk.StringVar()
number = tk.StringVar()
email = tk.StringVar()
listForTable = tk.StringVar()
lastQuery = []
contactImages = {}
contactImages["placeholder"] = contactPlaceholder

for contact in dbcursor.execute("SELECT * FROM contacts").fetchall():
    contactId = contact[0]
    if contact[PATH]:
        contactImages[contactId] = tk.PhotoImage(file=contact[PATH])
    else:
        contactImages[contactId] = "No path"

class listbox(ttk.Treeview):
    def __init__(self, dbcursor: sql.Cursor, contactWindow: "function", master = None,\
                                                                                  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.dbcursor = dbcursor
        self.imageList = []
        self.heading("#0", text="")
        self.heading("name", text="Name")
        self.heading("number", text="Phone Number")
        self.heading("email", text="Email Address")
        self.bind("<Double-1>", lambda e: contactWindow(self.item(self.selection()[0], "tags")))
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

        for contactInfo in results:
            fullName = f"{contactInfo[FIRSTNAME]} {contactInfo[MIDDLENAME]} {contactInfo[LASTNAME]}"

            if contactImages[contactInfo[ID]] == "No path":
                image = contactImages["placeholder"]
            else:
                image = contactImages[contactInfo[ID]]

            image = image.subsample(4)
            self.imageList.append(image)
            self.insert("", ["end"],\
                         values=[fullName, contactInfo[PHONE], contactInfo[EMAIL]],\
                              image=image, tags=contactInfo[ID])
        self.update()

    def clear(self):
        for child in self.get_children():
            self.delete(child)
        self.imageList.clear()


class newWindow(tk.Toplevel):
    def __init__(self, contactId: int, master = None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.contactId = contactId

        query = """ SELECT * FROM contacts WHERE id = ? """
        contactInfo = dbcursor.execute(query, (contactId))
        contactInfo = contactInfo.fetchall()
        contactInfo = contactInfo[0]
        formatedName = f"{contactInfo[FIRSTNAME]} {contactInfo[LASTNAME]}"
        self.title(formatedName)

        contactId = int(contactId[0])
        if contactImages[contactId] == "No path":
            photoImage = ttk.Label(self, image=contactPlaceholder)
        else:
            photoImage = ttk.Label(self, image=contactImages[contactId])
            
        frame = ttk.Frame(self, padding=FRAMEPADDING)
        firstLabel = ttk.Label(frame, text="First:")
        middleLabel = ttk.Label(frame, text="Middle:")
        lastLabel = ttk.Label(frame, text="Last:")
        fullNameLabel = ttk.Label(frame, text="Full Name:")
        firstName = ttk.Label(frame, text=contactInfo[FIRSTNAME])
        middleName = ttk.Label(frame, text=contactInfo[MIDDLENAME])
        lastName = ttk.Label(frame, text=contactInfo[LASTNAME])
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

def getInput() -> list:
    return [firstName.get(), middleName.get(), lastName.get(), number.get(), email.get()]

def addContact() -> None:
    global file

    query = """ INSERT INTO contacts (image, first_name, middle_name, last_name, phone, email)
                             VALUES (?, ?, ?, ?, ?, ?) """

    if file == "":
        dbcursor.execute(query,\
            ("", *getInput()))
        lastId = dbcursor.lastrowid
        contactImages[lastId] = contactPlaceholder
        contactdb.commit()
        contactList.updateContacts()
        return

    dbcursor.execute(query,\
         ("", *getInput()))

    lastId = dbcursor.lastrowid
    newFile = open(f"./Contact_images/{firstName.get()}_{lastName.get()}{lastId}.png", "xb")
    with open(file, "rb") as buf:
        newFile.write(buf.read())
    newFile.close()

    contactImages[lastId] = tk.PhotoImage(file=newFile.name)

    dbcursor.execute("UPDATE contacts SET image = ? WHERE id = ?", (newFile.name, lastId))

    contactdb.commit()
    contactList.updateContacts()
    file = ""

def deleteContact() -> None:
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE first_name = ?", (firstName.get(), ))
    contactdb.commit()
    contactList.updateContacts()

def createWindow(contactId: int):
    contactWindow = newWindow(contactId)

def addContactPage():
    global file; file = ""
    addWindow = tk.Toplevel(root)
    photoImage = contactImages["placeholder"]

    image = ttk.Label(addWindow, image=photoImage)
    imageButton = ttk.Button(addWindow,
                             command=lambda: imageSelect(image, addWindow),
                             text="Select Image")

    frame = ttk.Frame(addWindow, padding=FRAMEPADDING)
    firstLabel = ttk.Label(frame, text="First:")
    middleLabel = ttk.Label(frame, text="Middle:")
    lastLabel = ttk.Label(frame, text="Last:")
    numberLabel = ttk.Label(frame, text="Number: ")
    emailLabel = ttk.Label(frame, text="Email: ")
    fullNameLabel = ttk.Label(frame, text="Full Name:")
    firstNameEntry = ttk.Entry(frame, textvariable=firstName)
    middleNameEntry = ttk.Entry(frame, textvariable=middleName)
    lastNameEntry = ttk.Entry(frame, textvariable=lastName)
    numberEntry = ttk.Entry(frame, textvariable=number)
    emailEntry = ttk.Entry(frame, textvariable=email)
    fullName = ttk.Label(frame, text="Fix Me")
    addButton = ttk.Button(frame,
                           command=lambda: (addContact(), addWindow.destroy()),
                           text="Add new contact")

    # Grid
    image.grid(column=0, row=0)
    imageButton.grid(column=0, row=1)
    frame.grid(column=1, row=0)
    firstLabel.grid(column=0, row=0)
    middleLabel.grid(column=0, row=1)
    lastLabel.grid(column=0, row=2)
    numberLabel.grid(column=0, row=3)
    emailLabel.grid(column=0, row=4)
    fullNameLabel.grid(column=0, row=5)

    firstNameEntry.grid(column=1, row=0)
    middleNameEntry.grid(column=1, row=1)
    lastNameEntry.grid(column=1, row=2)
    numberEntry.grid(column=1, row=3)
    emailEntry.grid(column=1, row=4)
    fullName.grid(column=1, row=5)
    addButton.grid(column=1, row=6)


def imageSelect(image: ttk.Label, master = root):
    global file
    title = "Png image files\t\t (Directories are on left, files on right)"
    file = filedialog.Open(master, title=title)
    file = file.show(initialdir="/")
    if file == "":
        return

    tempPhoto = tk.PhotoImage(file=file)
    contactImages["temp"] = tempPhoto
    image.configure(image=contactImages["temp"])
    image.update()

menubar = tk.Menu(root)
root["menu"] = menubar
menubar.add_command(label="Home", command=lambda: createWindow(1))
menubar.add_command(label="Add", command=lambda: addContactPage())
menubar.add_command(label="Settings", command=lambda: createWindow(1))

# Menu for listing, searching, adding, and deleting contacts
menu = ttk.Frame(root, padding=FRAMEPADDING, borderwidth=BORDERWIDTH, relief="raised")

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
searchButton = ttk.Button(menu, text="Search", command=lambda:\
                           contactList.updateContacts(*getInput()))
deleteButton = ttk.Button(menu, text="Delete Contact", command=lambda: deleteContact())

# Search result table
content = ttk.Frame(root, padding=FRAMEPADDING)
contactList = listbox(dbcursor, createWindow, content, columns=["name","number","email"], height=8)

# Grid info - Menu
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.configure(padx=FRAMEPADDING/2, pady=FRAMEPADDING/2)

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

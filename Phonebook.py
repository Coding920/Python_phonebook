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

    def deleteContact(self):
        deleteContact(self.item(self.selection()[0], "tags"))

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
            self.photoImage = ttk.Label(self, image=contactPlaceholder)
        else:
            self.photoImage = ttk.Label(self, image=contactImages[contactId])
            
        self.frame = ttk.Frame(self, padding=FRAMEPADDING)
        self.firstLabel = ttk.Label(self.frame, text="First: ")
        self.middleLabel = ttk.Label(self.frame, text="Middle: ")
        self.lastLabel = ttk.Label(self.frame, text="Last: ")
        self.fullNameLabel = ttk.Label(self.frame, text="Full Name: ")
        self.numberLabel = ttk.Label(self.frame, text="Phone Number: ")
        self.emailLabel = ttk.Label(self.frame, text="Email: ")

        self.firstName = ttk.Label(self.frame, text=contactInfo[FIRSTNAME])
        self.middleName = ttk.Label(self.frame, text=contactInfo[MIDDLENAME])
        self.lastName = ttk.Label(self.frame, text=contactInfo[LASTNAME])
        self.fullName = ttk.Label(self.frame, text=formatedName)
        self.number = ttk.Label(self.frame, text=contactInfo[PHONE])
        self.email = ttk.Label(self.frame, text=contactInfo[EMAIL])

        # Grid
        self.photoImage.grid(column=0, row=0)
        self.frame.grid(column=1, row=0)
        self.firstLabel.grid(column=0, row=0)
        self.middleLabel.grid(column=0, row=1)
        self.lastLabel.grid(column=0, row=2)
        self.fullNameLabel.grid(column=0, row=3)
        self.numberLabel.grid(column=0, row=4)
        self.emailLabel.grid(column=0, row=5)

        self.firstName.grid(column=1, row=0)
        self.middleName.grid(column=1, row=1)
        self.lastName.grid(column=1, row=2)
        self.fullName.grid(column=1, row=3)
        self.number.grid(column=1, row=4)
        self.email.grid(column=1, row=5)

class blankPage(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.file = ""
        self.firstName = tk.StringVar()
        self.middleName = tk.StringVar()
        self.lastName = tk.StringVar()
        self.number = tk.StringVar()
        self.email = tk.StringVar()

        photoImage = contactImages["placeholder"]

        image = ttk.Label(self, image=photoImage)
        imageButton = ttk.Button(self,
                                command=lambda: imageSelect(image, self),
                                text="Select Image")

        self.frame = ttk.Frame(self, padding=FRAMEPADDING)
        self.firstLabel = ttk.Label(self.frame, text="First:")
        self.middleLabel = ttk.Label(self.frame, text="Middle:")
        self.lastLabel = ttk.Label(self.frame, text="Last:")
        self.numberLabel = ttk.Label(self.frame, text="Number: ")
        self.emailLabel = ttk.Label(self.frame, text="Email: ")
        self.fullNameLabel = ttk.Label(self.frame, text="Full Name:")
        self.firstNameEntry = ttk.Entry(self.frame, textvariable=self.firstName)
        self.middleNameEntry = ttk.Entry(self.frame, textvariable=self.middleName)
        self.lastNameEntry = ttk.Entry(self.frame, textvariable=self.lastName)
        self.fullName = ttk.Label(self.frame, text="")
        self.numberEntry = ttk.Entry(self.frame, textvariable=self.number)
        self.emailEntry = ttk.Entry(self.frame, textvariable=self.email)
        self.bind("<Key>", lambda e: self.updateFullName())
        self.addButton = ttk.Button(self.frame,
                            command=lambda: (addContact(), self.destroy()),
                            text="Add new contact")

        # Grid
        image.grid(column=0, row=0)
        imageButton.grid(column=0, row=1)
        self.frame.grid(column=1, row=0)
        self.firstLabel.grid(column=0, row=0)
        self.middleLabel.grid(column=0, row=1)
        self.lastLabel.grid(column=0, row=2)
        self.fullNameLabel.grid(column=0, row=3)
        self.numberLabel.grid(column=0, row=4)
        self.emailLabel.grid(column=0, row=5)

        self.firstNameEntry.grid(column=1, row=0)
        self.middleNameEntry.grid(column=1, row=1)
        self.lastNameEntry.grid(column=1, row=2)
        self.fullName.grid(column=1, row=3)
        self.numberEntry.grid(column=1, row=4)
        self.emailEntry.grid(column=1, row=5)
        self.addButton.grid(column=1, row=6)

    def updateFullName(self):
        self.fullName.configure(text=f"{self.firstName.get()} {self.lastName.get()}")
        self.fullName.update()

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

def deleteContact(contactId: int) -> None:
    # TODO Make function to delete specified contact
    dbcursor.execute("DELETE FROM contacts WHERE id = ?", contactId)
    contactdb.commit()
    contactList.updateContacts()

def createWindow(contactId: int):
    contactWindow = newWindow(contactId)

def addContactPage():
    addPage = blankPage()

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
menubar.add_command(label="Add Contact", command=lambda: addContactPage())
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
deleteButton = ttk.Button(menu, text="Delete Contact", command=lambda: contactList.deleteContact())

# Search result table
content = ttk.Frame(root, padding=FRAMEPADDING)
contactList = listbox(dbcursor, createWindow, content, columns=["name","number","email", "delete"], height=8)

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

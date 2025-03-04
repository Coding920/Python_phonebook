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
contactImages["placeholder"] = tk.PhotoImage(file="./Contact_images/program_images/blank_person.png")

for contact in dbcursor.execute("SELECT * FROM contacts").fetchall():
    if contact[PATH]:
        contactImages[contact[ID]] = tk.PhotoImage(file=contact[PATH])
    else:
        contactImages[contact[ID]] = "No path"

def updateImages(key = "", value = "") -> dict:
    global contactImages
    if not key and not value:
        return contactImages
    contactImages[key] = value
    return contactImages

class listbox(ttk.Treeview):
    """ Displays contacts in a treeview. Comes with 
        update contacts function to refresh the listbox, delete contact
        function to delete selected contact, and some internal
        functions used by the update contacts function """

    def __init__(self, dbcursor: sql.Cursor, contactWindow: "function", master = None,\
                                                                                  *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.dbcursor = dbcursor
        self.imageList = [] # Necessary to stop GC from taking tk.photos
        self.contactImages = {}
        self.heading("#0", text="")
        self.heading("name", text="Name")
        self.heading("number", text="Phone Number")
        self.heading("email", text="Email Address")
        self.bind("<Double-1>", lambda e: contactWindow(self.item(self.selection()[0], "tags")))
        self.grid()

    def updateContacts(self, firstName="", middleName="", lastName="", number="", email=""):
        """ Refreshes listbox """

        self.clear()
        self.contactImages = updateImages()

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
            fullName = f"{contact[FIRSTNAME]} {contact[MIDDLENAME]} {contact[LASTNAME]}"

            if self.contactImages[contact[ID]] == "No path":
                image = self.contactImages["placeholder"]
            else:
                image = self.contactImages[contact[ID]]

            image = image.subsample(4)
            self.imageList.append(image)
            self.insert("", ["end"],\
                         values=[fullName, contact[PHONE], contact[EMAIL]],\
                              image=image, tags=contact[ID])
        self.update()

    def deleteContact(self):
        deleteContact(self.item(self.selection()[0], "tags"))

    def clear(self):
        """ Internal function """
        for child in self.get_children():
            self.delete(child)
        self.imageList.clear()


class displayerPage(tk.Toplevel):
    """ Display page for contacts. Normally a static page but
            with the edit button, it can be used to edit contacts """

    def __init__(self, contactId: int, dbcursor: sql.Cursor, *args, master = None, **kwargs):
        super().__init__(master, *args, **kwargs)
        # Variables
        self.contactId = int(contactId[0])
        self.dbcursor = dbcursor
        self.file = ""
        self.contactImages = updateImages()
        self.first = tk.StringVar()
        self.middle = tk.StringVar()
        self.last = tk.StringVar()
        self.numberVar = tk.StringVar()
        self.emailVar = tk.StringVar()

        query = """ SELECT * FROM contacts WHERE id = ? """
        contactInfo = dbcursor.execute(query, (contactId))
        contactInfo = contactInfo.fetchall()
        self.contactInfo = contactInfo[0]
        contactInfo = contactInfo[0]

        formatedName = f"{contactInfo[FIRSTNAME]} {contactInfo[LASTNAME]}"
        self.title(formatedName)

        if self.contactImages[self.contactId] == "No path":
            self.image = ttk.Label(self, image=self.contactImages["placeholder"])
        else:
            self.image = ttk.Label(self, image=self.contactImages[self.contactId])

        # Static side of Gui
        self.frame = ttk.Frame(self, padding=FRAMEPADDING)
        self.editButton = ttk.Button(self.frame, text="Edit Contact", command=lambda: self.editContact())
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

        self.staticGui: list[tk.Widget] = [self.editButton, self.firstName, self.middleName,
                                            self.lastName, self.number, self.email]

        # Editing side of Gui
        self.imageButton = ttk.Button(self,
                                command=lambda: self.imageSelect(),
                                text="Select Image")

        self.exitButton = ttk.Button(self.frame, text="Don't save", command=lambda: self.exitEdit())
        self.saveButton = ttk.Button(self.frame, text="Save Contact", command=lambda: [self.save(), self.exitEdit()])
        self.firstNameIn = ttk.Entry(self.frame, textvariable=self.first)
        self.middleNameIn = ttk.Entry(self.frame, textvariable=self.middle)
        self.lastNameIn = ttk.Entry(self.frame, textvariable=self.last)
        self.numberIn = ttk.Entry(self.frame, textvariable=self.numberVar)
        self.emailIn = ttk.Entry(self.frame, textvariable=self.emailVar)

        self.editGui: list[tk.Widget] = [self.imageButton, self.exitButton, self.saveButton,
                                        self.firstNameIn, self.middleNameIn, self.lastNameIn,
                                        self.numberIn, self.emailIn]

        # Grid
        self.image.grid(column=0, row=0)
        self.frame.grid(column=1, row=0)
        self.firstLabel.grid(column=0, row=1)
        self.middleLabel.grid(column=0, row=2)
        self.lastLabel.grid(column=0, row=3)
        self.fullNameLabel.grid(column=0, row=4)
        self.numberLabel.grid(column=0, row=5)
        self.emailLabel.grid(column=0, row=6)

        self.exitButton.grid(column=0, row=0)
        self.saveButton.grid(column=1, row=0)
        self.editButton.grid(column=1, row=0)
        self.firstName.grid(column=1, row=1)
        self.firstNameIn.grid(column=1, row=1)
        self.middleName.grid(column=1, row=2)
        self.middleNameIn.grid(column=1, row=2)
        self.lastName.grid(column=1, row=3)
        self.lastNameIn.grid(column=1, row=3)
        self.fullName.grid(column=1, row=4)
        self.number.grid(column=1, row=5)
        self.numberIn.grid(column=1, row=5)
        self.email.grid(column=1, row=6)
        self.emailIn.grid(column=1, row=6)

        # Placed Grid Info and then removed edit so that the col and row data only need put in once
        for item in self.editGui:
            item.grid_remove()

    def editContact(self):
        """ Puts window into edit mode. Removes everything from the entry boxes 
            and then replaces it with upto date info. Also binds key presses to update fullname"""

        # Clears file to prevent an old file from being held from a previous edit
        self.file = ""
        for component in self.staticGui:
            component.grid_remove()

        self.firstNameIn.delete(0, tk.END)
        self.middleNameIn.delete(0, tk.END)
        self.lastNameIn.delete(0, tk.END)
        self.numberIn.delete(0, tk.END)
        self.emailIn.delete(0, tk.END)

        self.firstNameIn.insert(0, self.contactInfo[FIRSTNAME])
        self.middleNameIn.insert(0, self.contactInfo[MIDDLENAME])
        self.lastNameIn.insert(0, self.contactInfo[LASTNAME])
        self.numberIn.insert(0, self.contactInfo[PHONE])
        self.emailIn.insert(0, self.contactInfo[EMAIL])

        self.bind("<Key>", lambda e: self.updateFullName())

        for component in self.editGui:
            component.grid()

    def save(self):
        """ Updates sql table with new contact info and saves images 
                into the contact_images folder """

        query = """ UPDATE contacts SET
                    image = ?,
                    first_name = ?,
                    middle_name = ?, 
                    last_name = ?, 
                    phone = ?, 
                    email = ?
                    WHERE id = ? """

        if self.file == "":
            self.dbcursor.execute(query, (self.file, *self.getInput(), self.contactId))
            contactList.updateContacts()
            return

        newFilePath = copyImage(self.file, self.first.get(), self.last.get(), self.contactId)

        self.contactImages = updateImages(self.contactId, tk.PhotoImage(file=newFilePath))
        self.dbcursor.execute(query, (newFilePath, *self.getInput(), self.contactId))
        contactList.updateContacts()

    def exitEdit(self):
        """ Takes window out of edit mode and updates static side Gui
            to be current with possibly updated info. Also unbinds key press"""

        for component in self.editGui:
            component.grid_remove()

        contactInfo = self.dbcursor.execute("SELECT * FROM contacts WHERE id = ?", (self.contactId,))
        contactInfo = contactInfo.fetchall()[0]

        self.firstName.configure(text=contactInfo[FIRSTNAME])
        self.middleName.configure(text=contactInfo[MIDDLENAME])
        self.lastName.configure(text=contactInfo[LASTNAME])
        self.fullName.configure(text=f"{contactInfo[FIRSTNAME]} {contactInfo[LASTNAME]}")
        self.number.configure(text=contactInfo[PHONE])
        self.email.configure(text=contactInfo[EMAIL])

        for component in self.staticGui:
            component.update()
            component.grid()

        self.unbind("<Key>")

    def imageSelect(self):
        """ Updates self.file to selected file and 
        updates the temp image in self.contactImages """

        self.file = filedialog.Open(self, title="Png image files")
        self.file = self.file.show(initialdir="~") # ~ is Home dir
        if self.file == "":
            return

        self.contactImages = updateImages("temp", tk.PhotoImage(file=self.file))
        self.image.configure(image=self.contactImages["temp"])
        self.image.update()

    def updateFullName(self):
        self.fullName.configure(text=f"{self.first.get()} {self.last.get()}")
        self.fullName.update()

    def getInput(self) -> list:
        return [self.first.get(), self.middle.get(), self.last.get(),\
                self.numberVar.get(), self.emailVar.get()]


class blankPage(tk.Toplevel):
    def __init__(self, master = None):
        super().__init__(master)
        self.file = ""
        self.tempImage = None
        self.firstName = tk.StringVar()
        self.middleName = tk.StringVar()
        self.lastName = tk.StringVar()
        self.number = tk.StringVar()
        self.email = tk.StringVar()

        self.image = ttk.Label(self, image=contactImages["placeholder"])
        imageButton = ttk.Button(self,
                                command=lambda: self.imageSelect(),
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
                            command=lambda: (self.addContact(), self.destroy()),
                            text="Add new contact")

        # Grid
        self.image.grid(column=0, row=0)
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

    def imageSelect(self):
        """ Updates self.file to selected file and 
        updates the temp image in self.contactImages """

        self.file = filedialog.Open(self, title="Png image files")
        self.file = self.file.show(initialdir="/")
        if self.file == "":
            return

        self.tempImage = tk.PhotoImage(file=self.file)
        self.image.configure(image=self.tempImage)
        self.image.update()

    def addContact(self):
        addContact(*self.getInput())

    def updateFullName(self):
        self.fullName.configure(text=f"{self.firstName.get()} {self.lastName.get()}")
        self.fullName.update()

    def getInput(self) -> list:
        return [self.file, self.firstName.get(), self.middleName.get(), self.lastName.get(),
                self.number.get(), self.email.get()]


def getInput() -> list:
    return [firstName.get(), middleName.get(), lastName.get(), number.get(), email.get()]

def addContact(file, firstName, middleName, lastName, number, email) -> None:
    query = """ INSERT INTO contacts (image, first_name, middle_name, last_name, phone, email)
                             VALUES (?, ?, ?, ?, ?, ?) """

    if file == "":
        dbcursor.execute(query, (file, firstName, middleName, lastName, number, email))
        lastId = dbcursor.lastrowid
        updateImages(lastId, contactImages["placeholder"])
        contactdb.commit()
        contactList.updateContacts()
        return

    dbcursor.execute(query, ("", firstName, middleName, lastName, number, email))

    lastId = dbcursor.lastrowid
    newFilePath = copyImage(file, firstName, lastName, lastId)

    updateImages(lastId, tk.PhotoImage(file=newFilePath)) # Fix here

    dbcursor.execute("UPDATE contacts SET image = ? WHERE id = ?", (newFilePath, lastId))

    contactdb.commit()
    contactList.updateContacts()

def copyImage(path, firstName, lastName, contactId) -> str:
    """ Make new image path or write over old image """
    
    newPath = f"./Contact_images/{firstName}_{lastName}{contactId}.png"
    try:
        newFile = open(newPath, "xb")
    except FileExistsError:
        newFile = open(newPath, "wb")

    with open(path, "rb") as old:
        newFile.write(old.read())
    newFile.close()

    return newFile.name

def deleteContact(contactId: int) -> None:
    dbcursor.execute("DELETE FROM contacts WHERE id = ?", contactId)
    contactdb.commit()
    contactList.updateContacts()

def createWindow(contactId: int):
    contactWindow = displayerPage(contactId, dbcursor)

def addContactPage():
    addPage = blankPage()

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

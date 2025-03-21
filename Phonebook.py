""" Gui program for accessing contacts based off of the Windows 7 program """
# Used un-intergrated Copilot to help with several error messages and the understanding of certain
# details of code, mostly relating to the use of Tkinter. I tried to keep usage as minimal as possible

# Image for blank person is from https://www.freeimages.com/icon/users-folder-5600760
# Image for phonebook icon is from https://www.freepik.com/icons/phonebook

import os
import json
import sqlite3 as sql
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

# Config settings stuff
def_settings = {
    "Font": "Arial",
    "Font-size": 10,
    "Font-color": "Black",
    "Background-color": "Light Gray",
}

# Creates defaults but won't override user settings
if not os.path.exists("settings.json"):
    with open("settings.json", "w") as file:
        json.dump(def_settings, file, indent=4)

# Read json into settings dict
with open("settings.json", "r") as file:
    settings = json.load(file)

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

# Variables
ID = 0
PATH = 1
FIRSTNAME = 2
MIDDLENAME = 3
LASTNAME = 4
PHONE = 5
EMAIL = 6

GRID_KWARGS = {"padx": 2, "pady": 5}
COLORS = ["Red", "Black", "White", "Blue", "Aquamarine", "Cyan", "Chocolate",
                "Gray", "Light Gray", "Dark Gray", "Dark Red", "Dark Blue"]

FONTS = ["Terminal", "Modern", "Roman", "Script", "Courier", "MS Serif", "MS Sans Serif",
        "Ariel", "Ariel Greek", "Ariel Black", "Calibri", "Calibri Light", "Cambria",
        "Comic Sans MS", "Times New Roman", "Century Gothic"]

FRAMEPADDING = 20
BORDERWIDTH = 5

contactImages: dict[tk.PhotoImage] = {}
def updateImages(key = "", value = "") -> dict:
    global contactImages
    if not key and not value:
        return contactImages
    contactImages[key] = value
    return contactImages

class mainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.firstName = tk.StringVar()
        self.middleName = tk.StringVar()
        self.lastName = tk.StringVar()
        self.number = tk.StringVar()
        self.email = tk.StringVar()

        # Data Setup
        updateImages("window",
                        tk.PhotoImage(file="./Contact_images/program_images/phonebook.png"))
        updateImages("placeholder",
                        tk.PhotoImage(file="./Contact_images/program_images/blank_person.png"))

        # Inputting data for contact images
        for contact in dbcursor.execute("SELECT * FROM contacts").fetchall():
            if contact[PATH]:
                try:
                    updateImages(contact[ID], tk.PhotoImage(file=contact[PATH]))
                except tk.TclError:
                    self.after(150, lambda: messagebox.showerror("Image file missing",
                    f"The image associated with {contact[FIRSTNAME]}'s contact is missing"))

                    updateImages(contact[ID], "No path")
            else:
                updateImages(contact[ID], "No path")

        # Gui Defining
        self.title("Phonebook")
        self.iconphoto(True, contactImages["window"])

        # Style
        self.configure(background=settings["Background-color"])
        self.style = ttk.Style(self)
        self.style.theme_use("alt")
        self.style.configure(".",
                              font=(settings["Font"], settings["Font-size"]),
                              foreground=settings["Font-color"],
                              background=settings["Background-color"])
        self.style.configure("Treeview", rowheight=60,
                              foreground=settings["Font-color"],
                              background=settings["Background-color"],
                              fieldbackground=settings["Background-color"])

        # The window menu
        self.menubar = tk.Menu(self)
        self["menu"] = self.menubar
        self.menubar.add_command(label="Home", command=lambda: self.homePage())
        self.menubar.add_command(label="Add Contact", command=lambda: addContactPage())
        self.menubar.add_command(label="Settings", command=lambda: self.settingsPage())

        # Menu for listing, searching, and deleting contacts
        self.searchMenu = ttk.Frame(self)
        self.inputs = ttk.Frame(self.searchMenu)

        self.firstNameEntry = ttk.Entry(self.inputs, textvariable=self.firstName)
        self.firstNameLabel = ttk.Label(self.inputs, text="First name: ")
        self.middleNameEntry = ttk.Entry(self.inputs, textvariable=self.middleName)
        self.middleNameLabel = ttk.Label(self.inputs, text="Middle name: ")
        self.lastNameEntry = ttk.Entry(self.inputs, textvariable=self.lastName)
        self.lastNameLabel = ttk.Label(self.inputs, text="Last name: ")
        self.numberEntry = ttk.Entry(self.inputs, textvariable=self.number)
        self.numberLabel = ttk.Label(self.inputs, text="Phone Number:")
        self.emailEntry = ttk.Entry(self.inputs, textvariable=self.email)
        self.emailLabel = ttk.Label(self.inputs, text="Email Address:")

        self.listButton = ttk.Button(self.inputs, text="List all", 
                                     command=lambda: self.contactList.updateContacts())
        self.searchButton = ttk.Button(self.inputs, text="Search", command=lambda:\
                                self.contactList.updateContacts(*self.getInput()))
        self.deleteButton = ttk.Button(self.searchMenu, text="Delete Contact",
                                        command=lambda: self.contactList.deleteContact())
        self.infoLabel = ttk.Label(self.searchMenu,
                text="""\tFill in these text boxes to search. \n
                Delete Contacts by selecting them in the list and hitting the delete button\n
                Double-clicking a contact will launch more information\n
                Images must be PNG's""")

        # Contact list
        self.content = ttk.Frame(self, padding=FRAMEPADDING)
        self.contactList = listbox(dbcursor, createWindow,
                                    self.content, columns=["name","number","email"],
                                    height=8)
        self.mainPage = [self.content, self.searchMenu]

        # Grid Info
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(padx=FRAMEPADDING/2, pady=FRAMEPADDING/2)

        self.searchMenu.grid(column=1, row=0, sticky=tk.NSEW, **GRID_KWARGS)

        self.deleteButton.grid(column=0, row=0, padx=5, pady=40)
        self.inputs.grid(column=0, row=1)
        self.infoLabel.grid(column=0, row=2, columnspan=3, padx=5, pady=10)

        self.firstNameLabel.grid(column=0, row=1, **GRID_KWARGS)
        self.middleNameLabel.grid(column=0, row=2, **GRID_KWARGS)
        self.lastNameLabel.grid(column=0, row=3, **GRID_KWARGS)
        self.numberLabel.grid(column=0, row=4, **GRID_KWARGS)
        self.emailLabel.grid(column=0, row=5, **GRID_KWARGS)

        self.firstNameEntry.grid(column=1, row=1, **GRID_KWARGS)
        self.middleNameEntry.grid(column=1, row=2, **GRID_KWARGS)
        self.lastNameEntry.grid(column=1, row=3, **GRID_KWARGS)
        self.numberEntry.grid(column=1, row=4, **GRID_KWARGS)
        self.emailEntry.grid(column=1, row=5, **GRID_KWARGS)

        self.searchButton.grid(column=2, row=3, **GRID_KWARGS)
        self.listButton.grid(column=2, row=4, **GRID_KWARGS)

        self.content.grid(column=0, row=0)

        # Setting up contact list
        self.contactList.updateContacts()

    def getInput(self):
        return [self.firstName.get(), self.middleName.get(), self.lastName.get(),
                 self.number.get(), self.email.get()]

    def settingsPage(self):
        for child in self.mainPage:
            child.grid_remove()

        self.fontVar = tk.StringVar()
        self.sizeVar = tk.IntVar()
        self.fontColorVar = tk.StringVar()
        self.bgColorVar = tk.StringVar()

        self.settingFrame = ttk.Frame(self, padding=FRAMEPADDING)

        # Font Option
        self.fontLabel = ttk.Label(self.settingFrame, text="Font Style: ")
        self.fontOption = ttk.Combobox(self.settingFrame, values=FONTS, textvariable=self.fontVar)
        self.fontOption.set(settings["Font"])
        self.fontOption.state(["readonly"])

        # Font-size Option
        self.fontSizeLabel = ttk.Label(self.settingFrame, text="Font Size: ")
        fontSizes = [i for i in range(6, 41)]
        self.fontSize = ttk.Spinbox(self.settingFrame, values=fontSizes, textvariable=self.sizeVar)
        self.fontSize.state(["readonly"])
        self.fontSize.set(settings["Font-size"])

        # Font-color Option
        self.fontColorLabel = ttk.Label(self.settingFrame, text="Font Color: ")
        self.fontColor = ttk.Combobox(self.settingFrame, values=COLORS,
                                        textvariable=self.fontColorVar)
        self.fontColor.set(settings["Font-color"])
        self.fontColor.state(["readonly"])

        # Bg-color Option
        self.backgroundLabel = ttk.Label(self.settingFrame, text="Background Color: ")
        self.bgColor = ttk.Combobox(self.settingFrame, values=COLORS, textvariable=self.bgColorVar)
        self.bgColor.set(settings["Background-color"])
        self.bgColor.state(["readonly"])

        self.saveButton = ttk.Button(self.settingFrame, text="Save settings",
                                     command=lambda: self.saveSettings())

        # Grid
        self.settingFrame.grid(column=0, row=0)

        self.fontLabel.grid(column=0, row=0, **GRID_KWARGS)
        self.fontOption.grid(column=1, row=0, **GRID_KWARGS)
        self.fontSizeLabel.grid(column=0, row=1, **GRID_KWARGS)
        self.fontSize.grid(column=1, row=1, **GRID_KWARGS)
        self.fontColorLabel.grid(column=0, row=2, **GRID_KWARGS)
        self.fontColor.grid(column=1, row=2, **GRID_KWARGS)
        self.backgroundLabel.grid(column=0, row=3, **GRID_KWARGS)
        self.bgColor.grid(column=1, row=3, **GRID_KWARGS)
        self.saveButton.grid(column=0, row=4)

    def saveSettings(self):
        global settings
        inputs = {
        "Font": self.fontVar.get(),
        "Font-size": self.sizeVar.get(),
        "Font-color": self.fontColorVar.get(),
        "Background-color": self.bgColorVar.get()
        }

        with open("settings.json", "w+") as file:
            json.dump(inputs, file, indent=4)
            file.seek(0)
            settings = json.load(file)

        self.style.configure(".",
                              font=(settings["Font"], settings["Font-size"]),
                              foreground=settings["Font-color"],
                              background=settings["Background-color"])
        self.style.configure("Treeview", rowheight=60,
                              foreground=settings["Font-color"],
                              background=settings["Background-color"],
                              fieldbackground=settings["Background-color"])
        self.update()

    def homePage(self):
        self.settingFrame.grid_remove()
        for child in self.mainPage:
            child.grid()


class listbox(ttk.Treeview):
    """ Displays contacts in a treeview. Comes with 
        update contacts function to refresh the listbox, delete contact
        function to delete selected contact, and some internal
        functions used by the update contacts function """

    def __init__(self, dbcursor: sql.Cursor, contactWindow: "function", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dbcursor = dbcursor
        self.imageList = [] # Necessary to stop GC from taking tk.photos
        self.contactImages: dict[tk.PhotoImage] = {}
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
                image: tk.PhotoImage = self.contactImages["placeholder"]
            else:
                image: tk.PhotoImage = self.contactImages[contact[ID]]

            # Image resizing
            height = image.height() # The height needs to be 50 at the end

            # 50 = x * or % height      So we have to solve for x
            if height > 60:
                x = height / 60
                image = image.subsample(round(x))
            elif height < 60:
                x = 60 / height
                image = image.zoom(round(x))

            self.imageList.append(image)
            self.insert("", ["end"],\
                         values=[fullName, contact[PHONE], contact[EMAIL]],\
                              image=image, tags=contact[ID])
        self.update()

    def deleteContact(self):
        deleteContact(self.item(self.selection()[0], "tags"))

    def clear(self):
        """ Empties listbox """
        for child in self.get_children():
            self.delete(child)
        self.imageList.clear()


class displayerPage(tk.Toplevel):
    """ Display page for contacts. Normally a static page but
            with the edit button, it can be used to edit contacts """

    def __init__(self, contactId: int, dbcursor: sql.Cursor, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(padx=FRAMEPADDING/2, pady=FRAMEPADDING/2)

        if self.contactImages[self.contactId] == "No path":
            self.image: tk.PhotoImage = self.contactImages["placeholder"]
        else:
            self.image: tk.PhotoImage = self.contactImages[self.contactId]

        height = self.image.height() # We want height to be 300

        # 300 = X * or % height
        if height > 300:
            x = height / 300
            self.image = self.image.subsample(round(x))
        elif height < 300:
            x = 300 / height
            self.image = self.image.zoom(round(x))

        self.imageFrame = ttk.Frame(self, padding=FRAMEPADDING)
        self.imageLabel = ttk.Label(self.imageFrame, image=self.image)

        # Static side of Gui
        self.frame = ttk.Frame(self, padding=FRAMEPADDING)
        self.editButton = ttk.Button(self.frame, text="Edit Contact", 
                                     command=lambda: self.editContact())
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
        self.saveButton = ttk.Button(self.frame, text="Save Contact",
                                     command=lambda: [self.save(), self.exitEdit()])
        self.firstNameIn = ttk.Entry(self.frame, textvariable=self.first)
        self.middleNameIn = ttk.Entry(self.frame, textvariable=self.middle)
        self.lastNameIn = ttk.Entry(self.frame, textvariable=self.last)
        self.numberIn = ttk.Entry(self.frame, textvariable=self.numberVar)
        self.emailIn = ttk.Entry(self.frame, textvariable=self.emailVar)

        self.editGui: list[tk.Widget] = [self.imageButton, self.exitButton, self.saveButton,
                                        self.firstNameIn, self.middleNameIn, self.lastNameIn,
                                        self.numberIn, self.emailIn]

        # Grid
        self.imageFrame.grid(column=0, row=0)
        self.imageLabel.grid(column=0, row=0)
        self.imageButton.grid(column=0, row=1)
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

        if self.file:
            query = """ UPDATE contacts SET
                        image = ?,
                        first_name = ?,
                        middle_name = ?, 
                        last_name = ?, 
                        phone = ?, 
                        email = ?
                        WHERE id = ? """

            newFilePath = copyImage(self.file, self.first.get(), self.last.get(), self.contactId)

            self.contactImages = updateImages(self.contactId, tk.PhotoImage(file=newFilePath))
            self.dbcursor.execute(query, (newFilePath, *self.getInput(), self.contactId))
            root.contactList.updateContacts()

        query = """ UPDATE contacts SET
                    first_name = ?,
                    middle_name = ?, 
                    last_name = ?, 
                    phone = ?, 
                    email = ?
                    WHERE id = ? """
        
        if self.file == "":
            self.dbcursor.execute(query, (*self.getInput(), self.contactId))
            root.contactList.updateContacts()
            return


    def exitEdit(self):
        """ Takes window out of edit mode and updates static side Gui
            to be current with possibly updated info. Also unbinds key press"""

        for component in self.editGui:
            component.grid_remove()

        contactInfo = self.dbcursor.execute("SELECT * FROM contacts WHERE id = ?",
                                             (self.contactId,))
        contactInfo = contactInfo.fetchall()[0]
        if not contactInfo[PATH]:
           self.contactImages = updateImages(self.contactId, contactImages["placeholder"]) 
        else:
            self.contactImages = updateImages(self.contactId, tk.PhotoImage(file=contactInfo[PATH]))

        self.image = self.contactImages[self.contactId]

        if self.image == "No path":
            self.image = self.contactImages["placeholder"]

        height = self.image.height() # We want height to be 300

        # 300 = X * or % height
        if height > 300:
            x = height / 300
            self.image = self.image.subsample(round(x))
        elif height < 300:
            x = 300 / height
            self.image = self.image.zoom(round(x))

        self.imageLabel.configure(image=self.image)
        self.firstName.configure(text=contactInfo[FIRSTNAME])
        self.middleName.configure(text=contactInfo[MIDDLENAME])
        self.lastName.configure(text=contactInfo[LASTNAME])
        self.fullName.configure(text=f"{contactInfo[FIRSTNAME]} {contactInfo[LASTNAME]}")
        self.number.configure(text=contactInfo[PHONE])
        self.email.configure(text=contactInfo[EMAIL])

        self.imageLabel.update()
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
        self.image = self.contactImages["temp"]
        
        height = self.image.height() # We want height to be 300

        # 300 = X * or % height
        if height > 300:
            x = height / 300
            self.image = self.image.subsample(round(x))
        elif height < 300:
            x = 300 / height
            self.image = self.image.zoom(round(x))

        self.imageLabel.configure(image=self.image)
        self.imageLabel.update()

    def updateFullName(self):
        self.fullName.configure(text=f"{self.first.get()} {self.last.get()}")
        self.fullName.update()

    def getInput(self) -> list:
        return [self.first.get(), self.middle.get(), self.last.get(),\
                self.numberVar.get(), self.emailVar.get()]


class blankPage(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.file = ""
        self.tempImage = None
        self.firstName = tk.StringVar()
        self.middleName = tk.StringVar()
        self.lastName = tk.StringVar()
        self.number = tk.StringVar()
        self.email = tk.StringVar()

        self.image = contactImages["placeholder"]
        height = self.image.height()

        if height > 300:
            x = height / 300
            self.image = self.image.subsample(round(x))
        elif height < 300:
            x = 300 / height
            self.image = self.image.zoom(round(x))

        self.imageFrame = ttk.Frame(self)
        self.imageLabel = ttk.Label(self.imageFrame, image=self.image)
        imageButton = ttk.Button(self.imageFrame,
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
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(padx=FRAMEPADDING/2, pady=FRAMEPADDING/2)

        self.imageFrame.grid(column=0, row=0, sticky=tk.NSEW)
        self.imageLabel.grid(column=0, row=0)
        imageButton.grid(column=0, row=1)

        self.frame.grid(column=1, row=0, sticky=tk.NSEW)

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

        height = self.tempImage.height() # We want height to be 300

        # 300 = X * or % height
        if height > 300:
            x = height / 300
            self.tempImage = self.tempImage.subsample(round(x))
        elif height < 300:
            x = 300 / height
            self.tempImage = self.tempImage.zoom(round(x))

        self.imageLabel.configure(image=self.tempImage)
        self.imageLabel.update()

    def addContact(self):
        addContact(*self.getInput())

    def updateFullName(self):
        self.fullName.configure(text=f"{self.firstName.get()} {self.lastName.get()}")
        self.fullName.update()

    def getInput(self) -> list:
        return [self.file, self.firstName.get(), self.middleName.get(), self.lastName.get(),
                self.number.get(), self.email.get()]


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

    return newPath

def addContact(file, firstName, middleName, lastName, number, email) -> None:
    query = """ INSERT INTO contacts (image, first_name, middle_name, last_name, phone, email)
                             VALUES (?, ?, ?, ?, ?, ?) """

    if file == "":
        dbcursor.execute(query, (file, firstName, middleName, lastName, number, email))
        lastId = dbcursor.lastrowid
        updateImages(lastId, contactImages["placeholder"])
        contactdb.commit()
        root.contactList.updateContacts()
        return

    dbcursor.execute(query, ("", firstName, middleName, lastName, number, email))

    lastId = dbcursor.lastrowid
    newFilePath = copyImage(file, firstName, lastName, lastId)

    updateImages(lastId, tk.PhotoImage(file=newFilePath)) # Fix here

    dbcursor.execute("UPDATE contacts SET image = ? WHERE id = ?", (newFilePath, lastId))

    contactdb.commit()
    root.contactList.updateContacts()

def deleteContact(contactId: int) -> None:
    contact = dbcursor.execute("SELECT * FROM contacts WHERE id = ?", contactId).fetchall()[0]
    msg = messagebox.askyesno("Delete contact",
                  f"Are you sure you want to delete {contact[FIRSTNAME]} {contact[LASTNAME]}?")

    if not msg:
        return

    dbcursor.execute("DELETE FROM contacts WHERE id = ?", contactId)
    contactdb.commit()

    if not contact[PATH]:
        root.contactList.updateContacts()
        return

    try:
        os.remove(contact[PATH])
    except FileNotFoundError:
        pass
    except PermissionError:
        messagebox.showerror("Error",
                            "Couldn't delete image associated with contact/Permission error")
    except Exception as e:
        messagebox.showerror("Error", e)


    root.contactList.updateContacts()

def createWindow(contactId: int):
    contactWindow = displayerPage(contactId, dbcursor)
    contactWindow.transient(root) # Fixed window being hidden when file dialog is activated

def addContactPage():
    addPage = blankPage()
    addPage.transient(root) # Fixed window being hidden when file dialog is activated


root = mainWindow()

# GUI Startpoint
root.mainloop()

contactdb.commit()
contactdb.close()

import sqlite3 as sql

#This is a phonebook program that holds a persons name and their number

contactdb = sql.connect("contacts.db")
dbcursor = contactdb.cursor()

# This is where i'm testing to see if the table already exists, or else creating it 
tableCreation = "CREATE TABLE contacts(PersonID INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, PhoneNumber TEXT, Email TEXT, Notes TEXT)"
openingTest = dbcursor.execute("SELECT name FROM sqlite_master WHERE name='contacts'")
if openingTest.fetchone() == None:
     print("Creating database ...")
     dbcursor.execute(tableCreation)
         
print("Hello!", end=' ')

def main():
    
    while True:
            print()
            choice = input("Add or delete a contact (add/del), list contacts (list), search contacts (search), quit (q): ")
            print()

            match choice.lower():
                case "add":
                    add()

                case "list":
                    lister()

                case "search":
                    search()
               
                case "del":
                    delete()

                case "quit" | "q":
                    save()
                    break
                 
def add():
     name = input("Who is it that you are adding? ")
     number = input("Phone number: ")
     email = input("Email address: ")
     notes = input("Any notes? ")

     dbcursor.execute("INSERT INTO contacts (Name, PhoneNumber, Email, Notes) VALUES (?, ?, ?, ?)", (name, number, email, notes))

def lister():
     # TODO Make a function to list all contacts, maybe in the future add sorting
     wholeTable = dbcursor.execute("SELECT * FROM contacts")
     print(wholeTable.fetchall())
     pass 

def search():
     # TODO Make a function to search, at first just by name but then lets maybe broaden to other columns as well
     name = input("Who would you like to search for? ")

     searchResult = dbcursor.execute("SELECT * FROM contacts WHERE Name = ?", [name])
     print(searchResult.fetchall())
     pass

def delete():
     # TODO Make function to delete specified contact
     pass

def save():
     # TODO Determine if save function is neccesary 
     contactdb.commit()
     pass

# TODO Edit function, add column for more data function, 

main()
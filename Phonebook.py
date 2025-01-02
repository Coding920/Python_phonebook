import sqlite3 as sql

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

#This is a phonebook program that holds a persons name and their number

contactdb = sql.connect("contacts.db")
dbcursor = contactdb.cursor()

# SQL entry that tests and creates table
tableCreation = """CREATE TABLE IF NOT EXISTS contacts(
                    Name TEXT,
                    Phone TEXT,
                    Email TEXT,
                    Notes TEXT)"""
dbcursor.execute(tableCreation)
         
# Menu and prompts

print("Hello!", end=' ')

def main():
    
    while True:
            print()
            choice = input("Add or delete a contact (add/del), edit a contact (edit), list contacts (list), search contacts (search), quit (q): ")
            print()

            match choice.lower():
                case "add":
                    add()

                case "edit":
                    edit()
               
                case "del":
                    delete()

                case "list":
                    lister()

                case "search":
                    search()

                case "quit" | "q":
                    save()
                    break
                 
def add():
     name = input("Who is it that you are adding? ")
     number = input("Phone number: ")
     email = input("Email address: ")
     notes = input("Any notes? ")

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

def delete():
     # TODO Make function to delete specified contact
     name = input("Who's contact would you like to delete? ")
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

# TODO add column for more data function, make presentation prettier, etc.

main()
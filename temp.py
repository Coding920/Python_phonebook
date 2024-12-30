import sqlite3 as sql

contactdb = sql.connect("contacts.db")
dbcursor = contactdb.cursor()

result = dbcursor.execute("SELECT name FROM sqlite_master WHERE name='contacts'")

# Create table if doesn't exist
if result.fetchone() == None:
    print("Making new database ...")
    dbcursor.execute("CREATE TABLE contacts(name, phone, email, notes)")

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
            break

name = input("Name: ")
phone = input("Phone Number: ")
email = input("Email: ")
notes = input("Notes: ")

dbcursor.execute("INSERT INTO contacts VALUES(?, ?, ?, ?)", [name, phone, email, notes])
contactdb.commit() 

result = dbcursor.execute("SELECT * FROM contacts")

print(result.fetchall())

dbcursor.execute("DROP TABLE contacts")
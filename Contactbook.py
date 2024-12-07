import csv

#This is a contact book program that holds a persons name and their number

contactbook = {}

# Put Csv file into memory as a dict
with open("Contactbook.csv", 'r', newline='') as contactfile:
    contactreader = csv.reader(contactfile)

    for line in contactreader:
         contactbook[f"{line[0]}"] = line[1]

         
print("Hello!", end=' ')

def main():
    print("Add or delete a contact (add/del), list contacts (list), search contacts (search), quit (q)")
    
    while True:
            print()
            choice = input("What would you like to do? ", )
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
     number = input("And their phone number? ")

     contactbook[f"{name}"] = f"{number}"

def lister():
     for keys in contactbook:
          print(f"{keys} {contactbook[keys]}")

def search():
     name = input("Who are you looking for? ")

     if name in contactbook:
          print(f"Found! Number: {contactbook[f"{name}"]}")
     else:
          print("Not found")

def delete():
     name = input("Who's contact would you like to delete? ")

     if name in contactbook:
          del contactbook[name]
          print("Successfully deleted!")
     else:
          print("Unable to delete. Contact not found")

def save():
     # Writes contactbook dict back into the csv file
     with open("Contactbook.csv", 'w', newline='') as contactfile:
          csvwriter = csv.writer(contactfile)

          for keys in contactbook:
               csvwriter.writerow([f"{keys}"] + [f"{contactbook[keys]}"])

main()
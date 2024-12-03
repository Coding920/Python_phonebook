import csv

fieldnames = ['Name', 'Number']
contactbook = {}

with open("Contactbook.csv", 'r', newline='') as contactfile:
    contactreader = csv.DictReader(contactfile)

    for line in contactreader:
         contactbook = line


def main():
    print("Hello! You can: Add a new contact (add), list contacts (list), search contacts (search), quit (q)")
    
    while True:
            choice = input("What would you like to do? ")

            match choice.lower():
                case "add":
                    add()

                case "list":
                      lister()

                case "search":
                      search()

                case "save":
                      save()

                case "quit" | "q":
                    break
                 
def add():
     name = input("Who is it that you are adding? ")
     number = input("And their phone number? ")

     #contactbook["Name:"] = f"{name}"
     #contactbook["Number:"] = f"{number}" #Needs redone

def lister():
     for rows in contactbook:
          print(f"{contactbook}")

def search():
     name = input("Who are you looking for? ")

     if name in contactbook:
          print(f"{contactbook[f"{name}"]}")
     else:
          print("Not found")

def save():
     with open("Contactbook.csv", 'w', newline='') as contactfile:
          csvwriter = csv.DictWriter(contactfile, fieldnames = fieldnames)

          csvwriter.writeheader()
          for row in contactbook:
               csvwriter.writerow(row)

main()
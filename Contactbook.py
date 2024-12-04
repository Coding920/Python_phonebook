import csv

#This is a contact book program that holds a persons name and their number

contactbook = {}

# Put Csv file into memory as a dict
with open("Contactbook.csv", 'r', newline='') as contactfile:
    contactreader = csv.reader(contactfile)

    for line in contactreader:
         contactbook[f"{line[0]}"] = line[1]

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

def save():
     # Writes contactbook dict back into the csv file
     with open("Contactbook.csv", 'w', newline='') as contactfile:
          csvwriter = csv.writer(contactfile)

          for keys in contactbook:
               csvwriter.writerow([f"{keys}"] + [f"{contactbook[keys]}"])

main()
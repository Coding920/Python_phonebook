import csv

#This is a contact book program that holds a persons name and their number

class Contact:

    def __init__(self, name, phoneNumber, email, notes):
        self.name = name
        self.phoneNumber = phoneNumber
        self.email = email
        self.notes = notes
        return

    def display(self):
        return f"{self.name},  {self.phoneNumber},  {self.email},  {self.notes}"
    
    def csv_format(self):
         return f'{self.name}',f'{self.phoneNumber}',f'{self.email}',f'{self.notes}'

contactbook = {}
visual_seperator = ',  '


# Put Csv file into memory as a dict
with open("Contactbook.csv", 'r', newline='') as contactfile:
    csvreader = csv.reader(contactfile)

    csv_headers = next(csvreader)
    header_length = len(csv_headers)

    for line in csvreader: #hardcoded for now, unsure how to program using header_length and slicing
         contactbook[f"{line[0]}"] = Contact(line[0], line[1], line[2], line[3])
         
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

     contactbook[f"{name}"] = Contact(name, number, email, notes)

def lister():
     print(visual_seperator.join(csv_headers))
     for keys in contactbook:
          print(f"{contactbook[keys].display()}")

def search():
     name = input("Who are you looking for? ")

     if name in contactbook:
          print(f"Found! {contactbook[f"{name}"].display()}")
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

          csvwriter.writerow(csv_headers)

          for keys in contactbook:
               csvwriter.writerow(contactbook[keys].csv_format())

main()
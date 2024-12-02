#with open("Contactbook.txt", 'r+') as contactfile:
#    contactbook = contactfile.read()
#    pass

contactbook = {}

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
                      break
                 
def add():
     name = input("Who is it that you are adding? ")
     number = input("And their phone number? ")

     contactbook[f"{name}"] = f"{number}"

def lister():
     print(f"{contactbook.items()}")

def search():
     name = input("Who are you looking for? ")

     if name in contactbook:
          print(f"{contactbook[f"{name}"]}")
     else:
          print("Not found")

main()
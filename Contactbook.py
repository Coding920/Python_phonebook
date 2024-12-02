def main():
    print("Hello! You can: Add a new contact (add), list contacts (list), search contacts (search), quit (q)")
    
    while True:
            choice = input("What would you like to do? ")

            match choice:
                case "add":
                    #todo add func
                    return

                case "list":
                      #todo list func
                      return

                case "search":
                      #todo search func
                      return

                case "q":
                      #todo end prgrm
                      return
                 
def add():
     name = input("Who is it that you are adding? ")
     number = input("And their phone number? ")

     
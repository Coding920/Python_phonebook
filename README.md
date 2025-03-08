# Python Phonebook
### Video Demo: <https://youtu.be/xOh9LRb5yFo>
### Description: Gui Phonebook/Contact Program made with Python, Python's Tk interface, and SQLite3

My project has gone through serveral iterations while i've been working on it. I initially started it just wanting
to learn how I could save information and display it back out. This first iteration used a Command line 
interface and CSV files. Since it was such a small iteration, I won't be mentioning it here. The second iteration
implemented the sqlite database. The third iteration was the one to implement the Gui and has the most to talk about.

### The second iteration

The second iteration was when I brought on the sqlite database and had to learn all of the little odd things
with the module. The first time i was working with it, I ran into problems both with getting the data 
ready to be used, and with needing to learn about how to learn more in SQL.

Firstly, the data that the ".execute()" method wants is a tuple. I would try to pass in regular strings, etc.
in but it would only work some of the time. At first it would give me an error about wanting "string-literals".
So after some research, I learned you can make a string into a string literal by surrounding it in \[brackets\].
This was an alright temporary fix. After reading the documentation some more though, it wanted the data to be 
passed in as a tuple. This also makes it tremendously easier to pass in multiple variables into statements that
take mulitple.

Secondly, at the time of this second iteration, I wan't so experienced with SQL. So I had to learn about structuring queries,
I learned the hard way that primary unique keys are very important, and I also had to learn about how to
structure queries to create tables. What stood out the most to me was, at the beginning, my table was made
with a row id. I should've had the foresight to keep it but at that moment in time, it was actually giving
me more issues than I thought it was worth. I don't quite remember the issue but the removal of the key
ended up being far more of an issue than just figuring out my initial problem with the row id.

The biggest issue with no row id was that the only way I could delete a contact was by the name, number,
or email. This meant that if you wanted to delete a contact and another contact had some of the duplication,
then you'd delete both contacts. Refactoring it back to having a primary key was quite the pain.

### The third and most recent iteration

This was by far the hardest iteration as I had to carry over all of my logic onto a Gui. Tk is very hard
to work with as, unlike Html and Css, there aren't nearly as many resources and the support for it is more limited.
It's also not as straight forward to write as Css. First you have to declare the "widget" that you want,
such as a button, an entry box, a label, etc., and then you have to place it with either "place", "grid", 
or "pack". Grid is the best and most modern one but you still have to place everything in the column and row
that is needed. That its self is pretty straight forward but when it comes to styling and getting things to function,
it's no where near as simple as html. 

For things to function, you have to use special variables associated with the Tk module, mainly the 
"Tk.StringVar". This variable gives you a method, ".get()", in order to actually grab the variable stored there.
This created quite the confusion when i was trying to access values of regular string variables, but couldn't get
proper values out of it other than an empty string.

As well, when it came to stylizing everything, Tk doesn't have the most straight forward methods. One possibilty
is creating a "Tk.Style" instance and then trying to style everything by widget type. I say "trying" because 
trying to find the actual resources for the different attributes you can style was very difficult for me.

Then once the program started getting bigger, widget names started becoming more messy. Now, as I didn't
know quite how many widget names I was going to need. So, right after making the contact list, I had
some decisions. I could either continue making everything on the global level and let things just keep getting 
messier and messier; simply so I could get the program made a little sooner.

Alternatively, I could make different larger sized sections into their own classes and learn how to do that.
So I made the contact list into it's own class called a listbox (not to be confused with tk's listbox),
I made the root/main window into its own class, and I made the add contact page and the contact display page
into their own class as well. It really cut down on the naming neccesarry and made the code a lot more
maintainable and readable versus the alternative.

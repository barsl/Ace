from tkinter import *
from tkinter import *
from tkinter import ttk
from tkinter import font

# create a new TK window
window = Tk()
# we dont want people to be able to change the size of the actual window
window.resizable(width=False, height=False)
window.title("Login")
# dimensions of the window
window.geometry("400x300")

appHighlightFont = font.Font(family='Helvetica', size=14, weight='bold')
regularFont = font.Font(family='Helvetica', size=12, weight='normal')
loginlbl = ttk.Label(window, text ="Please Log In: ", font=appHighlightFont)

# create the username and password fields

username_label = Label(window, text="Username", font=regularFont)
username_entry = Entry(window, show="email address")
password_label = Label(window, text="Password", font=regularFont)
password_entry = Entry(window, show="*")

login_btn = Button(text="Login")

# use the grid layout managing function
# customize columns and rows
# empty label to create some space between the top 
# the entry labels
empty_label = Label(window, text="").grid(row=0, column=0, columnspan=5)
# place our created label inside the
loginlbl.grid(row=1, column=2, columnspan=2)
username_label.grid(row=5, column=3, columnspan=2)
username_entry.grid(row=5, column=5)
password_label.grid(row=6, column=3, columnspan=2)
password_entry.grid(row=6, column=5)
login_btn.grid(row=7, column=3)

window.mainloop()

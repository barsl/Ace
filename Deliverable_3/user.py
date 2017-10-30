import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db




APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")

class AddUser(tk.Frame):
    '''Creates a login screen, which will be the 
    first screen of our Application'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller
        self.credentials = {'Username' : '','Password': ''}
        
        '''creates the entry fields'''
        # login text
        loginlbl = ttk.Label(self, text="Please enter details for new user",
                             font=REGULAR_FONT, foreground="red")     
        
        # create the username and password lables and entries
        role_label = tk.Label(self, text="Role", font=REGULAR_FONT)
        name_label = tk.Label(self, text="Name", font=REGULAR_FONT)
        email_label = tk.Label(self, text="Email", font=REGULAR_FONT)
        password_label = tk.Label(self, text="Password", font=REGULAR_FONT) 
        
        self.role_entry = tk.Entry(self)
        self.name_entry = tk.Entry(self)
        self.email_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self)
        
        self.add_user_button = Button(self, text="Add User", font=REGULAR_FONT, 
                                      command=self.add_user)
        
        # pack elements
        loginlbl.pack() 
        role_label.pack()
        self.role_entry.pack()
        name_label.pack()
        self.name_entry.pack()
        email_label.pack()
        self.email_entry.pack()
        password_label.pack()
        self.password_entry.pack()
        tk.Label(self, text="\n\n\n\n").pack()
        self.add_user_button.pack()
        
    def add_user(self):
        conn = db.sqlite3.connect('ace.db')
        # print(self.user_name)
        number = db.add_user(self.role_entry.get(), self.name_entry.get(),
                      self.email_entry.get(), self.password_entry.get(), conn)
        self.role_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.password_entry.delete(0, END)   
        showinfo("Success", "ID of new user is: " + str(number))
        self.cont.show_frame(HomeScreen)

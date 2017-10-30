import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db


import sqlite3

conn = sqlite3.connect('ace.db')

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")

class User():
    def __init__(self, uid):
        user = db.get_user_details(conn, uid)[0]
        self.uid = user[0]
        self.role = user[1]
        self.name = user[2]
        self.email = user[3]
        self.password = user[4]
        
    def get_uid(self):
        return self.uid
    def get_role(self):
        return self.role      
    def get_name(self):
        return self.name
    def get_email(self):
        return self.email
    def get_password(self):
        return self.password  
    
    def remove_user(self, uid):
        db.remove_user(uid, conn)
        print("user removed: " + str(uid))

class UserInterface(tk.Frame):
    '''Creates a login screen, which will be the 
    first screen of our Application'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller
        self.credentials = {'Username' : '','Password': ''}
        
        '''creates the  fields'''
        ttk.Label(self, text="User Database Management\n",
                             font=REGULAR_FONT, foreground="Green").grid(
                                 row=0, column=0)
        self.roles = []
        self.names = []
        self.emails = []
        self.updates = []
        self.deletes = []
        tk.Label(self, text="Role", font=REGULAR_FONT).grid(row=1, column=0)
        tk.Label(self, text="Name", font=REGULAR_FONT).grid(row=1, column=1)
        tk.Label(self, text="Email", font=REGULAR_FONT).grid(row=1, column=2)
        
        self.gen_rows()
        
    def gen_rows(self):
        # get a list of all the user ids in the database
        ids = db.get_user_ids(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            # create new entries and add to corresponding lists
            # assign name to each entry to include the user id
            role_entry = tk.Entry(self, name="r"+str(uid))
            name_entry = tk.Entry(self, name="n"+str(uid))
            email_entry = tk.Entry(self, name="e"+str(uid))
            self.roles.append(role_entry)
            self.names.append(name_entry)
            self.emails.append(email_entry)            
            # create new buttons and add to corresponding lists
            # assign name to each button to include the user id
            update_button = Button(self, text="Update", name="u"+str(uid), font=REGULAR_FONT)
            delete_button = Button(self, text="Delete", name="d"+str(uid), font=REGULAR_FONT)
            self.updates.append(update_button)
            self.deletes.append(delete_button)
            # set everything nicely on the grid using an iterator i
            role_entry.grid(row=i+2, column=0)
            name_entry.grid(row=i+2, column=1)
            email_entry.grid(row=i+2, column=2)
            update_button.grid(row=i+2, column=3)
            delete_button.grid(row=i+2, column=4)
            i += 1
            
            # create new user object
            user = User(uid)
            # set each entry with the corresponding value
            role_entry.insert(0, user.get_role())
            name_entry.insert(0, user.get_name())
            email_entry.insert(0, user.get_email())
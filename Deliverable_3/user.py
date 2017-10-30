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
    '''
    A user object which is used to interact with users' data,
    and perform actions that affect users' data
    '''
    def __init__(self, uid):
        '''
        uid is the user id of the student we want to create
        '''
        # get user details from database
        user = db.get_user_details(conn, uid)[0]
        # assign corresponding values to variables
        self.uid = user[0]
        self.role = user[1]
        self.name = user[2]
        self.email = user[3]
        self.password = user[4]
        
    # getters and setters
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

class UserInterface(tk.Frame):
    '''
    Objects of this type are used to genereate the GUI for the User Database
    Management screen
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller
        
        # label at top of the frame
        ttk.Label(self, text="User Database Management\n",
                             font=REGULAR_FONT, foreground="Green").grid(
                                 row=0, column=1)
        # dictionaries to contain the widgets and associate widget to
        # correspondin user id
        self.roles = {}
        self.names = {}
        self.emails = {}
        self.updates = {}
        self.deletes = {}
        
        # the 3 static lables that are always there
        tk.Label(self, text="Role", font=REGULAR_FONT).grid(row=1, column=0)
        tk.Label(self, text="Name", font=REGULAR_FONT).grid(row=1, column=1)
        tk.Label(self, text="Email", font=REGULAR_FONT).grid(row=1, column=2)
        
        # get a list of all existing user ids
        self.user_ids = db.get_user_ids(conn)
        
        # generate all the dynamically generaterd widget rows
        self.gen_rows()
        
        # configure clicking function for all the delete buttons
        for uid in self.user_ids:
            self.deletes[uid].config(command=lambda j=uid: self.del_user(j))
        # configure clicking function for all the update buttons
        for uid in self.user_ids:
            self.updates[uid].config(command=lambda j=uid: self.up_user(j))           
        
    def gen_rows(self):
        # get a list of all the user ids in the database
        ids = db.get_user_ids(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            # create new entries 
            role_entry = tk.Entry(self)
            name_entry = tk.Entry(self)
            email_entry = tk.Entry(self)
            # add to corresponding dictonaries with user ids as keys
            self.roles[uid] = role_entry
            self.names[uid] = name_entry    
            self.emails[uid] = email_entry
          
            # create new buttons
            update_button = Button(self, text="Update", font=REGULAR_FONT)
            delete_button = Button(self, text="Delete", font=REGULAR_FONT)
            # add to corresponding dictonaries with user ids as keys        
            self.deletes[uid] = delete_button
            self.updates[uid] = update_button
            
            # set everything nicely on the grid using an iterator i
            role_entry.grid(row=i+2, column=0)
            name_entry.grid(row=i+2, column=1)
            email_entry.grid(row=i+2, column=2)
            update_button.grid(row=i+2, column=4)
            delete_button.grid(row=i+2, column=5)
            i += 1
            
            # create new user object to contain user info
            user = User(uid)
            # set each entry with the corresponding value from the user object
            role_entry.insert(0, user.get_role())
            name_entry.insert(0, user.get_name())
            email_entry.insert(0, user.get_email())
            
        
            
    def del_user(self, button):
        db.remove_user(button, conn)
        showinfo("Success", "User #" + str(button) + " has been deleted")
    
    def up_user(self, button):
        new_role = self.roles[button].get()
        new_name = self.names[button].get()
        new_email = self.emails[button].get()
        db.update_user_role(button, new_role, conn)
        db.update_user_name(button, new_name, conn)
        db.update_user_email(button, new_email, conn)
        showinfo("Success", "User #" + str(button) + " has been updated")

        
        

 
            
          
        
        
            
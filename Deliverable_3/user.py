import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
import sqlite3

conn = sqlite3.connect('ace.db')

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
NICE_BLUE = "#3399FF"

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
        tk.Label(self, text="Role", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=0)
        tk.Label(self, text="Name", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=1)
        tk.Label(self, text="Email", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=2)
        
        # create first row of entries for add_user function
        self.role_entry = tk.Entry(self, font=REGULAR_FONT)
        self.name_entry = tk.Entry(self, font=REGULAR_FONT)
        self.email_entry = tk.Entry(self, font=REGULAR_FONT)   
        # set everything nicely on the grid
        self.role_entry.grid(row=2, column=0)
        self.name_entry.grid(row=2, column=1)
        self.email_entry.grid(row=2, column=2)  
        # create add user button
        add_user_button = Button(self, text="Add User", font=REGULAR_FONT)
        add_user_button.grid(row=2, column=3, columnspan=2)
        # set button method to add_user
        add_user_button.config(command=lambda : self.add_user())
        
        # generate all the dynamically generaterd widget rows
        self.gen_rows()
        
        # enable clicking functionality for all the buttons
        self.enable_buttons()
        
          
        
    def gen_rows(self):
        # get a list of all the user ids in the database
        ids = db.get_user_ids(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            # create new entries 
            role_entry = tk.Entry(self, font=REGULAR_FONT)
            name_entry = tk.Entry(self, font=REGULAR_FONT)
            email_entry = tk.Entry(self, font=REGULAR_FONT)
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
            role_entry.grid(row=i+3, column=0)
            name_entry.grid(row=i+3, column=1)
            email_entry.grid(row=i+3, column=2)
            update_button.grid(row=i+3, column=3)
            delete_button.grid(row=i+3, column=4)
            i += 1
            
            # create new user object to contain user info
            user = User(uid)
            # set each entry with the corresponding value from the user object
            role_entry.insert(0, user.get_role())
            name_entry.insert(0, user.get_name())
            email_entry.insert(0, user.get_email())
            
        
            
    def del_user(self, button):
        '''
        delete a user from the database and show a success popup
        '''
        # remove user from databse
        db.remove_user(button, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "User #" + str(button) + " has been deleted")
    
    def up_user(self, button):
        '''
        delete a user details in the database and show a success popup
        '''        
        # get new parameters from entry widgets in the dictionaries
        new_role = self.roles[button].get()
        new_name = self.names[button].get()
        new_email = self.emails[button].get()
        # update the database with new entries
        db.update_user_role(button, new_role, conn)
        db.update_user_name(button, new_name, conn)
        db.update_user_email(button, new_email, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "User #" + str(button) + " has been updated")
        
    def add_user(self):
        '''
        delete a user from the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        new_role = self.role_entry.get()
        new_name = self.name_entry.get()
        new_email = self.email_entry.get()        
        # add new user to databse and save his id number
        uid = db.add_user(new_role, new_name, new_email, "", conn)
        # show popup
        self.refresh()
        # clear entries
        self.role_entry.delete(0, 'end')
        self.name_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')        
        showinfo("Success", "User #" + str(uid) + " has been added to database")
        

    def refresh(self):
        for role in list(self.roles.items()):
            role[1].destroy()
        for name in list(self.names.items()):
            name[1].destroy()
        for email in list(self.emails.items()):
            email[1].destroy()
        for update in list(self.updates.items()):
            update[1].destroy()
        for delete in list(self.deletes.items()):
            delete[1].destroy()
        self.gen_rows()
        self.enable_buttons()
        
    def enable_buttons(self):
        # get a list of all existing user ids
        user_ids = db.get_user_ids(conn)        
        # configure clicking function for all the delete buttons
        for uid in user_ids:
            self.deletes[uid].config(command=lambda j=uid: self.del_user(j))
        # configure clicking function for all the update buttons
        for uid in user_ids:
            self.updates[uid].config(command=lambda j=uid: self.up_user(j))         
        
        

 
            
          
        
        
            
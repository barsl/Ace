import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from problem import *
from user import *
import ast
import datetime

import matplotlib
matplotlib.use("TkAgg")
##from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')

class LeaderboardGraph(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI displaying a leaderboard
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller

        # label at top of the frame
        new_label = self.create_label(self, "Leaderboard\n",
                                      TITLE_FONT,
                                      "Red").grid(row=0, column=1,pady=10)
        # dictionaries to contain the widgets and associate widget to
        # corresponding user id
        self.names = {}
        ##self.emails = {}
        self.grades = {}
        self.times = {}

        ##self.updates = {}
        ##self.deletes = {}

        ## create add user button
        ##add_user_button = self.create_button(self, "Add User")
        ## set button method to add_user
        ##add_user_button["command"] = lambda : self.add_user()
        ##add_user_button.grid(row=2, column=3)
        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda : controller.show_frame('HomeScreen')
        back_button.grid(row=0, column=3)
        # generate all the dynamically generaterd widget rows
        self.gen_rows()

        # enable clicking functionality for all the buttons
        self.enable_buttons()



    def gen_rows(self):
        # get a list of all the user ids in the database
        ids = db.get_user_by_grade(conn)
        #Setup graph
        x_ax = []
        y_ax = []
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            user = db.get_user_details(conn, uid)

            x_ax.append(str(i))
            y_ax.append(user[0][5])
            i+=1

            """# create new entries
            user = db.get_user_details(conn, uid)
            rank_label = Label(self, font=REGULAR_FONT, text=i+1)
            name_label = Label(self, font=REGULAR_FONT, text=user[0][2])
            ##email_label = Label(self, font=REGULAR_FONT, text=user[0][3])
            grade_label = Label(self, font=REGULAR_FONT, text=str(user[0][5]) + "%")
            time_label = Label(self, font=REGULAR_FONT, text=self.datetimeFormat(user[0][6]))
            # add to corresponding dictonaries with user ids as keys
            self.names[uid] = name_label
            ##self.emails[uid] = email_label
            self.grades[uid] = grade_label
            self.times[uid] = time_label

            i += 1"""

        fig = Figure(figsize=(5,5), dpi=100)
        a = fig.add_subplot(111)
        a.plot(x_ax, y_ax)
        canvas = FigureCanvasTkAgg(fig, self)
        ##canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas.get_tk_widget().grid(row=1, column=0)
        canvas._tkcanvas.grid(row=1, column=0)

    """def del_user(self, button):
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
        new_role = self.names[button].get()
        new_name = self.emails[button].get()
        new_email = self.grades[button].get()
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
        new_role = self.entry_fields["Role"].get()
        new_name = self.entry_fields["Name"].get()
        new_email = self.entry_fields["Email"].get()
        # add new user to databse and save his id number
        uid = db.add_user(new_role, new_name, new_email, "", conn)
        # show popup
        self.refresh()
        # clear entries
        self.entry_fields["Role"].set('')
        self.entry_fields["Name"].set('')
        self.entry_fields["Email"].set('')
        showinfo("Success", "User #" + str(uid ) + " has been added to database")"""


    def refresh(self):
        for name in list(self.names.items()):
            name[1].destroy()
        ##for email in list(self.emails.items()):
        ##    email[1].destroy()
        for grade in list(self.grades.items()):
            grade[1].destroy()
        for time in list(self.times.items()):
            time[1].destroy()
        ##for update in list(self.updates.items()):
        ##    update[1].destroy()
        ##for delete in list(self.deletes.items()):
        ##    delete[1].destroy()
        self.gen_rows()
        self.enable_buttons()

    def enable_buttons(self):
        # get a list of all existing user ids
        user_ids = db.get_user_ids(conn)
        # configure clicking function for all the delete buttons
        ##for uid in user_ids:
        ##    self.deletes[uid].config(command=lambda j=uid: self.del_user(j))
        # configure clicking function for all the update buttons
        ##for uid in user_ids:
        ##    self.updates[uid].config(command=lambda j=uid: self.up_user(j))

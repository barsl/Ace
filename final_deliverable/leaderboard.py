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

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 16, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')

class Leaderboard(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI displaying a leaderboard
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller

        self.labels = ["Rank", "Name", "Email", "Grade", "Time"]
        # label at top of the frame
        new_label = self.create_label(self, "Leaderboard\n",
                                      TITLE_FONT,
                                      "Red").grid(row=0, column=1,pady=10) 
        # dictionaries to contain the widgets and associate widget to
        # corresponding user id
        self.names = {}
        self.emails = {}
        self.grades = {}
        self.times = {}

        
        # the 3 static lables that are always there
        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, APP_HIGHLIGHT_FONT,
                                          NICE_BLUE).grid(row=1, column=i)
            # create first row of entries for add_problem function
            # set everything nicely on the grid
            # create first row of entries for add_user function
            # set everything nicely on the grid            

            i += 1         

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
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            # create new entries
            user = db.get_user_details(conn, uid)
            rank_label = self.create_label(self, text=i+1, font=REGULAR_FONT)
            name_label = self.create_label(self, text=user[0][2], font=REGULAR_FONT)
            email_label = self.create_label(self, text=user[0][3], font=REGULAR_FONT)
            grade_label = self.create_label(self, text=user[0][5], font=REGULAR_FONT)
            time_label = self.create_label(self,  text=user[0][6], font=REGULAR_FONT)
            # add to corresponding dictonaries with user ids as keys
            self.names[uid] = name_label
            self.emails[uid] = email_label    
            self.grades[uid] = grade_label
            self.times[uid] = time_label
    
            # set everything nicely on the grid using an iterator i
            rank_label.grid(row=i+3, column=0)
            name_label.grid(row=i+3, column=1)
            email_label.grid(row=i+3, column=2)
            grade_label.grid(row=i+3, column=3)
            time_label.grid(row=i+3, column=4)

            i += 1        

    def refresh(self):
        for name in list(self.names.items()):
            name[1].destroy()
        for email in list(self.emails.items()):
            email[1].destroy()
        for grade in list(self.grades.items()):
            grade[1].destroy()
        for time in list(self.times.items()):
            time[1].destroy()

        self.gen_rows()
        self.enable_buttons()
        
    def enable_buttons(self):
        # get a list of all existing user ids
        user_ids = db.get_user_ids(conn)        


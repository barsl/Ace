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

from main import *

#import matplotlib
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.figure import Figure
#matplotlib.use("TkAgg")

YRSEC = 31556952
MONSEC = 2629746
DAYSEC = 86400
HRSEC = 3600
MINSEC = 60

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')

class Leaderboard(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI displaying a leaderboard
    '''
    def __init__(self, parent, controller, uid=None):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        ##self.labels = ["Rank", "Name", "Email", "Grade", "Time (Day - H:M:S)"]
        self.labels = ["Rank", "Name", "Grade", "Time (Day - H:M:S)"]
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

        # the 3 static lables that are always there
        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=1, column=i)
            # create first row of entries for add_problem function
            # set everything nicely on the grid
            # create first row of entries for add_user function
            # set everything nicely on the grid
            ##new_entry = self.create_entry(self, label,
            ##                              REGULAR_FONT).grid(row=2, column=i)
            i += 1
        ## create add user button
        ##add_user_button = self.create_button(self, "Add User")
        ## set button method to add_user
        ##add_user_button["command"] = lambda : self.add_user()
        ##add_user_button.grid(row=2, column=3)

        # Determine the current user's type and navigate back to the proper
        # main menu
        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda : controller.show_frame(self.x)
        back_button.grid(row=0, column=3)

        # generate all the dynamically generaterd widget rows
        self.gen_rows()

        # enable clicking functionality for all the buttons
        self.enable_buttons()

    def set_back(self, x):
        self.x = x


    def gen_rows(self):
        # get a list of all the user ids in the database
        ids = db.get_user_by_grade(conn)

        # Setup graph
        x_ax = []
        y_ax = []

        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            # create new entries
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

            # set everything nicely on the grid using an iterator i
            rank_label.grid(row=i+3, column=0)
            name_label.grid(row=i+3, column=1)
            ##email_label.grid(row=i+3, column=2)
            grade_label.grid(row=i+3, column=2)
            time_label.grid(row=i+3, column=3)

            # Append for graph
            x_ax.append(str(i) + "\n" + str(user[0][2]))
            y_ax.append(user[0][5])
            i+=1

        fig = Figure(figsize=(5,6), dpi=100)
        graph = fig.add_subplot(111)
        graph.set_title("Leaderboard Graph")
        graph.set_xlabel("Rank with name")
        graph.set_ylabel("Grade in %")
        graph.plot(x_ax, y_ax)

        canvas = FigureCanvasTkAgg(fig, self)
        ##canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        canvas.get_tk_widget().grid(row=i+4, column=0, columnspan=4)
        canvas._tkcanvas.grid(row=i+4, column=0, columnspan=4)

        """# Add toolbar
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.grid(row=i+4, column=0, columnspan=4)"""

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

    def datetimeFormat(self, input_sec):
        """
        Returns inputted seconds in the following format:
        "Day - Hour:Minute:Second"
        """
        day = input_sec // DAYSEC
        hour = (input_sec % DAYSEC) // HRSEC
        minute = ((input_sec % DAYSEC) % HRSEC) // MINSEC
        sec = ((input_sec % DAYSEC) % HRSEC) % MINSEC
        return str(day) + " - " + str(hour) + ":" + str(minute) + ":" + str(sec)

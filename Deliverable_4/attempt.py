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

class Attempt():
    '''
    An attempt object which is used to interact with attempts' data,
    and perform actions that affect attempts' data
    '''
    def __init__(self, aNum):
        '''
        aid is the attempt id of the student we want to create
        '''
        # get attempt details from database
        attempt = db.get_attempt_details(conn, aid)[0]
        # assign corresponding values to variables
        self.aNum = attempt[0]
        self.aid = attempt[1]
        self.qids = attempt[2]
        self.user = attempt[3]
        self.date = attempt[4]
        self.mark = attempt[5]
        self.answers = attempt[6]
        
    # getters and setters
    def get_aNum(self):
        return self.aNum    
    def get_aid(self):
        return self.aid
    def get_qids(self):
        return self.qid
    def get_user(self):
        return self.user
    def get_date(self):
        return self.date
    def get_mark(self):
        return self.mark
    def get_answers(self):
        return self.answers

class AttemptInterface(tk.Frame):
    '''
    Objects of this type are used to genereate the GUI for the attempt Database
    Management screen
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        # label at top of the frame
        ttk.Label(self, text="Attempts Database Management\n",
                             font=REGULAR_FONT, foreground="Green").grid(
                                 row=0, column=1)
        # dictionaries to contain the widgets and associate widget to
        # corresponding attempt id
        self.attempts = {}
        self.aid = {}
        self.qids = {}
        self.users = {}
        self.dates = {}
        self.marks = {}
        self.answers = {}
        # the buttons
        self.updates = {}
        self.deletes = {}

        # the static labels that are always there
        tk.Label(self, text="#", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=0)
        tk.Label(self, text="Assignment", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=1)
        tk.Label(self, text="qIds", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=2)
        tk.Label(self, text="User", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=3)
        tk.Label(self, text="Date", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=4)
        tk.Label(self, text="Mark", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=5)
        tk.Label(self, text="Answer", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=6)        

        # create first row of entries for add_attempt function
        self.attempt_entry = tk.Entry(self, font=REGULAR_FONT)
        import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
import sqlite3
##from attempt import *
conn = sqlite3.connect('ace.db')

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
NICE_BLUE = "#3399FF"

class Attempt():
    '''
    An attempt object which is used to interact with attempts' data,
    and perform actions that affect attempts' data
    '''
    def __init__(self, aNum):
        '''
        aid is the attempt id of the student we want to create
        '''
        # get attempt details from database
        attempt = db.get_attempt_details(conn, aNum)[0]
        # assign corresponding values to variables
        self.aNum = attempt[0]
        self.aid = attempt[1]
        self.qids = attempt[2]
        self.user = attempt[3]
        self.date = attempt[4]
        self.mark = attempt[5]
        self.answers = attempt[6]
        
    # getters and setters
    def get_aNum(self):
        return self.aNum    
    def get_aid(self):
        return self.aid
    def get_qids(self):
        return self.qids
    def get_user(self):
        return self.user
    def get_date(self):
        return self.date
    def get_mark(self):
        return self.mark
    def get_answers(self):
        return self.answers

class AttemptInterface(tk.Frame):
    '''
    Objects of this type are used to genereate the GUI for the attempt Database
    Management screen
    '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.cont = controller

        # label at top of the frame
        ttk.Label(self, text="Attempts Database Management\n",
                             font=REGULAR_FONT, foreground="Green").grid(
                                 row=0, column=1)
        # dictionaries to contain the widgets and associate widget to
        # corresponding attempt id
        self.attempts = {}
        self.aids = {}
        self.qids = {}
        self.users = {}
        self.dates = {}
        self.marks = {}
        self.answers = {}
        # the buttons
        self.updates = {}
        self.deletes = {}

        # the static labels that are always there
        tk.Label(self, text="#", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=0)
        tk.Label(self, text="Assignment", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=1)
        tk.Label(self, text="qIds", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=2)        
        tk.Label(self, text="User", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=3)
        tk.Label(self, text="Date", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=4)
        tk.Label(self, text="Mark", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=5)
        tk.Label(self, text="Answers", font=REGULAR_FONT, fg=NICE_BLUE).grid(
            row=1, column=6)        

        # create first row of entries for add_attempt function
        self.attempt_entry = tk.Entry(self, font=REGULAR_FONT)
        self.aid_entry = tk.Entry(self, font=REGULAR_FONT)
        self.qids_entry = tk.Entry(self, font=REGULAR_FONT)
        self.user_entry = tk.Entry(self, font=REGULAR_FONT)
        self.date_entry = tk.Entry(self, font=REGULAR_FONT)
        self.mark_entry = tk.Entry(self, font=REGULAR_FONT)
        self.answers_entry = tk.Entry(self, font=REGULAR_FONT)
        # set everything nicely on the grid
        self.attempt_entry.grid(row=2, column=0)
        self.aid_entry.grid(row=2, column=1)
        self.qids_entry.grid(row=2, column=2)
        self.user_entry.grid(row=2, column=3)
        self.date_entry.grid(row=2, column=4)
        self.mark_entry.grid(row=2, column=5)
        self.answers_entry.grid(row=2, column=6)
        # create add attempt button
        add_attempt_button = Button(self, text="Add attempt", font=REGULAR_FONT)
        add_attempt_button.grid(row=2, column=7, columnspan=2)
        # set button method to add_attempt
        add_attempt_button.config(command=lambda : self.add_attempt())

        # generate all the dynamically generaterd widget rows
        self.gen_rows()

        # enable clicking functionality for all the buttons
        self.enable_buttons()

    def gen_rows(self):
        # get a list of all the attempt ids in the database
        ids = db.get_attempt_ids(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for aNum in ids:
            # create new entries
            attempt_entry = tk.Entry(self, font=REGULAR_FONT)
            aid_entry = tk.Entry(self, font=REGULAR_FONT)
            qids_entry = tk.Entry(self, font=REGULAR_FONT)
            user_entry = tk.Entry(self, font=REGULAR_FONT)
            date_entry = tk.Entry(self, font=REGULAR_FONT)
            mark_entry = tk.Entry(self, font=REGULAR_FONT)
            answers_entry = tk.Entry(self, font=REGULAR_FONT)
            # add to corresponding dictonaries with attempt ids as keys
            self.attempts[aNum] = attempt_entry
            self.qids[aNum] = qids_entry
            self.users[aNum] = user_entry
            self.dates[aNum] = date_entry
            self.marks[aNum] = mark_entry
            self.answers[aNum] = answers_entry

            # create new buttons
            update_button = Button(self, text="Update", font=REGULAR_FONT)
            delete_button = Button(self, text="Delete", font=REGULAR_FONT)
            # add to corresponding dictonaries with attempt ids as keys
            self.deletes[aNum] = delete_button
            self.updates[aNum] = update_button

            # set everything nicely on the grid using an iterator i
            attempt_entry.grid(row=i+3, column=0)
            aid_entry.grid(row=i+3, column=1)
            qids_entry.grid(row=i+3, column=2)
            user_entry.grid(row=i+3, column=3)
            date_entry.grid(row=i+3, column=4)
            mark_entry.grid(row=i+3, column=5)
            answers_entry.grid(row=i+3, column=6)
            
            update_button.grid(row=i+3, column=7)
            delete_button.grid(row=i+3, column=8)
            i += 1

            # create new attempt object to contain attempt info
            attempt = attempt(aNum)
            # set each entry with the corresponding value from the attempt object
            attempt_entry.insert(0, attempt.get_aNum())
            aid_entry.insert(0, attempt.get_aid())
            qids_entry.insert(0, attempt.get_qids())
            user_entry.insert(0, attempt.get_user())
            date_entry.insert(0, attempt.get_date())
            mark_entry.insert(0, attempt.get_mark())
            answers_entry.insert(0, attempt.get_answer())

    def del_attempt(self, button):
        '''
        delete a attempt from the database and show a success popup
        '''
        # remove attempt from databse
        db.remove_attempt(button, conn)

        self.refresh()

        # show popup
        showinfo("Success", "attempt #" + str(button) + " has been deleted")

    def up_attempt(self, button):
        '''
        delete a attempt details in the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        ##new_attempt = self.attempts[button].get()
        ##new_aid = self.aids[button].get()
        ##new_user = self.users[button].get()
        new_date = self.dates[button].get()
        new_mark = self.marks[button].get()
        new_answers = self.answers[button].get()
        # update the database with new entries
        ##db.update_attempt_aNum(button, new_attempt, conn)
        ##db.update_attempt_assignment(button, new_aid, conn)
        ##db.update_attempt_user(button, new_user, conn)
        db.update_attempt_date(button, new_date, conn)
        db.update_attempt_mark(button, new_mark, conn)
        db.update_attempt_answers(button, new_answers, conn)

        self.refresh()

        # show popup
        showinfo("Success", "attempt #" + str(button) + " has been updated")

    def add_attempt(self):
        '''
        delete an attempt from the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        new_aNum = self.attempt_entry.get()
        new_aid = self.aid_entry.get()
        new_qids = self.qids_entry.get()
        new_user = self.user_entry.get()
        new_date = self.date_entry.get()
        new_mark = self.mark_entry.get()
        new_answers = self.answers_entry.get()
        
        # add new attempt to databse and save his id number
        aid = db.add_attempt(new_aNum, new_aid, new_user, new_date, new_mark, new_answers, conn)
        # show popup
        self.refresh()
        # clear entries
        self.attempt_entry.delete(0, 'end')
        self.aid_entry.delete(0, 'end')
        self.user_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.mark_entry.delete(0, 'end')
        self.answers_entry.delete(0, 'end')
        showinfo("Success", "attempt #" + str(aid) + " has been added to database")

    def refresh(self):
        for aNum in list(self.attempts.items()):
            aNum[1].destroy()
        for aid in list(self.aids.items()):
            aid[1].destroy()
        for user in list(self.users.items()):
            user[1].destroy()
        for date in list(self.dates.items()):
            date[1].destroy()
        for mark in list(self.marks.items()):
            mark[1].destroy()
        for answers in list(self.answers.items()):
            answers[1].destroy()
            
        for update in list(self.updates.items()):
            update[1].destroy()
        for delete in list(self.deletes.items()):
            delete[1].destroy()
        self.gen_rows()
        self.enable_buttons()

    def enable_buttons(self):
        # get a list of all existing attempt ids
        attempt_ids = db.get_attempt_ids(conn)
        # configure clicking function for all the delete buttons
        for aNum in attempt_ids:
            self.deletes[aNum].config(command=lambda j=aNum: self.del_attempt(j))
        # configure clicking function for all the update buttons
        for aNum in attempt_ids:
            self.updates[aNum].config(command=lambda j=aNum: self.up_attempt(j))

        self.attempt_entry = tk.Entry(self, font=REGULAR_FONT)
        self.aid_entry = tk.Entry(self, font=REGULAR_FONT)
        self.user_entry = tk.Entry(self, font=REGULAR_FONT)
        self.date_entry = tk.Entry(self, font=REGULAR_FONT)
        self.mark_entry = tk.Entry(self, font=REGULAR_FONT)
        self.answers_entry = tk.Entry(self, font=REGULAR_FONT)
        # set everything nicely on the grid
        self.attempt_entry.grid(row=2, column=0)
        self.aid_entry.grid(row=2, column=1)
        self.user_entry.grid(row=2, column=2)
        self.date_entry.grid(row=2, column=3)
        self.mark_entry.grid(row=2, column=4)
        self.answers_entry.grid(row=2, column=5)
        # create add attempt button
        add_attempt_button = Button(self, text="Add attempt", font=REGULAR_FONT)
        add_attempt_button.grid(row=2, column=6, columnspan=2)
        # set button method to add_attempt
        add_attempt_button.config(command=lambda : self.add_attempt())

        # generate all the dynamically generaterd widget rows
        self.gen_rows()

        # enable clicking functionality for all the buttons
        self.enable_buttons()

    def gen_rows(self):
        # get a list of all the attempt ids in the database
        ids = db.get_attempt_ids(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for aNum in ids:
            # create new entries
            attempt_entry = tk.Entry(self, font=REGULAR_FONT)
            aid_entry = tk.Entry(self, font=REGULAR_FONT)
            qids_entry = tk.Entry(self, font=REGULAR_FONT)
            user_entry = tk.Entry(self, font=REGULAR_FONT)
            date_entry = tk.Entry(self, font=REGULAR_FONT)
            mark_entry = tk.Entry(self, font=REGULAR_FONT)
            answers_entry = tk.Entry(self, font=REGULAR_FONT)
            # add to corresponding dictonaries with attempt ids as keys
            self.attempts[aNum] = attempt_entry
            self.users[aNum] = user_entry
            self.dates[aNum] = date_entry
            self.marks[aNum] = mark_entry
            self.answers[aNum] = answers_entry

            # create new buttons
            update_button = Button(self, text="Update", font=REGULAR_FONT)
            delete_button = Button(self, text="Delete", font=REGULAR_FONT)
            # add to corresponding dictonaries with attempt ids as keys
            self.deletes[aNum] = delete_button
            self.updates[aNum] = update_button

            # set everything nicely on the grid using an iterator i
            attempt_entry.grid(row=i+3, column=0)
            aid_entry.grid(row=i+3, column=1)
            qids_entry.grid(row=i+3, column=2)
            user_entry.grid(row=i+3, column=3)
            date_entry.grid(row=i+3, column=4)
            mark_entry.grid(row=i+3, column=5)
            answers_entry.grid(row=i+3, column=6)
            
            update_button.grid(row=i+3, column=7)
            delete_button.grid(row=i+3, column=8)
            i += 1

            # create new attempt object to contain attempt info
            attempt = Attempt(aNum)
            # set each entry with the corresponding value from the attempt object
            attempt_entry.insert(0, attempt.get_aNum())
            aid_entry.insert(0, attempt.get_aid())
            qids_entry.insert(0, attempt.get_qids())
            user_entry.insert(0, attempt.get_user())
            date_entry.insert(0, attempt.get_date())
            mark_entry.insert(0, attempt.get_mark())
            answers_entry.insert(0, attempt.get_answers())

    def del_attempt(self, button):
        '''
        delete a attempt from the database and show a success popup
        '''
        # remove attempt from databse
        db.remove_attempt(button, conn)

        self.refresh()

        # show popup
        showinfo("Success", "attempt #" + str(button) + " has been deleted")

    def up_attempt(self, button):
        '''
        delete a attempt details in the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        ##new_attempt = self.attempts[button].get()
        ##new_aid = self.aids[button].get()
        ##new_user = self.users[button].get()
        new_date = self.dates[button].get()
        new_mark = self.marks[button].get()
        new_answers = self.answers[button].get()
        # update the database with new entries
        ##db.update_attempt_aNum(button, new_attempt, conn)
        ##db.update_attempt_assignment(button, new_aid, conn)
        ##db.update_attempt_user(button, new_user, conn)
        db.update_attempt_date(button, new_date, conn)
        db.update_attempt_mark(button, new_mark, conn)
        db.update_attempt_answers(button, new_answers, conn)

        self.refresh()

        # show popup
        showinfo("Success", "attempt #" + str(button) + " has been updated")

    def add_attempt(self):
        '''
        delete a attempt from the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        new_aNum = self.attempt_entry.get()
        new_aid = self.aid_entry.get()
        new_qids = self.qids_entry.get()
        new_user = self.user_entry.get()
        new_date = self.date_entry.get()
        new_mark = self.mark_entry.get()
        new_answers = self.answers_entry.get()
        # add new attempt to databse and save his id number
        aNum = db.add_attempt(new_aNum, new_aid, new_qids, new_user, new_date, new_mark, new_answers, conn)
        # show popup
        self.refresh()
        # clear entries
        self.attempt_entry.delete(0, 'end')
        self.aid_entry.delete(0, 'end')
        self.qids_entry.delete(0, 'end')
        self.user_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.mark_entry.delete(0, 'end')
        self.answers_entry.delete(0, 'end')
        
        showinfo("Success", "attempt #" + str(aNum) + " has been added to database")

    def refresh(self):
        for aNum in list(self.attempts.items()):
            aNum[1].destroy()
        for aid in list(self.aids.items()):
            aid[1].destroy()
        for qid in list(self.qids.items()):
            qid[1].destroy()
        for user in list(self.users.items()):
            user[1].destroy()
        for date in list(self.dates.items()):
            date[1].destroy()
        for mark in list(self.marks.items()):
            mark[1].destroy()
        for answers in list(self.answers.items()):
            answers[1].destroy()
            
        for update in list(self.updates.items()):
            update[1].destroy()
        for delete in list(self.deletes.items()):
            delete[1].destroy()
        self.gen_rows()
        self.enable_buttons()

    def enable_buttons(self):
        # get a list of all existing attempt ids
        attempt_ids = db.get_attempt_ids(conn)
        # configure clicking function for all the delete buttons
        for aNum in attempt_ids:
            self.deletes[aNum].config(command=lambda j=aNum: self.del_attempt(j))
        # configure clicking function for all the update buttons
        for aNum in attempt_ids:
            self.updates[aNum].config(command=lambda j=aNum: self.up_attempt(j))

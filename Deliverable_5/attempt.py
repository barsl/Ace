import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from problem import *
import ast


APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')
    

class Attempt(GUISkeleton):
    '''
    Objects of this type are used to genereate the GUI for the problem Database
    Management screen
    '''
    def __init__(self, parent, controller, uid=None, aid=None):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.labels = ["Subject", "Question", "Answer"]
        # dictionaries to contain the widgets and associate widget to
        # correspondin problem id
        self.entries = []
        self.labels = []
        

        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda: self.refresh()
        back_button.grid(row=0, column=3)
        
        
        # enable clicking functionality for all the buttons
        # self.enable_buttons()
        
    def set_uid(self, uid, aid=None):
        self.uid = uid
        if (aid):
            self.aid = aid
            # label at top of the frame
        title = self.create_label(self, "A"+str(aid)+" Attempt",
                                  TITLE_FONT,
                                  "Red").grid(row=0, column=1, pady=10)
         
         # get the existing progress for the user for the assignment
        self.existing_progress = db.get_assignment_progress_for_user(
            self.aid, self.uid, conn)
        
        self.gen_rows()
           
        Label(self, text="Problem", font=REGULAR_FONT).grid(row=1,column=0, pady=10)
        Label(self, text="Solution", font=REGULAR_FONT).grid(row=1,column=1, pady=10)
        
       
        
    def gen_rows(self):
        # get a list of all the problem ids for the user for that assignment
        ids = db.get_user_first_attempt(self.aid, self.uid, conn)[1]
        # set iterator for grid rows
        ids = ast.literal_eval(ids)
        # for each id create a row
        i = 0
        for qid in ids:
            # create new entries 
            question_label = Label(self, font=REGULAR_FONT)
            answer_entry = Entry(self, font=REGULAR_FONT)
            self.labels.append(question_label)
            self.entries.append(answer_entry)
            # add to corresponding dictonaries with problem ids as keys
            # self.subjects[qid] = subject_entry
            # self.questions[qid] = question_entry
            # self.answers[qid] = answer_entry
          
            # set everything nicely on the grid using an iterator i
            question_label.grid(row=i+3, column=0)
            answer_entry.grid(row=i+3, column=1)

            # set each label with the corresponding value from the problem object
            question_label.config(text=db.get_problem_details(conn, qid)[0][2])

            # set each entry with the corresponding value from list of existing progress
            try:
                answer_entry.insert(0, self.existing_progress[i])
            except IndexError:
                print("no progress yet")
            
            i += 1
            
        # create submit and save progress buttons
        self.update_progress_button = ttk.Button(
            text="Save", command= lambda : self.update_progress())
        self.update_progress_button.pack()
        
            
    def refresh(self):
        for i in self.entries:
            i.destroy()
        for j in self.labels:
            j.destroy()
        self.update_progress_button.destroy()
        self.entries=[]
        self.labels=[]
        self.cont.show_frame('ViewUserAssignments', self.uid)
        
        
    def get_entries(self):
        ''' 
        create a new list, iterate throgh the list of entries and
        add each text to the new list of texts, return that list
        '''
        answers = []
        for ent in self.entries:
            answers.append(ent.get())
            
        return answers
        
    def update_progress(self):
        '''
        takes a list of answers, creates a string in format:'ans1,ans2,ans3,...'
        and calles a database function to update the user's attempt row with the
        new progress
        '''
        answers = self.get_entries()
        progress = ""
        for ans in answers:
            progress += (str(ans)+',')
            
        db.update_assignment_progress_for_user(self.aid, self.uid, progress[:-1], conn)
        self.refresh()
        
    def update_submission_time(self):
        '''
        gets the current time upon submission and calls a db function to update
        the user's attempt row with the new submission time
        '''
        
class ViewAttempt(GUISkeleton):
    '''
    Objects of this type are used to genereate the GUI for the problem Database
    Management screen
    '''
    def __init__(self, parent, controller, uid=None, aid=None):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.labels = ["Subject", "Question", "Answer"]
        # dictionaries to contain the widgets and associate widget to
        # correspondin problem id
        self.entries = []
        self.labels = []
        

        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda: self.refresh()
        back_button.grid(row=0, column=3)
        
        
        # enable clicking functionality for all the buttons
        # self.enable_buttons()
        
    def set_uid(self, uid, aid=None):
        self.uid = uid
        if (aid):
            self.aid = aid
            # label at top of the frame
        title = self.create_label(self, "A"+str(aid)+" Attempt",
                                  TITLE_FONT,
                                  "Red").grid(row=0, column=1, pady=10)
         
         # get the existing progress for the user for the assignment
        self.existing_progress = db.get_assignment_progress_for_user(
            self.aid, self.uid, conn)
        
        self.gen_rows()
           
        Label(self, text="Problem", font=REGULAR_FONT).grid(row=1,column=0, pady=10)
        Label(self, text="Solution", font=REGULAR_FONT).grid(row=1,column=1, pady=10)
        
       
        
    def gen_rows(self):
        # get a list of all the problem ids for the user for that assignment
        ids = db.get_user_first_attempt(self.aid, self.uid, conn)[1]
        # set iterator for grid rows
        ids = ast.literal_eval(ids)
        # for each id create a row
        i = 0
        for qid in ids:
            # create new entries 
            question_label = Label(self, font=REGULAR_FONT)
            answer_label = Label(self, font=REGULAR_FONT)
            self.labels.append(question_label)
            self.entries.append(answer_label)
            # add to corresponding dictonaries with problem ids as keys
            # self.subjects[qid] = subject_entry
            # self.questions[qid] = question_entry
            # self.answers[qid] = answer_entry
          
            # set everything nicely on the grid using an iterator i
            question_label.grid(row=i+3, column=0)
            answer_label.grid(row=i+3, column=1)

            # set each label with the corresponding value from the problem object
            question_label.config(text=db.get_problem_details(conn, qid)[0][2])

            # set each entry with the corresponding value from list of existing progress
            try:
                answer_label.config(text=self.existing_progress[i])
            except IndexError:
                print("no progress yet")
            
            i += 1      
            
    def refresh(self):
        for i in self.entries:
            i.destroy()
        for j in self.labels:
            j.destroy()
        self.entries=[]
        self.labels=[]
        self.cont.show_frame('ViewUserAssignments', self.uid)
        
   
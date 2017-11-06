import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
import sqlite3
from user import *
from main import *

conn = sqlite3.connect('ace.db')

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")


class AddAssignment(GUISkeleton):
    '''
    Window used to input details about an assignment and generate a new assignment
    based on those details
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.row_counter = 0
        self.pairs = {}
        # init lists for labels
        self.subjs = []
        self.nums = []
        # init formula holder
        self.formula = ""        
        
        # label at top of the frame
        ttk.Label(self, text="Add Assignment Menu\n",
                             font=APP_HIGHLIGHT_FONT, foreground="green").grid(
                                 row=self.row_counter, column=1)
        # increment current row counter
        self.row_counter += 1
        
        # set form labels and entries, while keeping track on current line
        self.name_label = Label(self, text="Assignment Name:\n",
                             font=REGULAR_FONT, foreground=NICE_BLUE)
        self.name_label.grid(row=self.row_counter, column=0)
        self.name_entry = Entry(self)
        self.name_entry.grid(row=self.row_counter, column=1)        
        self.row_counter += 1           
        
        self.deadline_label = Label(self, text="Deadline:\n(dd/mm/yyyy)",
                             font=REGULAR_FONT, foreground=NICE_BLUE)
        self.deadline_label.grid(row=self.row_counter, column=0)
        self.deadline_entry = Entry(self)
        self.deadline_entry.grid(row=self.row_counter, column=1)
        self.row_counter += 1
        
        self.visible_label = Label(self, text="Visible:\n(0 or 1)\n",
                             font=REGULAR_FONT, foreground=NICE_BLUE)
        self.visible_label.grid(row=self.row_counter, column=0)
        self.visible_entry = Entry(self)
        self.visible_entry.grid(row=self.row_counter, column=1)        
        self.row_counter += 1
         
        self.subj_label = Label(self, text="Subject:",
                             font=REGULAR_FONT, foreground=NICE_BLUE)
        self.subj_label.grid(row=self.row_counter, column=0)
        self.num_quests_label = Label(self, text="# Of Questions:",                        font=REGULAR_FONT, foreground=NICE_BLUE)
        self.num_quests_label.grid(row=self.row_counter, column=1)
        self.row_counter += 1
        
        self.subj_entry = Entry(self)
        self.subj_entry.grid(row=self.row_counter, column=0)
        
        self.num_quests_entry = Entry(self)
        self.num_quests_entry.grid(row=self.row_counter, column=1)        
        
        # add and place the buttons
        self.add_button = Button(self, text="Add Subject", font=REGULAR_FONT, 
                                 command=lambda :
                                 self.gen_row(self.subj_entry.get(),
                                              self.num_quests_entry.get()))
        self.add_button.grid(row=self.row_counter, column=2) 
        self.done_button = Button(self, text="Done", font=REGULAR_FONT,
                                  command=self.done)
        self.done_button.grid(row=self.row_counter, column=3)  
        self.done_button = Button(self, text="Back", font=REGULAR_FONT,
                                  command=lambda :
                                 self.cont.show_frame('HomeScreen'))
        self.done_button.grid(row=self.row_counter, column=4)          
        self.row_counter += 1 
        
    def gen_row(self, subj, num_quests):
        '''
        takes a subject a number of questions from that subject, add these
        to a dictionary to keep track, and displays a line in the gui with
        these details.
        '''
        # create a subj label, add to list of labels, and fill with details
        subj_label = Label(self, text=subj,
                         font=REGULAR_FONT, foreground="black").grid(
                             row=self.row_counter, column=0)
        self.subjs.append(subj_label)
        # create a #q's label, add to list of labels, and fill with details
        num_quests_label = Label(self, text=num_quests,
                         font=REGULAR_FONT, foreground="black").grid(
                             row=self.row_counter, column=1)
        self.nums.append(num_quests_label)
        
        # create a dictinary pair
        self.pairs[subj] = num_quests
        # increment current row counter
        self.row_counter += 1  
        
        self.subj_entry.delete(0, END)
        self.num_quests_entry.delete(0, END) 
        
        
            
    def create_formula(self):
        '''
        create the formula with the format " subj1:#1q's, subj2:#q's2... "
        based on the text from the labels in the list, and the numbers from
        the labels in the other list
        '''
        # append pairs to formula for each pair
        for pair in self.pairs.items():
            self.formula += str(pair[0]) + ":" + str(pair[1]) + ","
            
        self.formula = self.formula[:-1]
        
    def update_assignments_table(self):
        ''' 
        insert a new row to the assignments table with the details
        '''
        db.add_assignment(self.name_entry.get(), self.formula, 
                          self.deadline_entry.get(), self.visible_entry.get(), conn)
        
    def done(self):
        '''
        create formula, update table, 
        create new assignment table->add row for each user
        '''
        self.create_formula()
        self.update_assignments_table()
        # create the assignment table with it's proper name, and save it's new id
        num = db.create_assignment_table(num, conn)
        
        # get a list of currently existing user ids in the system
        ids = db.get_user_ids()
        
        # for each user id, create a table
        
class ViewUserAssignments(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI for the user to see all Assignments screen
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)        
        self.labels = ["Topic", "Deadline", "Grade"]
        # label at top of the frame
        title = self.create_label(self, "User Assignments\n",
                                  TITLE_FONT,
                                  "Red").grid(row=1, column=1)
        # dictionaries to contain the widgets and associate widget to
        # correspondin assignment id
        self.names = {}
        self.deadlines = {}
        self.grades = {}
        # the buttons
        self.past_attempts = {}
        self.new_attempts = {}

        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=2, column=i)
            i+=1
        back_button = self.create_button(self, "Back")
        # set button method to go back
        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda: controller.show_frame('UserHome')
        back_button.grid(row=1, column=4)
        
        # generate all the dynamically generated widget rows
        self.gen_rows()
        
        # enable clicking functionality for all the buttons
        #self.enable_buttons()

    '''
    def enable_buttons(self):
        # get a list of all existing problem ids
        assignment_ids = db.get_assignment_ids(conn)        
        # configure clicking function for all the delete buttons
        for aid in assignment_ids:
            self.past_attempts[aid].config(command=lambda j=qid: self.del_problem(j))
        # configure clicking function for all the update buttons
        for qid in problem_ids:
            self.updates[qid].config(command=lambda j=qid: self.up_problem(j))
    '''
    def gen_rows(self):
        # get a list of all the user ids in the database
        #ids = db.get_assignment_ids(conn)
        ids = [5,9,10]
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for aid in ids:
            # create new entries 
            name_entry = ttk.Entry(self, font=REGULAR_FONT)
            deadline_entry = ttk.Entry(self, font=REGULAR_FONT)
            grade_entry = ttk.Entry(self, font=REGULAR_FONT)
            # add to corresponding dictonaries with user ids as keys
            self.names[aid] = name_entry
            self.deadlines[aid] = deadline_entry    
            self.grades[aid] = grade_entry
          
            # create new buttons
            past_attempt_button = self.create_button(self, "Past Attempts")
            new_attempt_button = self.create_button(self, "New Attempt")
            # add to corresponding dictonaries with user ids as keys        
            self.past_attempts[aid] = past_attempt_button
            self.new_attempts[aid] = new_attempt_button
            
            # set everything nicely on the grid using an iterator i
            name_entry.grid(row=i+3, column=0)
            deadline_entry.grid(row=i+3, column=1)
            grade_entry.grid(row=i+3, column=2)
            new_attempt_button.grid(row=i+3, column=3)
            past_attempt_button.grid(row=i+3, column=4)
            i += 1
        

class Assignment():
    '''
    A problem object which is used to interact with assignment's data,
    and perform actions that affect assignment's data
    '''
    def __init__(self,aid):
        '''
        aid is the assignment id of the assignment we want to create
        '''
        # get user details from database
        assignment = db.get_assignment_details(conn, aid)[0]
        # assign corresponding values to variables
        self.aid = assignment[0]
        self.topic = assignment[1]
        self.deadline = assignment[2]
        self.visible = assignment[3]
        self.questions = assignment[4]
        self.length = assignment[5]
        
    # getters and setters
    def get_aid(self):
        return self.aid
    def get_deadline(self):
        return self.deadline
    def get_length(self):
        return self.length     
    def get_topic(self):
        return self.topic
    def get_questions(self):
        return self.questions
    def get_visible(self):
        return self.visible 
            
          
        
        

import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from ViewAssignments import *

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 14, "normal")
TITLE_FONT = ("Helvetica", 16, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')


class ViewStudentGrades(GUISkeleton):
	'''class for an admin to view student grades'''
	def __init__(self, parent, controller):
		'''initialises the window'''
		GUISkeleton.__init__(self, parent)

		# create the title label
		self.title = self.create_label(self, "View Student Grades",
		                               TITLE_FONT, "Red").grid(row=0, column=1,
		                                                       pady=10, padx=20)
		self.create_dropdown()


		
	def create_dropdown(self):
		'''create  a drop down menu with the assignment options currently in database'''
		self.tkvar = StringVar()
		self.choices = []
		# Dictionary with options
		aids = db.get_assignments_ids(conn) # this returns a list
		for aid in aids:	
			assignment = db.get_assignment_details(aid, conn)
			assign_str = "Assignment " + str(assignment[0])
			self.choices.append(assign_str)

		self.title = self.create_label(self, "Please select the Assignment to view Grades",
	                                       REGULAR_FONT, NICE_BLUE).grid(row=1, column=1,
	                                                                   pady=10, padx=20)			
		
		self.dropdown = ttk.Combobox(self, textvariable=self.tkvar)
		self.dropdown['values'] = self.choices
		self.dropdown.bind('<<ComboboxSelected>>', self.on_change)
		self.dropdown.grid(row = 2, column =1)
		
	
	
	def on_change(self, eventObject):
		self.drop_down_selection = self.dropdown.get()
		self.create_frame(2, 0)
		result = self.drop_down_selection.split() 
		aid = int(result[1])
		users = 
		#then for each user in aid table do the loop and add to the list box
	
			#self.add_assign_to_lb(aid)
			#get_nth_attempt_id_for_user(aid, uid, -1, conn) # returns nth attempt for user
			# list that will hold all the frames of the widgets created 
			#self.frames = []
		
		print(self.drop_down_selection)	
	
	
	
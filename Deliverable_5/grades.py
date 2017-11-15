import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *

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
		self.create_dropdown();


		
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
	
	
		self.popupMenu = ttk.OptionMenu(self, self.tkvar, self.choices[0],*self.choices)
		self.title = self.create_label(self, "Please select the Assignment to view Grades",
	                                       REGULAR_FONT, NICE_BLUE).grid(row=1, column=1,
	                                                                   pady=10, padx=20)			
		self.popupMenu.grid(row = 2, column =1)
		self.tkvar.trace("w", self.on_change)
	
	def on_change(self):
		'''fuction called when a drop down option was selected'''
		print(self.tkvar.get())
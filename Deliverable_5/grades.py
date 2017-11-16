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
		result = self.drop_down_selection.split() 
		aid = int(result[1])
		user_ids = db.get_users_ids_assignment(aid,conn)
		new_frame = ttk.Frame(self)
		# create a new scrollbar
		scrollbar = ttk.Scrollbar(new_frame, orient='vertical')
		# create a listbox widget
		list_box = tk.Listbox(new_frame,yscrollcommand=scrollbar.set,
			                      width=40, height=8)
		#configure the scrollbar
		scrollbar.config(command=list_box.yview)
		scrollbar.pack(side="right", fill="y")
		# adds the listbox to a listbox dictionary with given key
		self.list_box["grades_listbox"] = list_box        
		list_box.pack(side="left", fill="both")
		new_frame.grid(row=4, column=1)				
		for uid in user_ids:
			user_attempt = db.get_nth_attempt_id_for_user(aid, uid, -1, conn)
			list_box.insert(END, self.user_attempt)
			
			def get_users_ids_assignment(aid, conn):
				cur = conn.cursor()
				cur.execute("SELECT DISTINCT uid FROM " + 'a'+str(aid))
				users = cur.fetchall()
			
				return users			
			
			
	
			
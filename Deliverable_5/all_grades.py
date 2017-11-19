import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db
from assignments import *
from gui_skeleton import *
from ViewAssignments import *
from filtergrades import *

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 14, "normal")
TITLE_FONT = ("Helvetica", 16, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

conn = sqlite3.connect('ace.db')


class ViewStudentGrades(GUISkeleton):
	'''class for an admin to view student grades'''
	def __init__(self, parent, controller, uid=None):
		'''initialises the window'''
		self.controller = controller			
		GUISkeleton.__init__(self, parent)	

		self.title = self.create_label(self, "Please select the Assignment to view Grades",
		                               TITLE_FONT, "Red").grid(row=0, column=1,
		                                                       pady=10, padx=20)			
		self.stu_id = 0
		self.average = self.create_label(self, "", REGULAR_FONT)
		self.create_assignments_dropdown()
		self._init_buttons(controller)

	def _init_buttons(self, controller):
		'''initiate the buttons on the screen'''
		#back button
		back_button = self.create_button(self, "Back")
		back_button["command"] = lambda: controller.show_frame('HomeScreen')
		back_button.grid(row=0, column=4)
		#filter by student Uid button
		find_button = self.create_button(self, "Filter by UID")
		find_entry = self.create_entry(self, "find")
		find_button["command"] = lambda: controller.show_frame('FilterGrade', self.uid, self.aid, find_entry.get())
		find_button.grid(row=1, column=3)		
		find_entry.grid(row=1, column=4)


	def set_uid(self, uid, aid=None, atid=None):
		''' Function to set the uid and aid for the current screen
		@param uid -> current user in the app
		@param aid -> current assignment being looked at
		'''
		self.uid = uid[0]	
		self.aid = None
		#self.create_logout_dropdown(self.uid)


		'''
	def create_logout_dropdown(self, uid):
                Function to have a menu bar for user to log out- NoT WORKING
		menubar = tk.Menu(root)
		filemenu = tk.Menu(menubar, tearoff=0)
		filemenu.add_command(label="Back", command= lambda: controller.show_frame('HomeScreen'))
		filemenu.add_separator()
		menubar.add_cascade(label=str(self.uid), menu=filemenu)
		**** ERROR -> root.config(menu=menubar)
		              goroot.mainloop()


	def user_exit(self, eventObject):
		self.logout_selection = self.logout.get()
		if (self.logout_selection == self.main_choices[1]):
			lambda: controller.show_frame('HomeScreen', self.uid)
		'''					

	def create_assignments_dropdown(self):
		'''Create  a drop down menu for the assignments 
		current in the database table
		
		NOTE: The Filter by ID ONLY works if the assignment has been selected from dropdown 
		already, need to add a popup or somethiing
		'''
		self.tkvar = StringVar()
		self.choices = []
		dropdown_frame = ttk.Frame(self)
		# Dictionary with options
		aids = db.get_assignments_ids(conn) # this returns a list
		for aid in aids:	
			assignment = db.get_assignment_details(aid, conn)
			assign_str = "Assignment " + str(assignment[0])
			self.choices.append(assign_str)

		self.dropdown = ttk.Combobox(dropdown_frame, textvariable=self.tkvar)
		self.dropdown['values'] = self.choices
		self.dropdown.bind('<<ComboboxSelected>>', self.create_listbox)     
		self.dropdown.pack(side="left", fill="both")
		dropdown_frame.grid(row=2, column=1,padx=5)	


	def create_listbox(self, eventObject):
		''' Create a listbox for the last attempt of each user for selected assignment
		@param eventObject, dropdown menu item selected
		
		NOTE: WHEN TESTING A1 AND A10 ARE ONLY TABLES WITH DATA IN DB
		NOTE2: HOW-TO-TAB-THE-FREAKING-LISTBOX-ENTRY!!!! 
		       ITS TOO CLOSE TO EACH OTHER "kex 2 5- vs "Kez    2    50"
		
		'''
		self.average.destroy()
		self.all_grades = 0
		self.num_users = 0
		self.drop_down_selection = self.dropdown.get()
		#split the selection strng to get the 'aid' 
		result = self.drop_down_selection.split() 
		self.aid = int(result[1])
		user_ids = db.get_users_ids_assignment(self.aid,conn)
		new_frame = ttk.Frame(self)
		# create a new scrollbar
		scrollbar = ttk.Scrollbar(new_frame, orient='vertical')
		# create a listbox widget
		self.list_box = tk.Listbox(new_frame,yscrollcommand=scrollbar.set,
		                           width=30, height=8)
		#configure the scrollbar
		scrollbar.config(command=self.list_box.yview)
		scrollbar.pack(side="right", fill="y")
		# adds the listbox to a listbox dictionary with given key     
		self.list_box.pack(side="left", fill="both")
		new_frame.grid(row=5, column=1,padx=5)

		for user in user_ids:
			# get all the attempts for the user id
			attempts = db.get_user_attempts(self.aid, user, conn)
			# get the last attempt
			last_a = attempts[-1]
			user_result = self.update_grades_table(self, *last_a)
			# return it
			self.list_box.insert(END, user_result)	
		
		self.list_box.select_set(0)
		self.show_average()

	def update_grades_table(self, row, uid, questions, progress, grade):
		''' 
		Insert a new row to the grades table with the user details
		@param row -> tuple from attempt table
		@param uid -> user uid from database
		@param questions -> assignment questions assigned to user
		@param progress -> questions completed by the user stored in database
		@param grade -> current grade for user in the database for the assignment
		'''
		tab = ViewAssignments.create_tab(self)
		user_row = []
		student_details = db.get_user_details(conn, uid)
		name = student_details[0][2]
		user_row.append(name)
		user_row.append(uid)
		#check for empty grades
		if (grade == ''):
			user_row.append("Grade Not Available")
		else:
			 # if user has completed assignment then 
			# upgrade num_users and all_grades for the avg calculation
			self.num_users = self.num_users + 1
			self.all_grades = self.all_grades + int(grade)
			user_row.append(grade)

		return user_row


	def average_grade(self):
		''' Function returns string of the average grade of
		all students who have completed the assignment
		'''
		if (self.all_grades == 0 and self.num_users == 0):
			return "No Grades Available"
		elif (self.num_users != 0 and self.all_grades == 0):
			return "0"
		else:
			return str(int(self.all_grades/self.num_users))

	def show_average(self):
		''' Function that displays average labels for student grades on
		the current display assignment
		'''
		self.header_label = self.create_label(self, "Student UID Grade", REGULAR_FONT)
		self.header_label.grid(row=4, column=1, pady=10)
		self.average = self.create_label(self, "Average Grade: " + self.average_grade(), APP_HIGHLIGHT_FONT)
		self.average.grid(row=4, column=3)

	
			
		
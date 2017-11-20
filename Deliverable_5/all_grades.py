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
		self.selected = False
		self.filters = ['','']
		self.sort_opt = None
		self.controller = controller			
		GUISkeleton.__init__(self, parent)
		self.widgets = {}
		self.all_grades = 0
		self.num_users = 0		
		self.stu_id = 0
		self.uids = {}
		self.create_assignments_dropdown()
		self._init_buttons(controller)

	def _init_buttons(self, controller):
		'''initiate the buttons on the screen'''
		new_frame = ttk.Frame(self)
		#back button
		self.create_label(new_frame, "View Grades",
		                  TITLE_FONT, "Red").pack(side="left", padx=40)	
		back_button = self.create_button(new_frame, "Back")
		back_button["command"] = lambda: controller.show_frame('HomeScreen')
		back_button.pack(side="right", padx=10)
		new_frame.grid(row=0, column=3, pady=20)

	def create_assignments_dropdown(self):
		'''Create  a drop down menu for the assignments 
		current in the database table
		
		NOTE: The Filter by ID ONLY works
		if the assignment has been selected from dropdown 
		already, need to add a popup or somethiing
		'''
		self.tkvar = StringVar()
		self.choices = []
		frame = ttk.Frame(self)
		# Dictionary with options
		aids = db.get_assignments_ids(conn) # this returns a list
		for aid in aids:	
			assignment = db.get_assignment_details(aid, conn)
			assign_str = "Assignment " + str(assignment[0])
			self.choices.append(assign_str)

		self.dropdown = ttk.Combobox(frame, textvariable=self.tkvar)
		self.dropdown['values'] = self.choices
		# set the command that is invoked when the value of the box is
		# switched
		self.dropdown.bind('<<ComboboxSelected>>', self.create_listbox)     
		self.dropdown.pack(side="left", fill="both")
		# create the sort and filter buttons
		filter_button = self.create_button(frame, "Filter")
		sort_button = self.create_button(frame, "Sort")
		filter_button["command"] = lambda : self.filter_options()
		sort_button["command"] = lambda : self.sort_options()
		# pack the buttosn into the frame
		filter_button.pack(side="left", padx=10)
		sort_button.pack(side="left")
		frame.grid(row=1, column=1,padx=5, columnspan=2)	


	def create_listbox(self, eventObject):
		''' Create a listbox for the last 
		attempt of each user for selected assignment
		@param eventObject, dropdown menu item selected
		
		NOTE: WHEN TESTING A1 AND A10 ARE ONLY TABLES WITH DATA IN DB
		NOTE2: HOW-TO-TAB-THE-FREAKING-LISTBOX-ENTRY!!!! 
		       ITS TOO CLOSE TO EACH OTHER "kex 2 5- vs "Kez    2    50"
		
		'''
		drop_results = self.dropdown.get()
		#split the selection strng to get the 'aid' 
		aid = drop_results.split()[1] 
		self.aid = int(aid)
		user_ids = db.get_users_ids_assignment(self.aid,conn)
		self.create_list_box("results", 4, 2, span=3)
		self.create_edit_grade(5, 3)
		max_len = self.get_longest_username(user_ids)
		for user in user_ids:
			# get all the attempts for the user id
			attempts = db.get_user_attempts(self.aid, user, conn)
			user_result = self.update_grades_table(self.uids[user],
			                                       user, attempts,
			                                       max_len)
			# place it in the lists_box
			self.list_box["results"].insert(END, user_result)
		self.average_labels(user_ids).grid(row=3, column=2,
		                                   columnspan=3)
			
			
	def filter_options(self):
		'''opens up the filter menu to filter results
		in the assignment'''
		# create a new frame
		frame = ttk.Frame(self)
		# create the radio button
		radio = ttk.Radiobutton(frame, text="Student")
		radio["command"] = lambda : self.create_student_box(frame)
		grades = ["All", "0%", " < 50%", " > 50%", " > 70%",
		          " > 80%", " > 90%", "100%"]
		# create a dropdown menu
		dropdown = ttk.Combobox(frame)
		dropdown['values'] = grades
		self.widgets["grades filter"] = dropdown
		done = self.create_button(frame, "Done")
		done["command"] = (lambda : self.filter_results())
		radio.grid(row=0, column=0, sticky="W")
		dropdown.grid(row=1, column=0)
		done.grid(row=1, column=3, padx=10)
		frame.grid(row=2, column=1, pady=15)
	
		
	def filter_results(self):
		'''filters the results in the listbox by filter options
		doesn't calls refresh to change the main list_box'''
		# get the filter options that the user selected
		key = "students"
		drop_option = self.widgets["grades filter"].get()
		if key in self.list_box:
			lb = self.list_box["students"]
			# this gives a tuple with the indices, but we want
			# the user ids
			selected = lb.curselection()
			select_ids = []
			for index in selected:
				select_ids.append(lb.get(index).split()[0])
			self.filters = [select_ids, drop_option]
			self.refresh()
		else:
			self.filters = ['', drop_option]
			self.refresh()
			
	def sort_options(self):
		'''creates the buttons that are enabled when sort is pressed'''
		frame = ttk.Frame(self)
		sorts = ["Grades", "User Id", "Attempts"]
		dropdown = ttk.Combobox(frame)
		dropdown['values'] = sorts
		self.widgets["sorts"] = dropdown
		done = self.create_button(frame, "Done")
		done["command"] = (lambda : self.sort_results())		
		dropdown.pack(side="left", padx=10)
		done.pack(side="left")
		frame.grid(row=2, column=4)
		
	def sort_results(self):
		'''sets the sort option and calls refresh based on the sort
		option selected'''
		option = self.widgets["sorts"].get()
		sorts = ["User Id", "Grades", "Attempts"]		
		if (option == sorts[0]):
			self.sort_opt = 0
		elif (option == sorts[1]):
			self.sort_opt = 2
		elif (option == sorts[2]):
			self.sort_opt = 3
		self.refresh()
		
	def refresh(self):
		'''refreshes the main list_box, based on filters
		that are in self.filter, and sort options in self.sortopt
		this can be used to clear the filters as well'''
		filters = self.filters
		filter_grade = filters[1].split()
		sort_opt = self.sort_opt
		if (len(filter_grade) > 1 and filter_grade[-1] == "50%"):
			if (filter_grade[-2] == "<"):
				filter_grade[-1] = "-50%"
		main_lb = self.list_box["results"]
		# get all items from main list_box
		all_items = main_lb.get(0, main_lb.size())
		# delete everything currently in the main list_box
		main_lb.delete(0, main_lb.size())
		# filter the results and add them back to the listbox
		items = []
		for item in all_items:
			# split the items
			items.append(item.split())
		if (sort_opt != None): 
			# sort the nested list by the sort option given
			self.sort_nested(sort_opt, items)
		# filter out the ones we dont need
		for item in items:
			# check to see if the filter tuple is empty
			ids = filters[0]
			filtered_id = False
			filtered_grade = False
			if (ids != ''):
				# check if the user id is in 
				if (item[0] in ids):
					# we want to check the other option
					filtered_id = True
			else:
				filtered_id = True
			if (filter_grade != []):
				if (filter_grade[-1] == "-50%"):
					# check if % is less than 50
					filtered_grade = (int(item[2][:-1]) + 
					            int(filter_grade[-1][:-1])) < 0
				else:
					filtered_grade = (int(item[2][:-1]) - 
					            int(filter_grade[-1][:-1])) > 0
			else:
				filtered_grade = True
			if (filtered_id and filtered_grade):
				result = "{:>4}   {:<12}   {:>3}  {:>4}"
				result = result.format(*item)
				main_lb.insert(END, result)
	
	
	def sort_nested(self, index, nlist):
		'''sorts a nested list given an index
		this uses a simple insertion sort algorithm to sort'''
		for i in range(1,len(nlist)):

			current = nlist[i]
			pos = i
			
			while(pos > 0 and nlist[pos - 1][index] > current[index]):
				nlist[pos] = nlist[pos - 1]
				pos = pos - 1
			nlist[pos] = current
				      
				      
	def create_student_box(self, location):
		'''creates a student listbox in the given location'''
		list_box = self.create_list_box_loc(location, "students", 10, 5,
		                                    mode="multiple")
		users = db.get_user_ids(conn)
		for user in users:
			info = db.get_user_details(conn, user)
			# check that a user is a student
			if (info[0][1] == "student"):
				result = "{:>3} {:<12}"
				result = result.format(info[0][0], info[0][2])
				self.list_box["students"].insert(END, result)
		list_box.grid(row=0, column=2, rowspan=8, padx=5)
	
	def average_labels(self, uids):
		'''creates a label for the average and a label
		for the number of users that have completed the assignment
		@param uids-> uids of people who have this assignment assigned
		'''
		frame = ttk.Frame(self)
		# set the strings if we have data
		if (len(uids) > 0):
			completion_string = ("Student Completion: {}%".format( 
			                     round(self.num_users/len(uids) * 100)))
		else:
			completion_string = ''
		if (self.all_grades > 0):
			average_string = ("Student Average: {}%".format(
			                  round((self.all_grades/self.num_users))))
		else:
			average_string = "No grades available"
		# create labels for the strings
		completion_label = self.create_label(frame, completion_string)
		average_label = self.create_label(frame, average_string)
		completion_label.grid(row=0, column=0)
		average_label.grid(row=1, column=0)
		self.widgets["average"] = frame
		return frame
	
	def create_edit_grade(self, row, column):
		'''creates the edit grade frame
		@param row ->row you want to place the frame in
		@param column -> column you want to place the frame in
		'''
		# create the edit grade button
		frame = ttk.Frame(self)
		edit_grade = self.create_button(frame, "Edit Grade")
		edit_grade["command"] = lambda : self.edit_grade(frame)
		edit_grade.pack()
		self.widgets["edit grade"] = frame
		frame.grid(row=row, column=column)
			
	def get_longest_username(self, uids):
		''' a function that gets the longest user name
		for the formatting of the list box
		@param uids -> a list containing the uids
		that are going to be checked '''
		max_len = 0
		for uid in uids:
			# get the user_info
			user_info = db.get_user_details(conn, uid)
			name = user_info[0][2]
			# want to call this later without accessing the db
			self.uids[uid] = name
			if (len(name) > max_len):
				max_len = len(name)
		return max_len
			
			
	def update_grades_table(self, username, uid, attempts, max_len):
		''' 
		Insert a new row to the grades table with the user details
		@parame username ->username of the uid
		@param uid -> user uid from database
		@param attempts -> Attempts tuple
		the attempts are stored in a tuple, where each element of the 
		tuple is in this format:
		(id, correct answers, student answers, 100)
		for example
		(4, [10,6], [10,6], 100)
		is the tuple with student id 4, answers 10, 6
		student answers 10, 6 resulting in grade 100%
		@param max_len -> the length of the maximum name...
		used for formatting
		'''
		result = "{:>4}   {:<12}   {:>3}%   {:>4}"
		grade = attempts[-1][-1]
		#check for empty grades
		if (grade == ''):
			result += "Grade Not Available" + tab
		else:
			# if user has completed assignment then 
			# upgrade num_users and all_grades for the avg calculation
			self.num_users = self.num_users + 1
			self.all_grades = self.all_grades + int(grade)
		# put number of attempts
		num_attempts = len(attempts)
		result = result.format(uid, username, grade, num_attempts)
		return result

"""
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
"""
"""
	def show_average(self):
		''' Function that displays average labels for student grades on
		the current display assignment
		'''
		self.header_label = self.create_label(self, "Student UID Grade", REGULAR_FONT)
		self.header_label.grid(row=4, column=1, pady=10)
		self.average = self.create_label(self, "Average Grade: " + self.average_grade(), APP_HIGHLIGHT_FONT)
		self.average.grid(row=4, column=3)
"""
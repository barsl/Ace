import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
                    StringVar, DISABLED, NORMAL, END, W, E
from tkinter.messagebox import showinfo
import database_api as db

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
NICE_BLUE = "#3399FF"

class GUISkeleton(ttk.Frame):
    '''Skeleton for creating frames in Tkinter'''
    def __init__(self, parent):
        self.entry_fields = {}
        ttk.Frame.__init__(self, parent)
        
    def create_label(self, location, text, font=None, foreground=None):
        '''creates a label the programmer will be able to assign
        this to a variable, edit the parameters, and pack to their liking'''
        label = ttk.Label(location)
        label["text"] = text
        if (font != None):
            label["font"] = font
        if (foreground != None):
            label["foreground"] = foreground
        return label
    
    def create_entry(self, location, key, font=None):
        ''' Returns an entry box that the programmer is able to pack'''
        # create an entrybox
        new_entry = ttk.Entry(location)
        if (font != None):
            new_entry["font"] = font
        # assign a stringvar to the Entry
        self.entry_fields[key] = StringVar()
        new_entry["textvariable"] = self.entry_fields[key]
        return new_entry
    
    def create_button(self, location, text):
        ''' creates a button with the wanted text that the programmer
        can customize'''
        new_button = ttk.Button(location)
        new_button["text"] = text
        return new_button   

        
    def create_empty_label(location, num):
        ''' creates an empty label with the designated number of newlines
        create_empty_label(self, 1)
        GUI: \n              <-- this is the label created
        widget
        '''
        txt = ""
        for i in range(num):
            txt += "\n"
            label = ttk.Label(location)
            label["text"] = txt
        label.pack()
        

class AoS(tk.Tk):
    '''Class that contains everything in the Application '''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # title of the software
        tk.Tk.wm_title(self, "Ace of Spades")
        tk.Tk.wm_minsize(self, width=350, height=350)
        self.container = tk.Frame(self)
        
        self.container.pack(side="top", fill="both", expand = True)
        
        # configuration for the grid (0 is the min row or column)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # the frame that is on the top is the one that is on the screen
        # the dictionary will contain the different screens
        self.frames = {}
        
        # this loop adds screens to the dictionary,
        # once we build more screens, add them to the tuple 
        # for F in TUPLE e.g. (LoginScreen, HomeScreen, DataBlaBLa)
        for F in (LoginScreen, HomeScreen, ProblemInterface, UserHome,
                  UserInterface):
            # here F is the name of the Screen
            frame = F(self.container, self)
            self.frames[F] = frame
            # with grid you can assign columns and rows to your
            # sticky determines (alignment + stretch) 
            # stretch the window to north south east or west (n,s,e,w)
            frame.grid(row=0, column=0, sticky="nsew")            
            
        self.show_frame(LoginScreen)


    def show_frame(self, cont):
        ''' function that determines which of the screens will be viewed by
        the user. This function uses tkraise, in order to bring the
        wanted screen to the front
        @param cont - name of the screen that needs to be displayed
        this is stored in the frames dictionary in self'''
        # get the frame from the dictionary
        frame = self.frames[cont]
        frame.tkraise()
        


class LoginScreen(GUISkeleton):
    '''Creates a login screen, which will be the 
    first screen of our Application'''
    def __init__(self, parent, controller):
        self.entry_keys = ["Email", "Password"]      
        GUISkeleton.__init__(self, parent)
        self.create_login_labels()
        self.create_entry_fields(controller)


    def create_login_labels(self):
        '''creates the beginning labels'''
        # login text
        login_label = self.create_label(self, "Welcome to Ace! Please Log In: ",
                          APP_HIGHLIGHT_FONT, "blue")
        #empty label for format
        # tk.Label(self, text="\n\n\n\n").pack()
        self.create_empty_label(4)
        login_label.pack()
        
        
    def create_entry_fields(self, controller):
        ''' creates the entry fields for username and password'''
        # create the username and password fields
        for field in self.entry_keys:
            myframe = ttk.Frame(self)
            new_label = self.create_label(myframe, field, REGULAR_FONT)
            new_label.pack({"side": "left"}, padx=10)
            enterbox = self.create_entry(myframe, field)
            if field == "Password":
                # the show field of the password window makes sure that we only
                # show '*' when somebody types in the password                
                enterbox["show"] = "*"
            enterbox.pack({"side": "left"})
            myframe.pack()
        self.create_login(controller)

    def create_login(self, controller):
        '''creates login button'''
        button = self.create_button(self, "Login")
        button["command"] = lambda : self.verify_creds(controller)
        button.pack(pady=20)
        
    def verify_creds(self, controller):
        ''' used to verify  login credentials from the entry boxes
        of the LoginScreen '''
        i = 0;
        creds = []
        for field in self.entry_keys:
            # get user's entries and store
            creds.append(self.entry_fields[field].get())
            i += 1
        # try getting user's details from database according to entered email
        try :
            user_details = db.get_user_details_by_email(conn, creds[0])
            # if the provided password matches the one stored
            if (creds[1] == user_details[0][4]):
                # check if user or admin
                # print(user_details)
                if (user_details[0][1] == 'student'):
                    controller.show_frame(UserHome)
                # move to home screen
                elif (user_details[0][1] == 'admin'):
                    controller.show_frame(HomeScreen)
                else:
                    showinfo("Fail", "User has no role")
            else :
                # otherwise pop msg to terminal
                showinfo("Fail", "Wrong combo")
            self.entry_fields["Email"].set('')
            self.entry_fields["Password"].set('')
        # print msg to terminal if email doesnt exist
        except IndexError:
            showinfo("Fail", "This email address is not in the system")

class UserHome(GUISkeleton):
    '''HomeScreen that appears if login person is user'''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.buttons = ["View Assignments", "Logout"]
        self.init_window(controller)
        
    def init_window(self, controller):
        '''initialises the window'''
        self.create_empty_label(5)
        for button in self.buttons:
            new_button = self.create_button(self, button)
            if (button == "Logout"):
                new_button["command"] = (lambda :
                                         controller.show_frame(LoginScreen))
            new_button.pack()

class HomeScreen(GUISkeleton):
    ''' Homescreen that appears after the user logs in
    at the moment the homescreen is just a placeholder for some buttons'''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.buttons = ["Add User", "Manage Question Bank", "Logout"]
        self.init_window(controller)
    
    def create_buttons(self, controller):
        ''' creates logout button'''
        # button will go to login screen
        for button in self.buttons:
            new_button = self.create_button(self, button)
            if button == "Add User":
                new_button["command"] = lambda : controller.show_frame(UserInterface)
            elif button == "Manage Question Bank":
                new_button["command"] = lambda : controller.show_frame(ProblemInterface)
            elif button == "Logout":
                new_button["command"] = (lambda :
                                         controller.show_frame(LoginScreen))
            new_button.pack()
    
    def init_window(self, controller):
        ''' initialises the homescreen and its elements'''
        homescreen_label = self.create_label(self, "Home", APP_HIGHLIGHT_FONT)
        # just to get the formatting correct
        # empty_label = ttk.Label(self, text="\n").pack()
        self.create_empty_label(1)
        homescreen_label.pack()
        self.create_buttons(controller)
        

class User():
    '''
    A user object which is used to interact with users' data,
    and perform actions that affect users' data
    '''
    def __init__(self, uid):
        '''
        uid is the user id of the student we want to create
        '''
        # get user details from database
        user = db.get_user_details(conn, uid)[0]
        # assign corresponding values to variables
        self.uid = user[0]
        self.role = user[1]
        self.name = user[2]
        self.email = user[3]
        self.password = user[4]
        
    # getters and setters
    def get_uid(self):
        return self.uid
    def get_role(self):
        return self.role      
    def get_name(self):
        return self.name
    def get_email(self):
        return self.email
    def get_password(self):
        return self.password  

class UserInterface(GUISkeleton):
    '''
    Objects of this type are used to generate the GUI for the User Database
    Management screen
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.labels = ["Role", "Name", "Email"]
        # label at top of the frame
        new_label = self.create_label(self, "User Database Management\n",
                                      REGULAR_FONT,
                                      "Green").grid(row=0, column=1) 
        # dictionaries to contain the widgets and associate widget to
        # corresponding user id
        self.roles = {}
        self.names = {}
        self.emails = {}
        self.updates = {}
        self.deletes = {}
        
        # the 3 static lables that are always there
        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=1, column=i)
            # create first row of entries for add_problem function
            # set everything nicely on the grid
            # create first row of entries for add_user function
            # set everything nicely on the grid            
            new_entry = self.create_entry(self, label,
                                          REGULAR_FONT).grid(row=2, column=i)
            i += 1         
        # create add user button
        add_user_button = self.create_button(self, "Add User")
        # set button method to add_user  
        add_user_button["command"] = lambda : self.add_user()        
        add_user_button.grid(row=2, column=3)
        back_button = self.create_button(self, "Back")
        back_button["command"] = lambda : controller.show_frame(HomeScreen)
        back_button.grid(row=2, column=4)
        # generate all the dynamically generaterd widget rows
        self.gen_rows()
        
        # enable clicking functionality for all the buttons
        self.enable_buttons()
        
          
        
    def gen_rows(self):
        # get a list of all the user ids in the database
        ids = db.get_user_ids(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for uid in ids:
            # create new entries 
            role_entry = ttk.Entry(self, font=REGULAR_FONT)
            name_entry = ttk.Entry(self, font=REGULAR_FONT)
            email_entry = ttk.Entry(self, font=REGULAR_FONT)
            # add to corresponding dictonaries with user ids as keys
            self.roles[uid] = role_entry
            self.names[uid] = name_entry    
            self.emails[uid] = email_entry
          
            # create new buttons
            update_button = self.create_button(self, "Update")
            delete_button = self.create_button(self, "Delete")
            # add to corresponding dictonaries with user ids as keys        
            self.deletes[uid] = delete_button
            self.updates[uid] = update_button
            
            # set everything nicely on the grid using an iterator i
            role_entry.grid(row=i+3, column=0)
            name_entry.grid(row=i+3, column=1)
            email_entry.grid(row=i+3, column=2)
            update_button.grid(row=i+3, column=3)
            delete_button.grid(row=i+3, column=4)
            i += 1
            
            # create new user object to contain user info
            user = User(uid)
            # set each entry with the corresponding value from the user object
            role_entry.insert(0, user.get_role())
            name_entry.insert(0, user.get_name())
            email_entry.insert(0, user.get_email())
            
        
            
    def del_user(self, button):
        '''
        delete a user from the database and show a success popup
        '''
        # remove user from databse
        db.remove_user(button, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "User #" + str(button) + " has been deleted")
    
    def up_user(self, button):
        '''
        delete a user details in the database and show a success popup
        '''        
        # get new parameters from entry widgets in the dictionaries
        new_role = self.roles[button].get()
        new_name = self.names[button].get()
        new_email = self.emails[button].get()
        # update the database with new entries
        db.update_user_role(button, new_role, conn)
        db.update_user_name(button, new_name, conn)
        db.update_user_email(button, new_email, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "User #" + str(button) + " has been updated")
        
    def add_user(self):
        '''
        delete a user from the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        new_role = self.entry_fields["Role"].get()
        new_name = self.entry_fields["Name"].get()
        new_email = self.entry_fields["Email"].get()        
        # add new user to databse and save his id number
        uid = db.add_user(new_role, new_name, new_email, "", conn)
        # show popup
        self.refresh()
        # clear entries
        self.entry_fields["Role"].set('')
        self.entry_fields["Name"].set('')
        self.entry_fields["Email"].set('')        
        showinfo("Success", "User #" + str(uid ) + " has been added to database")
        

    def refresh(self):
        for role in list(self.roles.items()):
            role[1].destroy()
        for name in list(self.names.items()):
            name[1].destroy()
        for email in list(self.emails.items()):
            email[1].destroy()
        for update in list(self.updates.items()):
            update[1].destroy()
        for delete in list(self.deletes.items()):
            delete[1].destroy()
        self.gen_rows()
        self.enable_buttons()
        
    def enable_buttons(self):
        # get a list of all existing user ids
        user_ids = db.get_user_ids(conn)        
        # configure clicking function for all the delete buttons
        for uid in user_ids:
            self.deletes[uid].config(command=lambda j=uid: self.del_user(j))
        # configure clicking function for all the update buttons
        for uid in user_ids:
            self.updates[uid].config(command=lambda j=uid: self.up_user(j))         


class Problem():
    '''
    A problem object which is used to interact with problems' data,
    and perform actions that affect problems' data
    '''
    def __init__(self, qid):
        '''
        qid is the problem id of the student we want to create
        '''
        # get problem details from database
        problem = db.get_problem_details(conn, qid)[0]
        # assign corresponding values to variables
        self.qid = problem[0]
        self.subject = problem[1]
        self.question = problem[2]
        self.answer = problem[3]
        
    # getters and setters
    def get_qid(self):
        return self.qid
    def get_subject(self):
        return self.subject      
    def get_question(self):
        return self.question
    def get_answer(self):
        return self.answer

class ProblemInterface(GUISkeleton):
    '''
    Objects of this type are used to genereate the GUI for the problem Database
    Management screen
    '''
    def __init__(self, parent, controller):
        GUISkeleton.__init__(self, parent)
        self.cont = controller
        self.labels = ["Subject", "Question", "Answer"]
        # label at top of the frame
        title = self.create_label(self, "Problem Database Management\n",
                                  REGULAR_FONT, "Green").grid(
                                 row=0, column=1)
        # dictionaries to contain the widgets and associate widget to
        # correspondin problem id
        self.subjects = {}
        self.questions = {}
        self.answers = {}
        # the buttons
        self.updates = {}
        self.deletes = {}
        
        # the 3 static lables that are always there
        i = 0
        for label in self.labels:
            new_label = self.create_label(self, label, REGULAR_FONT,
                                          NICE_BLUE).grid(row=1, column=i)
            # create first row of entries for add_problem function
            # set everything nicely on the grid
            new_entry = self.create_entry(self, label,
                                          REGULAR_FONT).grid(row=2, column=i)
            i += 1
        # create add problem button
        add_problem_button = self.create_button(self, "Add problem")
        add_problem_button.grid(row=2, column=3)
        back_button = self.create_button(self, "Back")
        # set button method to add_problem
        add_problem_button.config(command=lambda : self.add_problem())
        back_button["command"] = lambda: controller.show_frame(HomeScreen)
        back_button.grid(row=2, column=4)
        
        # generate all the dynamically generated widget rows
        self.gen_rows()
        
        # enable clicking functionality for all the buttons
        self.enable_buttons()
        
          
        
    def gen_rows(self):
        # get a list of all the problem ids in the database
        ids = db.get_problem_ids(conn)
        # set iterator for grid rows
        i = 0
        # for each id create a row
        for qid in ids:
            # create new entries 
            subject_entry = ttk.Entry(self, font=REGULAR_FONT)
            question_entry = ttk.Entry(self, font=REGULAR_FONT)
            answer_entry = ttk.Entry(self, font=REGULAR_FONT)
            # add to corresponding dictonaries with problem ids as keys
            self.subjects[qid] = subject_entry
            self.questions[qid] = question_entry    
            self.answers[qid] = answer_entry
          
            # create new buttons
            update_button = ttk.Button(self, text="Update")
            delete_button = ttk.Button(self, text="Delete")
            # add to corresponding dictonaries with problem ids as keys        
            self.deletes[qid] = delete_button
            self.updates[qid] = update_button
            
            # set everything nicely on the grid using an iterator i
            subject_entry.grid(row=i+3, column=0)
            question_entry.grid(row=i+3, column=1)
            answer_entry.grid(row=i+3, column=2)
            update_button.grid(row=i+3, column=3)
            delete_button.grid(row=i+3, column=4)
            i += 1
            
            # create new problem object to contain problem info
            problem = Problem(qid)
            # set each entry with the corresponding value from the problem object
            subject_entry.insert(0, problem.get_subject())
            question_entry.insert(0, problem.get_question())
            answer_entry.insert(0, problem.get_answer())
            
        
            
    def del_problem(self, button):
        '''
        delete a problem from the database and show a success popup
        '''
        # remove problem from databse
        db.remove_problem(button, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "problem #" + str(button) + " has been deleted")
    
    def up_problem(self, button):
        '''
        delete a problem details in the database and show a success popup
        '''        
        # get new parameters from entry widgets in the dictionaries
        new_subject = self.subjects[button].get()
        new_question = self.questions[button].get()
        new_answer = self.answers[button].get()
        # update the database with new entries
        db.update_problem_subject(button, new_subject, conn)
        db.update_problem_question(button, new_question, conn)
        db.update_problem_answer(button, new_answer, conn)
        
        self.refresh()
        
        # show popup
        showinfo("Success", "problem #" + str(button) + " has been updated")
        
    def add_problem(self):
        '''
        delete a problem from the database and show a success popup
        '''
        # get new parameters from entry widgets in the dictionaries
        new_subject = self.entry_fields["Subject"] .get()
        new_question = self.entry_fields["Question"].get()
        new_answer = self.entry_fields["Answer"].get()        
        # add new problem to databse and save his id number
        qid = db.add_problem(new_subject, new_question, new_answer, conn)
        # show popup
        self.refresh()
        # clear entries
        self.entry_fields["Subject"].set('')
        self.entry_fields["Question"].set('')
        self.entry_fields["Answer"].set('')      
        showinfo("Success", "problem #" + str(qid) + " has been added to database")

    def refresh(self):
        for subject in list(self.subjects.items()):
            subject[1].destroy()
        for question in list(self.questions.items()):
            question[1].destroy()
        for answer in list(self.answers.items()):
            answer[1].destroy()
        for update in list(self.updates.items()):
            update[1].destroy()
        for delete in list(self.deletes.items()):
            delete[1].destroy()
        self.gen_rows()
        self.enable_buttons()
        
    def enable_buttons(self):
        # get a list of all existing problem ids
        problem_ids = db.get_problem_ids(conn)        
        # configure clicking function for all the delete buttons
        for qid in problem_ids:
            self.deletes[qid].config(command=lambda j=qid: self.del_problem(j))
        # configure clicking function for all the update buttons
        for qid in problem_ids:
            self.updates[qid].config(command=lambda j=qid: self.up_problem(j))         


if __name__ == "__main__":
    conn = db.sqlite3.connect('ace.db')
    app = AoS()
    app.mainloop()
    
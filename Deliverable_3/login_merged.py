import tkinter as tk
from tkinter import ttk
from tkinter import font

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")

class AoS(tk.Tk):
    '''Class that contains everything in the Application '''
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # title of the software
        tk.Tk.wm_title(self, "Ace of Spades")
        tk.Tk.wm_minsize(self, width=300, height=200)
        container = tk.Frame(self)
        
        container.pack(side="top", fill="both", expand = True)
        
        # configuration for the grid (0 is the min row or column)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # the frame that is on the top is the one that is on the screen
        # the dictionary will contain the different screens
        self.frames = {}
    
        # this loop adds screens to the dictionary,
        # once we build more screens, add them to the tuple 
        # for F in TUPLE e.g. (LoginScreen, HomeScreen, DataBlaBLa)
        for F in (LoginScreen, Problems, RemoveProblems, AddProblems):
            # here F is the name of the Screen
            frame = F(container, self)
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


class LoginScreen(tk.Frame):
    '''Creates a login screen, which will be the 
    first screen of our Application'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.init_window(controller)
        
    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        # login text
        loginlbl = ttk.Label(self, text ="Welcome to Ace! Please Log In: ",
                             font=APP_HIGHLIGHT_FONT, foreground="blue")
        # create the username and password fields
        username_label = tk.Label(self, text="Username", font=REGULAR_FONT, foreground="red")
        username_entry = tk.Entry(self)
        password_label = tk.Label(self, text="Password", font=REGULAR_FONT, foreground="red")
        # the show field of the password window makes sure that we only
        # show '*' when somebody types in the password
        password_entry = tk.Entry(self, show="*")
        
        login_btn = tk.Button(self, text="Log in", command=lambda: controller.show_frame(Problems))        
        # empty label to create some space between the top 
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        # place our created label inside the
        loginlbl.pack()
        username_label.pack()
        username_entry.pack()
        password_label.pack()
        password_entry.pack()
        login_btn.pack(pady=20)        

class Problems(tk.Frame):
    '''Creates a prob screen, which will used by admin to add/edit and remove problems from '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)
        
    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
 
        # create the question label
        options_label = tk.Label(self, text="To make changes to the Question Bank, please select from the options below: ",
                                 font=APP_HIGHLIGHT_FONT, foreground="blue", wraplength=300)


        add_btn = tk.Button(self, text="Add a Problem", command=lambda: controller.show_frame(AddProblems))
        remove_btn = tk.Button(self, text="Remove a Problem", command=lambda: controller.show_frame(RemoveProblems))
        # empty label to create some space between the top 
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        # place our created label inside the
        
        options_label.pack()
        empty2_label = tk.Label(self, text="\n").pack()
        remove_btn.pack()
        add_btn.pack()  


class AddProblems(tk.Frame):
    '''Creates a prob screen, which will used by admin to add/edit and remove problems from '''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)
        feedback_label = tk.Label(self, text="")
        feedback_label.pack()
        
    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        # create the question label
        add_problem_label = tk.Label(self, text="Please enter a new question", font=REGULAR_FONT, foreground="red")
        problem_entry = tk.Entry(self)
        feedback_label = tk.Label(self, text="")
        
        add_btn = ttk.Button(self, text="Add")
        # empty label to create some space between the top 
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        # place widges inside the grid
        add_problem_label.pack()
        problem_entry.pack()
        add_btn.pack(pady=20)
        feedback_label.pack()

    def press(self):
        #calls a function that tells the user if add was sucessfully,
        #displays appropriate message on label 
        feedback_label.config(text="Added Successfully!")

class RemoveProblems(tk.Frame):
    '''Screen to remove a problem from database'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)
        
    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
 
        # remove the question label and button
        remove_problem_label = tk.Label(self, text="Enter question ID to remove", font=REGULAR_FONT, foreground="red")
        problem_entry = tk.Entry(self)
        remove_btn = ttk.Button(self, text="Remove")
        #this label will display the result from a function that tells the user if remove was sucessful
        feedback_label = tk.Label(self, text = "")
        # empty label to create some space between the top 
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        # place widges inside the grid
        remove_problem_label.pack()
        problem_entry.pack()
        remove_btn.pack(pady=20)
        feedback_label.pack()
       
        
if __name__ == "__main__":
    app = AoS()
    app.mainloop()

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
        for F in (LoginScreen, HomeScreen):
            # here F is the name of the Screen
            frame = F(container, self)
            self.frames[F] = frame
            # with grid you can assign columns and rows to your
            # sticky determines (alignment + stretch) 
            # stretch the window to north south east or west (n,s,e,w)
            frame.grid(row=0, column=0, sticky="nsew")            
            
        self.show_frame(LoginScreen)

    def login(self, num):
        '''Function that continues to the next screen depending on if the
        login is valid. This function will take 1 as valid, and 0 as invalid.
        would work with boolean variables as well
        login(1)
        >>>(GUI opens HomeScreen)
        login(0)
        >>>Invalid Username or Password
        '''
        if (num == 0):
            # call the showframe function 
            self.show_frame(HomeScreen)
        else:
            print("Invalid username or password")


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
        self.credentials = {'Username' : '','Password': ''}
        self.init_window(controller)

        
    def create_login(self, controller):
        '''creates login button'''
        button = ttk.Button(self)
        button["text"] = "Login"
        button["command"] = lambda : controller.login(0)
        button.pack(pady=20)
    
    def create_entries(self):
        '''creates the entry fields for username and password'''
        # login text
        loginlbl = ttk.Label(self, text ="Please Log In: ",
                             font=APP_HIGHLIGHT_FONT)        
        # create the username and password fields
        username_label = tk.Label(self, text="Username", font=REGULAR_FONT)
        username_entry = tk.Entry(self)
        password_label = tk.Label(self, text="Password", font=REGULAR_FONT)
        # the show field of the password window makes sure that we only
        # show '*' when somebody types in the password
        password_entry = tk.Entry(self, show="*")
        loginlbl.pack()
        username_label.pack()
        username_entry.pack()
        password_label.pack()
        password_entry.pack()      
    
    def init_window(self, controller):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''        
        # empty label to create some space between the top 
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        # place our created label inside the
        self.create_entries()
        self.create_login(controller)


class HomeScreen(tk.Frame):
    ''' Homescreen that appears after the user logs in
    at the moment the homescreen is just a placeholder for some buttons'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window(controller)
    
    def create_logout_button(self, controller):
        ''' creates logout button'''
        # button will go to login screen
        logout_btn = ttk.Button(self)
        logout_btn["text"] = "Logout"
        logout_btn["command"] = lambda : controller.show_frame(LoginScreen)
        logout_btn.pack()
    
    def create_edit_problem_button(self):
        ''' creates edit problem button'''
        button = ttk.Button(self)
        button["text"] = "Edit Problems"
       # button["command"] = lambda : controller.showframe(EditProblemScreen)
        button.pack()
        
    def create_add_user_button(self):
        ''' creates add user button'''
        button = ttk.Button(self)
        button["text"] = "Add User"
       # button["command"] = lambda : controller.showframe(AddUserScreen)
        button.pack()
    
    def init_window(self, controller):
        ''' initialises the homescreen and its elements'''
        homescreen_label = ttk.Label(self, text="Home", font=APP_HIGHLIGHT_FONT)
        # just to get the formatting correct
        empty_label = ttk.Label(self, text="\n").pack()
        homescreen_label.pack()
        self.create_add_user_button()
        self.create_edit_problem_button()
        self.create_logout_button(controller)
        
        
if __name__ == "__main__":
    app = AoS()
    app.mainloop()
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
        
        frame = Problems(container, self)
        self.frames[Problems] = frame
        
        # with grid you can assign columns and rows to your
        # sticky determines (alignment + stretch) 
        # stretch the window to north south east or west (n,s,e,w)
        frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Problems)


    def show_frame(self, cont):
        ''' function that determines which of the screens will be viewed by
        the user. This function uses tkraise, in order to bring the
        wanted screen to the front'''
        # get the frame from the dictionary
        frame = self.frames[cont]
        frame.tkraise()


class LoginScreen(tk.Frame):
    '''Creates a login screen, which will be the 
    first screen of our Application'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window()
        
    def init_window(self):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        # login text
        loginlbl = ttk.Label(self, text ="Please Log In: ",
                             font=APP_HIGHLIGHT_FONT)
        # create the username and password fields
        username_label = tk.Label(self, text="Username", font=REGULAR_FONT, foreground="red")
        username_entry = tk.Entry(self, show="email address")
        password_label = tk.Label(self, text="Password", font=REGULAR_FONT, foreground="red")
        # the show field of the password window makes sure that we only
        # show '*' when somebody types in the password
        password_entry = tk.Entry(self, show="*")
        
        login_btn = ttk.Button(text="Login")
        
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
    '''Creates a prob screen, which will be the 
    first screen of our Application'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.init_window()
        
    def init_window(self):
        '''Initialises the GUI window and its elements
        Sets the different widgets that will be on the screen '''
        # login text
        addproblemlbl = ttk.Label(self, text ="Add a problem to the Question Bank",
                             font=APP_HIGHLIGHT_FONT)
        removeproblemlbl = ttk.Label(self, text ="Remove a problem from the Question Bank ",
                             font=APP_HIGHLIGHT_FONT)
        # create the username and password fields
        addproblem_label = tk.Label(self, text="Question", font=REGULAR_FONT, foreground="red")
        problem_entry = tk.Entry(self)
        
        add_btn = ttk.Button(text="Add")
        remove_btn = ttk.Button(text="Remove")
        # empty label to create some space between the top 
        # the entry labels
        empty_label = tk.Label(self, text="\n").pack()
        # place our created label inside the

        addproblem_label.pack()
        problem_entry.pack()
        add_btn.pack(pady=20)
        remove_btn.pack(pady=20)
        
if __name__ == "__main__":
    app = AoS()
    app.mainloop()

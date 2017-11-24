import tkinter as tk
from tkinter import ttk, font,  Tk, Label, Button, Entry,\
     StringVar, DISABLED, NORMAL, END, W, E
#from PIL import ImageTk, Image
from tkinter.messagebox import showinfo
import database_api as db
from gui_skeleton import *
from assignments import *
from all_grades import *
from latex import build_pdf

APP_HIGHLIGHT_FONT = ("Helvetica", 14, "bold")
REGULAR_FONT = ("Helvetica", 12, "normal")
TITLE_FONT = ("Helvetica", 14, "normal")
NICE_BLUE = "#3399FF"
HOME_FONT = ("Comic Sans", 26, "bold")

class DisplayLatex(GUISkeleton):
    '''class for an admin to view student grades'''
    def __init__(self, parent, controller, aid=None):    

        min_latex = (r"\documentclass{article}"
                     r"\begin{document}"
                     r"Hello, world!"
                     r"\end{document}")

        # this builds a pdf-file inside a temporary directory
        pdf = build_pdf(min_latex)
        display = self.create_label(self, (bytes(pdf)[:10]))
        display.grid(row=1,column=1)
        
        # look at the first few bytes of the header
        # print(bytes(pdf)[:10])
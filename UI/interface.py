import curses
from curses import wrapper, window
from curses.textpad import Textbox, rectangle

#Regex
import re

#Necessary for PuTTy
import os
import subprocess

#Necessary for environmental password configuration.
from decouple import config

#For reading and updating csv during runtime
import csv
from collections import defaultdict

#for cmd line args 
import sys
import getpass





class MenuBox:

    def __init__(stdscr):
        stdscr = stdscr
        options: list = []

    def text_box(text: str, topLeftCorner: int, topRightCorner: int, y: int):
        # loads options to screen
        rectangle(stdscr, 2,2,max_y-2,40)
        
        #if options to display = options[slice:y-1]

    def add_text_option(option: str):
        # Adds an option the list
        options.append(option) 



    def initial_start_screen():
        logo: str = """
        ██████╗███████╗███╗   ███╗
        ██╔════╝██╔════╝████╗ ████║
        ███████╗███████╗██╔████╔██║
        ╚════██║╚════██║██║╚██╔╝██║
        ███████║███████║██║ ╚═╝ ██║
        ╚══════╝╚══════╝╚═╝     ╚═╝
                                  
        """


       
    
#Need to create an intro screen with some SSM ascii

def start_screen():
    logo: str = """
    ██████╗███████╗███╗   ███╗
    ██╔════╝██╔════╝████╗ ████║
    ███████╗███████╗██╔████╔██║
    ╚════██║╚════██║██║╚██╔╝██║
    ███████║███████║██║ ╚═╝ ██║
    ╚══════╝╚══════╝╚═╝     ╚═╝
                              
    """

    stdscr(5, 30, )

def test_textpad(stdscr, insert_mode=False):
    #TODO make this text box size of window, then move hosts.csv here.  Have option to save to file, this function should return the information as a csv string.

    ncols, nlines = 40, 10 
    uly, ulx = 3, 2
    if insert_mode:
        mode = 'insert mode'
    else:
        mode = 'overwrite mode'

    stdscr.addstr(uly-3, ulx, "Use Ctrl-G to end editing (%s)." % mode)
    stdscr.addstr(uly-2, ulx, "Be sure to try typing in the lower-right corner.")
    win = curses.newwin(nlines, ncols, uly, ulx)
    rectangle(stdscr, uly-1, ulx-1, uly + nlines, ulx + ncols)
    stdscr.refresh()

    box = Textbox(win, insert_mode)
    contents = box.edit() # Getting the contents of the box as a string.

    stdscr.addstr(uly+ncols+2, 0, "Text entered in the box\n")
    stdscr.addstr(repr(contents))
    stdscr.addstr('\n')
    stdscr.addstr('Press any key')
    stdscr.getch()

    for i in range(3):
        stdscr.move(uly+ncols+2 + i, 0)
        stdscr.clrtoeol()




def start(stdscr):
    #test = MenuBox(stdscr)
    test_textpad(stdscr)





if __name__ == "__main__":   
    #NOTE this file is currently not used but planned for future implementations.

    wrapper(start)


    print("etst")

    





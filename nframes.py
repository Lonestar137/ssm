import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

#Regex
import re

#Necessary for PuTTy
import os

#Necessary for environmental password configuration.
from decouple import config



def extra_text(stdscr):
    #Extra text on the rectangle, i.e., (?) help or (q) quit
    stdscr.addstr(2, 3, 'SSH Sessions', curses.A_UNDERLINE)
    stdscr.addstr(2, 30, '(?) Help')
    stdscr.addstr(45, 30, '(q) Quit')

def print_list(stdscr, lst: list, y: int, x:int):

    #How many hosts should be spawned.
    y_limit=46

    for i in lst:
        if y < y_limit:
            stdscr.addstr(y,x, str(i)+'\t\t\t')
            y+=1
        else:
            break

def queue(stdscr):
    global my_list
    list_x=3 #X of list objects
    list_y=3

    #Regex to match the full IP address pattern.
    ip_pattern=re.compile("([0-9].+)")

    try:
        print_list(stdscr, my_list, list_y, list_x)
    except:
        pass

    pointer = int(len(my_list)/2)
    if pointer > 20:
        pointer = 15# Prevents the cursor from going off the screen.

    #Ensures that the key is made at startup, i.e. if pointer lands on folder it won't error out because key is never created.
    key_made=False

    while True:

        selected_item = str(my_list[pointer])

        #Place highlighted ontop of the list.  But place selected object in the center always.
        stdscr.addstr(list_y+pointer, list_x, '\t\t'+selected_item, curses.A_STANDOUT)

        #Frame, try - to prevent crash if window size becomes too small.
        try:
            rectangle(stdscr, 2,2,45,40)
            extra_text(stdscr)
        except:
            pass

        #If keymade and the current selected item does not match IP pattern then pass else get key press.
        if key_made == True and ip_pattern.fullmatch(selected_item) == None:
            pass#Key should stay equal to your last movement to move you up or down.
        else:
            key = stdscr.getkey()
            key_made = True

        if key in ['k', 'KEY_UP']:
            #Press j key to increment list down.
            last_index = len(my_list)-1
            my_list.insert(0, my_list[last_index])

            last_index = len(my_list)-1
            my_list.pop(last_index)
        elif key in ['j', 'KEY_DOWN']:
            #Press k key to incrment list up.
            last_index = len(my_list)-1
            my_list.append(my_list[0])

            last_index = len(my_list)-1
            my_list.pop(0)
        elif key in ['l', 'KEY_RIGHT']:
            server = selected_item
            user='user'
            passw='pass'
            #Putty config here
            os.system('putty -ssh -l '+user+' -pw '+passw+' '+server+' &')
            pass
        elif key == 'q':
            #q to quit
            exit()
        else:
            pass

        stdscr.refresh()
        try:
            print_list(stdscr, my_list, list_y, list_x)
        except:
            pass


def read_csv(csv_file):
    #TODO: Generate list of hosts from a csv file.
    pass
    # returns list



PATH = './hosts.csv'
read_csv(PATH)

#my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
my_list = ['127.0.0.1', 'A test']
for i in range(20):
    my_list.append('10.100.1.'+str(i))

wrapper(queue)

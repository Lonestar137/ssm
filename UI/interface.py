import curses
from curses import wrapper, window
from curses.textpad import Textbox, rectangle

#Regex
import re

#Necessary for PuTTy
import os, subprocess, platform

#Necessary for environmental password configuration.
from decouple import config

#For reading and updating csv during runtime
import csv
from collections import defaultdict

#for cmd line args 
import sys
import getpass

from UI.datastore import *
#from datastore import *

def prune_env(envuser: str, envpass: str):
    # Remove all the non used env variables from .env
    # # Remove all the non used env variables from .env
    create_env_variable('NULL', envuser, envpass)

def delete_host(location, ip):
    my_list, SSH_USER, SSH_PASS, unique_hosts_dict, PLATFORM = initiate_vars()
    pass

def create_env_variable(possible_env_var_name: str, username: str, password: str):
    #Checks .env to see if the password already exists, if not create new one, elif exists use original.

    if(password == ''):
        return '', ''

    with open(datastore+'/.env', 'r') as f:
        file = f.read().split('\n')

    values_keys = dict()
    for line in file:
        if(line.find('=') != -1):
            pv = line.strip().split('=')
            values_keys.update({pv[1]: pv[0]})

    if(username in values_keys and password in values_keys):
        #password exists, return the existing envvar name
        return values_keys[username], values_keys[password]
    else:
        #if not exists, add to .env and return new variables.
        name = possible_env_var_name
        index = str(len(values_keys))
        envuser, envpassw = name+'User'+index, name+'Pass'+index

        #Write the changes.
        with open(datastore+'/.env', 'a') as f:
            newVariables = f'\n{envuser}={username}\n{envpassw}={password}'
            file = f.write(newVariables)

        return envuser, envpassw
    


def new_host_screen(stdscr):
    #               (y, x, field, answer)
    options: list = [(3, 3, "location: ", ""), (4, 3, "ip: ", ""), (5, 3, "username: ", ""), (6, 3, "password: ", ""), (7, 3, "ssh_key: ", "")]
    curr_option = 0
    while True:

        max_y, max_x=window.getmaxyx(stdscr)
        rectangle(stdscr, 2,2,len(options)+3,40)
        stdscr.addstr(2,3,"Add a host:", curses.A_UNDERLINE | curses.A_BOLD | curses.color_pair(1))
        stdscr.refresh()
        stdscr.addstr(len(options)+3,3,"(<=) Back, (Enter) Save ", curses.color_pair(2))
        stdscr.addstr(len(options)+4,3,"(=>) Batch create", curses.color_pair(2))

        for option in options:
            #Hide password as it's printed
            if(option[2] == 'password: '):
                hiddenpass = option[3].replace(option[3], '*') * len(option[3])
                stdscr.addstr(option[0], option[1], option[2]+hiddenpass)
            else:
                stdscr.addstr(option[0], option[1], option[2]+option[3])

        if(curr_option == 3):
            # Hide password as it's typed.
            hiddenpass = options[curr_option][3].replace(options[curr_option][3], '*') * len(options[curr_option][3])
            stdscr.addstr(options[curr_option][0],
                    options[curr_option][1],
                    options[curr_option][2]+hiddenpass)

        else:
            stdscr.addstr(options[curr_option][0],
                    options[curr_option][1],
                    options[curr_option][2]+options[curr_option][3])

        key = stdscr.getkey()
        stdscr.clear()
        if(key == "KEY_DOWN"):
            if(curr_option == -1 or curr_option == len(options)-1):
                curr_option = 0
            else:
                curr_option += 1

            stdscr.addstr(options[curr_option][0],
                    options[curr_option][1], 
                    options[curr_option][2]+options[curr_option][3],
                    curses.A_STANDOUT)
        elif(key == "KEY_UP"):
            if(curr_option == -1 or curr_option == len(options)):
                curr_option = len(options)-1
            else:
                curr_option -= 1
            stdscr.addstr(options[curr_option][0],
                    options[curr_option][1],
                    options[curr_option][2]+options[curr_option][3],
                    curses.A_STANDOUT)
        elif(key in ["KEY_LEFT"]):
            break
        elif(key in ["KEY_RIGHT"]):
            #Open hosts.csv in editor.
            try:
                if(platform.system() == "Darwin"): #if mac
                    subprocess.call(('open', datastore+'/hosts.csv'))
                elif(platform.system() == "Windows"):
                    os.system("start " + datastore+'\\hosts.csv')
                else:
                    subprocess.call(('xdg-open', datastore+'/hosts.csv'))
            except Exception as e:
                stdscr.clear()
                stdscr.addstr(1,1,"An exception occurred: \n"+ str(e))
                stdscr.getch()
                break

        elif(key == "KEY_BACKSPACE"):
            stdscr.refresh()
            options[curr_option] = (options[curr_option][0], 
                    options[curr_option][1], 
                    options[curr_option][2],
                    options[curr_option][3][:-1])
        elif(key == "\n"):
            envVarUser, envVariablePass = create_env_variable(options[0][3], options[2][3], options[3][3]) #generate envvar from location if it doesn't already exist.
            csv_line = f'{options[0][3]},{options[1][3]},{envVarUser},{envVariablePass},{options[4][3]}'

            stdscr.addstr(len(options)-1, options[curr_option][1], 'Save the following host?(y/n)')
            stdscr.addstr(len(options), options[curr_option][1], csv_line)
            key = stdscr.getkey()
            if(key in ['\n', 'y', 'Y', 'yes', 'Yes']):
                #Append the new host to the hosts.csv
                stdscr.addstr(len(options)+1, options[curr_option][1], "Saved!")
                with open(datastore+'/hosts.csv', 'a') as f:
                    f.write('\n'+csv_line)
                
                stdscr.getch()
                stdscr.clear()
            else:
                stdscr.clear()
                
        else:
            options[curr_option] = (options[curr_option][0], 
                    options[curr_option][1],
                    options[curr_option][2],
                    options[curr_option][3]+ key)







if __name__ == "__main__":   
    #NOTE this file is currently not used but planned for future implementations.
    wrapper(new_host_screen())

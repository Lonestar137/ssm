import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

import json 
import os

from decouple import config





class frame:
    def __init_(self):
        pass

    def movement(self):
        # Allows for VIM movement inside wrapper.
        pass

    def new_option(self):
        #Creates a new object(folder or host) in sorted colleciotn
        pass

    def del_option(self):
        #deletes an object from collection.
        pass


#PLAYGROUND
#

def print_key(stdscr):
    #Prints the key number
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    BLUE_AND_YELLOW = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    ORANGE_AND_WHITE = curses.color_pair(3)

    key = stdscr.getkey()
    stdscr.addstr(5, 5, f'Key: {key}')
    stdscr.getch()

def movement(stdscr):
    USER = config('SSH_USER')
    PASS = config('SSH_PASS')
    PATH = config('HOST_PATH')
    #Basic movement function
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    BLUE_AND_YELLOW = curses.color_pair(1)
    GREEN_AND_BLACK = curses.color_pair(2)
    ORANGE_AND_WHITE = curses.color_pair(3)

    #Define menu options.
    options = user_input(stdscr)

    #Cursor start position
    x, y = 3, 3

    #Menu choice
    selection = 0
    while True:

        #Try block prevents stdscr from blocking.
        try:
            key = stdscr.getkey()
        except:
            pass

        if key in ["KEY_LEFT", 'h', 'H']:
            pass
            #x -= 1 #For movement
        elif key in ["KEY_RIGHT", 'l', 'L']:
            ssh_into(stdscr, options[selection][2], USER, PASS)

            #x += 1 #For movement
        elif key in ["KEY_UP", 'k', 'K']:
            #y -= 1
            if selection == 0:
                selection = len(options)-1
            else:
                selection -= 1

        elif key in ["KEY_DOWN", 'j', 'J']:
            if selection == len(options)-1:
                selection = 0
            else: 
                #y += 1
                selection += 1
        elif key == 'q':
            exit()
        elif key == 'N':
            stdscr.addstr(1, 5, 'Add new SITE:')
            win = curses.newwin(1, 30, 1, 19)
            box = Textbox(win)
            stdscr.refresh()
            box.edit()
            new_site = box.gather()

        elif key == 'n':
            stdscr.addstr(1, 5, 'Add new HOST:')
            win = curses.newwin(1, 30, 1, 19)
            box = Textbox(win)
            stdscr.refresh()
            box.edit()
            new_site = box.gather()
            
        elif key in ['/']:
            #Search function
            pass
        elif key in ['?', '.']:
            stdscr.addstr(2, 42, 'Movement Keys', curses.A_UNDERLINE)
            #Dynamic help menu space allocation.
            for i in [(3, 42, 'j-up'), (4, 42,'k-down'), (5, 42,'h-left'),
                    (6, 42,'l-right'),(7, 42, 'Session', True),(8,42,'Enter-Open Session'),
                    (9, 42, 'Creation', True),(10, 42,'n-Create new Host'), (11, 42, 'N-Create new SITE')]:
                _x = i[1]
                _y = i[0]
                text=i[2]

                #For headers, if its a header underline it.
                try:
                    i[3] == True
                    stdscr.addstr(_y, _x, text, curses.A_UNDERLINE)
                except:
                    stdscr.addstr(_y, _x, text)


            stdscr.getkey()#Blocker so you can read it.



        stdscr.clear()

        #Frame function, also defined before key loop.
        options = user_input(stdscr)

        #Debugger: Coords marker on cursor.
        #stdscr.addstr(y,x+20,'<---',curses.A_STANDOUT)
        stdscr.addstr(0,0,key)

        #Selection menu choices
        y_of_opt = options[selection][0]
        x_of_opt = options[selection][1]
        opt_text = options[selection][2]
        stdscr.addstr(y_of_opt, x_of_opt, '\t\t'+opt_text, curses.A_STANDOUT)

        stdscr.refresh()

def user_input(stdscr):
    #Creates Box Frame and takes user input
    rectangle(stdscr, 2,2,45,40)
    stdscr.addstr(2,3, 'SSH Sessions')
    stdscr.addstr(2,30, '(?) Help')
    #Quit
    stdscr.addstr(45,30, '(q) Quit')

    #Generate session
    global ssh_sessions #import Dictionary
    pos=3
    options=[]
    for folder, hosts in ssh_sessions.items():
        stdscr.addstr(pos, 3, folder)
        pos+=1
        for host in hosts:
            stdscr.addstr(pos, 3, '\t'+host)
            options.append((pos, 3, host))
            pos+=1


    stdscr.refresh()
    return options

def ssh_into(stdscr, server, user, passw):
    #Creates an interactive SSH session.

    #Import paramiko
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(server, username=user, password=passw)

    #(topleft_y, topleft_x, bottomright_x, bottomleft_y)
    #rectangle(stdscr, 2, 42, 50 ,100)

    #win = curses.newwin(2, 40, 50, 48)
    #win.addstr(0,0, prompt)

    #SSH session BOX
    #stdscr.addstr(2, 43, server)
    stdscr.refresh()


    #os.system("xterm -hold -e sshpass -p ${SSH_PASS} ssh -o 'UserKnownHostsFile=/dev/null' -o 'StrictHostKeyChecking=no' ${SSH_USER}@10.$1.1.$2 &")
    os.system("putty -ssh -l "+user+" -pw "+passw+" "+server+" &")
    #os.system('xterm')
    stdscr.getch()
    #stdscr.addstr(1, 70, x.stdout)
    #opt = stdout.readlines()
    #opt = "".join(opt)
                              #Ht  wd  y   x
    #output_win = curses.newwin(49, 50, 3, 43) #TOOD: FIgure out why if you set x(10) to 42 it doesn't appear in the rectangle..
    #output_win.addstr(cmd_output)
    #output_win.refresh()


    #print(opt)
    #stdscr.addstr(2,50, opt)


    #TODO Placeholder prompt generation, needs to be replaced with mroe efficient solution.
    #if cmd.find('conf t') != -1 or cmd.find('configure t') != -1:
    #    prompt = '(config)# '

    #if prompt == '(config)#' and cmd in ['exit', 'Exit', 'end']:
    #    prompt = '# '
    #elif cmd in ['Exit', 'exit']:
    #    break

PATH = config('HOST_PATH')
hosts_file = open(PATH)
ssh_sessions = json.load(hosts_file)

#wrapper(print_key)
wrapper(movement)
#wrapper(user_input)

hosts_file.close()

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
    key = stdscr.getkey()
    stdscr.addstr(5, 5, f'Key: {key}')
    stdscr.getch()

def movement(stdscr):
    USER = config('SSH_USER')
    PASS = config('SSH_PASS')
    PATH = config('HOST_PATH')

    #Define menu options.
    options = user_input(stdscr)
    curr_display=[]
    for i in range(3, 45):
        curr_display.append(options[i-3])
        stdscr.addstr(i, options[i-3][1], options[i-3][2] +'\t\t')

    stdscr.addstr(15,35, curr_display[len(curr_display)-1][2]+' Tail')

    #Cursor start position
    x, y = 3, 3

    #Menu choice
    selection = 1
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
            if selection == 1:
                selection = len(options)-1 #Sends to bottom side of list if hit top
                
            else:
                selection -= 1
                curr_display.pop(len(curr_display)-1)
                curr_display.insert(0, options[selection])

        elif key in ["KEY_DOWN", 'j', 'J']:
            if selection == len(options)-1:
                selection = 0 #Sends to top if hit bottom
                
            #elif options[selection+1][2].find('\t') == -1:
            #    selection+=2
            #    curr_display.pop(0)
            #    curr_display.insert(len(curr_display)-1, options[selection-1])
            else: 
                #y += 1
                selection += 1
                curr_display.pop(0)
                #curr_display.insert(len(curr_display)-1, options[selection])
                curr_display.append(options[selection])
        elif key == 'q':
            exit()
        elif key == 'N':
            stdscr.addstr(1, 5, 'Add new SITE:')
            win = curses.newwin(1, 30, 1, 19)
            box = Textbox(win)
            stdscr.refresh()
            box.edit()
            new_site = box.gather()
            if new_site in ['', ' ']:
                #SKip and dont add to list.
                pass
            else:
                import json
                site = {new_site: []}
                with open(PATH, mode='a',encoding='utf-8') as hosts_file:
                    file_data = json.load(hosts_file)
                    json.dump(site, hosts_file)

                #add to list.
                stdscr.refresh()

        elif key == 'n':
            stdscr.addstr(1, 5, 'Add new HOST:')
            win = curses.newwin(1, 30, 1, 19)
            box = Textbox(win)
            stdscr.refresh()
            box.edit()
            new_host = box.gather()
            
        elif key in ['/']:
            #Search function
            stdscr.addstr(1, 5, 'Search:')
            win = curses.newwin(1, 30, 1, 19)
            box = Textbox(win)
            stdscr.refresh()
            box.edit()
            new_host = box.gather()
            #TODO Create a function which takes a list and makes a queue.



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



        #stdscr.clear() #Necessary if you don't put options[txt]\t\t on the i==selection for
        stdscr.refresh()

        #Frame function, also defined before key loop.
        options = user_input(stdscr)

        stdscr.addstr(0,0,key)

        #Selection menu choices
        y_of_opt = options[selection][0]
        x_of_opt = options[selection][1]
        opt_text = options[selection][2]

        for i in range(3, 45):
            stdscr.addstr(i, curr_display[i-3][1], curr_display[i-3][2] +'\t\t\t')
            

        stdscr.addstr(44, x_of_opt, '\t'+opt_text, curses.A_STANDOUT)
            

        #for i in range(0, len(options)):
        #    if i > 41:
        #        continue


        #    if options[selection][2].find('\t') == -1:
        #        try:
        #            if key in ['j', 'J', 'key.DOWN']:
        #                selection+=1
        #            elif key in ['k', 'K', 'key.UP'] and selection != 1:
        #                selection-=1
        #        except:
        #            pass

        #    if i == selection:
        #        opt_text = options[selection][2]
        #        try:
        #            stdscr.addstr(i+3, x_of_opt, '\t'+opt_text, curses.A_STANDOUT)
        #        except:
        #            pass
        #    else:
        #        try:
        #            stdscr.addstr(i+3, x_of_opt, options[i][2] +'\t\t')#\t\t is used to clear the screen more efficiently.
        #        except:
        #            pass


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
        pos+=1
        #stdscr.addstr(pos, 3, folder)
        options.append((pos, 3, folder))
        for host in hosts:
            #stdscr.addstr(pos, 3, '\t'+host)

            options.append((pos, 3, '\t'+host))
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
started=False

#wrapper(print_key)
wrapper(movement)
#wrapper(user_input)

hosts_file.close()

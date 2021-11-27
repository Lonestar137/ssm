import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle

#Regex
import re

#Necessary for PuTTy
import os

#Necessary for environmental password configuration.
from decouple import config

#For reading and updating csv during runtime
import csv
from collections import defaultdict



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
    #global my_list
    my_list, SSH_USER, SSH_PASS, unique_hosts_dict = initiate_vars()

    list_x=3 #X of list objects
    list_y=3

    #Regex to match the full IP address pattern.
    ip_pattern=re.compile("\t([0-9].+)")

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
            #Open press l, opens up a putty session on the selected device.
            server = selected_item
            found = False
            #Putty config here
            #If the server has a unique password.
            for folder, hosts in unique_hosts_dict.items():
                for host in hosts:
                    if server[1:] == host[0]:#[1:] because server has tab at start
                        #The .env variable needs to be assigned in the .csv file in the username/password fields.
                        UNIQUE_USER = config(host[1])
                        UNIQUE_PASS = config(host[2])
                        os.system('putty -ssh -l '+UNIQUE_USER+' -pw '+UNIQUE_PASS+' '+server+' &')
                        found = True
                    else:
                        pass

            if found == False:
                os.system('putty -ssh -l '+SSH_USER+' -pw '+SSH_PASS+' '+server+' &')
        elif key == 'n':
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

    unique_hosts=defaultdict(list)
    hosts = defaultdict(list)
    with open(csv_file, newline='') as hosts_file:
        reader = csv.DictReader(hosts_file)
        for row in reader:
            if row['username'] != None and row['password'] != None:
                unique_hosts[row['location']].append((row['ip'], row['username'], row['password']))

            hosts[row['location']].append(row['ip'])

    return dict(hosts), dict(unique_hosts)

def read_csv2(csv_file):

    with open(csv_file, newline='') as hosts_file:
        comma_sep_string = ''
        reader=csv.reader(hosts_file)
        for row in reader:
            comma_sep_string += ','.join(row)
            comma_sep_string +='\n'

    print(comma_sep_string)
    return comma_sep_string

def dict_to_list(data: dict):
    #generates a list from csv dictinoary.
    data_list=[]

    for folder, hosts in data.items():
        data_list.append(folder)
        for host in hosts:
            data_list.append('\t'+host)
    return data_list

def initiate_vars():
    #Grabs credentials and host dict as defined in hosts.csv and .env
    PATH = config('HOST_PATH')
    SSH_USER = config('SSH_USER')
    SSH_PASS = config('SSH_PASS')

    #Create dictionary
    hosts_dict, unique_hosts_dict = read_csv(PATH)
    hosts_list = dict_to_list(hosts_dict)
    print(unique_hosts_dict)

    return hosts_list, SSH_USER, SSH_PASS, dict(unique_hosts_dict)



if __name__ == "__main__":
   wrapper(queue)
   exit()
   x,y,z, unique = initiate_vars()
   for folder, hosts in unique.items():
       for i in hosts:
           print(i)




   #read_csv('hosts.csv')

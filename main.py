import time
import curses
import xml.etree.ElementTree as ET

#pip3 install python-decouple
from decouple import config


def main_menu(stdscr):
    curses.curs_set(0)
    
    h, w = stdscr.getmaxyx()
    text = "SSH Manager"

    x=w//2 - len(text)//2
    y=h//2

    stdscr.addstr(y, x, text) 
    selection=0
    options=["SSH", "Options", "Exit"]
    while True:

        if selection == -1:
            selection = len(options)-1

        key = stdscr.getch()
        if key == curses.KEY_DOWN: 
            #Print num
            stdscr.addstr(y, x-5, str(selection))

            selection+=1
            stdscr.clear()
            if selection == len(options):#3:
                selection = 0

            try:
                stdscr.addstr(y+1,x,options[selection+1])
            except:
                stdscr.addstr(y+1,x, options[0])

            stdscr.addstr(y,x, options[selection], curses.A_BOLD)
            stdscr.addstr(y-1,x, options[selection-1])
        elif key == curses.KEY_UP:
            #Print num
            stdscr.addstr(y, x-5, str(selection))

            selection-=1
            stdscr.clear()

            stdscr.addstr(y+1,x,options[selection+1])
            stdscr.addstr(y,x, options[selection], curses.A_BOLD)
            try:
                stdscr.addstr(y-1,x, options[selection-1])
            except:
                stdscr.addstr(y-1,x, options[0])
                

        elif key == curses.KEY_ENTER or key in [10, 13]: # or if key value in list to detect other ENTER key types.
            #Takes indicated selection and decides.
            stdscr.clear()
            if options[selection] == 'SSH':
                break
            elif options[selection] == 'Exit':
                exit()
            else:
                stdscr.addstr(y,x,"Option: "+options[selection]+" is not implemented yet.")



    #Generates selection.
    if options[selection] == 'SSH':
#        stdscr.addstr(0, 0, 'Birmingham')
#        for i in range(10):
#            stdscr.addstr(i+1, 5, '10.30.1.'+str(i))

        #Temporary for MVP(Min Viable Product)
         nodes=[]
         i=0
         for folder in root:
             stdscr.addstr(i,0,folder.attrib['name'])
             i+=1
             if folder.attrib['type'] == 'folder':
                 for district in folder:
                     stdscr.addstr(i,0,'\t'+district.attrib['name'])
                     i+=1

                     if district.attrib['type'] == 'folder':
                         for host in district:
                             nodes.append((host.attrib['name'], i, 0))
                             stdscr.addstr(i,0,'\t\t'+host.attrib['name'])
                             i+=1

             else:
                 print('Not in folder ', folder.attrib['name'])

             pass

         stdscr.refresh()
         # Movement
         choice=0
         while True:
             if key == curses.KEY_UP:
                 choice+=1
             elif key == curses.KEY_DOWN:
                 choice-=1

             x=nodes[choice][2]
             y=nodes[choice][1]
             host=nodes[choice][0]
             stdscr.addstr(y,x,host)


    stdscr.refresh()
    time.sleep(10)



if __name__ == "__main__":
    #GRAB SSH Credentials as defined in .env file.
    USER = config('SSH_USER')
    PASS = config('SSH_PASS')

    tree = ET.parse('TestDatabase.dat')
    root = tree.getroot()


    #print(USER, PASS)

    #Starts gui
    curses.wrapper(main_menu)
    #
    #

#NOTE
#for i in hosts.items()
#Yaml returns
#{'Site': [
#{'Device': {'IP': '10xxxx', 'Hostname': 'Router', 'SSH_USER': 'Environment', 'SSH_PASS': 'Environment'}},
#{'10.30.1.2': {'IP': '10xxxxxx', 'Hostname': 'test', 'SSH_USER': 'Environment', 'SSH_PASS': Environment}},
#{'etc. . .': {'IP': 'etc. . .'}}
#]}

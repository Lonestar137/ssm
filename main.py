import time
import curses

#pip3 install yaml
import yaml

#pip3 install python-decouple
from decouple import config


def process_ips(yaml_file)->str:
    with open(yaml_file) as stream:
        try:
            #print(yaml.safe_load(stream))
            data = yaml.safe_load(stream)
            for sites in data.items():
                for site_name in sites:
                    if site_name == '3rd Div Birmingham':
                        return print(site_name)
                #    if device == '3rd Div Birmingham':
                #        print(device)
        except yaml.YAMLError as exc:
            print(exc)


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



    if options[selection] == 'SSH':
        stdscr.addstr(0, 0, 'Birmingham')
        for i in range(10):
            stdscr.addstr(i+1, 5, '10.30.1.'+str(i))

    stdscr.refresh()
    time.sleep(10)




if __name__ == "__main__":
    #GRAB SSH Credentials as defined in .env file.
    USER = config('SSH_USER')
    PASS = config('SSH_PASS')

    process_ips('ALDOT.yaml')
    #print(USER, PASS)

    #Starts gui
    #curses.wrapper(main_menu)
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

from decouple import config
import requests


def server_request(user: str, password: str, server: str, payload: dict):
    #Sends request to server.

    s = requests.Session()
    s.trust_env = False
    response = s.post(server, 
            verify=False,
            auth=(user, password),
            json=payload,
            headers={'Accept': 'application/json', 'X-HTTP-Method-Override': 'GET'})
    
    return response.json()

def parse_dict(hosts: dict):
    #Parses Icinga Response dictionary and creates tuple list (address, color_pair)
    host_list=[]
    for group_tuple in hosts.items():
        for x in group_tuple[1]:
            for y in x:
                print(x['attrs'])
                #print(x['joins']['host']['address']) #Prints host names of all devices.
                if x['attrs']['state'] == 2.0:
                    address=x['joins']['host']['address']
                    host_list.append((address, 3))
                elif x['attrs']['state'] == 1.0:
                    address=x['joins']['host']['address']
                    host_list.append((address, 2))
    #print(host_list)
    return host_list

 
def render_list(stdscr, y: int, x: int, lst: list):
    import curses
    from curses import window
    #Renders a TUP_LIST to the screen ('str', 2) str, color_pair_num

    #State color definitions
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)

    #Find window definitions
    y_limit, x_limit = window.getmaxyx(stdscr)

    #Starting y position
    pos=y
    stdscr.addstr(pos-1,x,'Host problems',curses.A_UNDERLINE)
    for i in lst:
        if pos < y_limit:
            try:
                #Render hosts with associated active state
                stdscr.addstr(pos,x,i[0],curses.color_pair(i[1]))
                pos+=1
            except:
                pass
    stdscr.refresh()

if __name__ == '__main__':
    #for testing purposes only:

    import curses
    from curses import wrapper

    load = {'joins': ['host.name', 'host.address', 'host.vars'],
            'attrs' : ['name', 'state', 'downtime_depth', 'acknowledgement'],
            #'filter': 'service.state != ServiceOK && service.downtime_depth == 0.0 && service.acknowledgement == 0.0'}
            'filter': 'match(host.vars.tenant, \"WC Region\") &&  service.state != ServiceOK && service.downtime_depth == 0.0 && service.acknowledgement == 0.0'}


    USER = config('MONITOR_USER')
    PASS = config('MONITOR_PASS')
    SERVER = config('MONITOR_URL')

    hosts = server_request(USER, PASS, SERVER, load)
    print(hosts['results'][1])#Prints first host in the response
    exit()

    hosts_tup_list=parse_dict(hosts)

    wrapper(render_list, 1, 1, hosts_tup_list)




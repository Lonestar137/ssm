import time
import nframes
from nframes import queue
from nframes import initiate_vars
from curses import wrapper
from decouple import config

import monitor


try:
    load = {'joins': ['host.name', 'host.address', 'host.vars', 'host'],
            'attrs' : ['name', 'state', 'downtime_depth', 'acknowledgement'],
            #'filter': 'service.state != ServiceOK && service.downtime_depth == 0.0 && service.acknowledgement == 0.0'}
            'filter': 'match(host.vars.tenant, \"Network Operations\") &&  service.state != ServiceOK && service.downtime_depth == 0.0 && service.acknowledgement == 0.0'}


    USER = config('MONITOR_USER')
    PASS = config('MONITOR_PASS')
    SERVER = config('MONITOR_URL')

    hosts = monitor.server_request(USER, PASS, SERVER, load)
    hosts_tup_list=monitor.parse_dict(hosts)
    wrapper(monitor.render_list, 3, 50, hosts_tup_list)

except:
    pass


#The only relevant line of code if not using a monitor server.
initiate_vars()
wrapper(queue)

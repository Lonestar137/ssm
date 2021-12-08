from nframes import queue
from curses import wrapper
from decouple import config
import monitor
from monitor import render_list

import Threading

#try:
payload = {'joins': ['host.name', 'host.address', 'host.vars'],
        'attrs' : ['name', 'state', 'downtime_depth', 'acknowledgement'],
        'filter': 'match(host.vars.tenant, \"Network Operations\") && service.state != ServiceOK && service.downtime_depth == 0.0 && service.acknowledgement == 0.0'}


USER = config('MONITOR_USER')
PASS = config('MONITOR_PASS')
SERVER = config('MONITOR_URL')

hosts = monitor.server_request(USER, PASS, SERVER, payload)
hosts_tup_list=monitor.parse_dict(hosts)
wrapper(render_list, 3, 50, hosts_tup_list)
#except:
    # TODO print request status code in-case it failed.
#    pass


wrapper(queue)

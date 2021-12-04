from nframes import queue
from curses import wrapper
from decouple import config

Host_server_exists=False
try:
    Host_server_exists=config("HOST_SERVER")
except:
    pass


wrapper(queue)

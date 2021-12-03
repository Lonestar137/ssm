import json
from decouple import config

#This is a debugging file.  Please ignore.


PATH=config('PATH')

with open(PATH, mode='a', encoding='utf-8') as hosts_file:
    file_data = json.load(hosts_file)
    import pdb
    pdb.set_trace()




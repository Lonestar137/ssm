
## Simple SSH Manager (SSM)


SSM is a lightweight Python(ncurses) based SSH manager.

### Installation
1. Download the python dependencies: curses(ncurses), python-decouple.  
   `pip3 install windows-curses python-decouple`

2. Clone the repo into a directory of your choosing.  
   `git clone https://github.com/Lonestar137/ssm.git`

3. Then, rename the `env` file to `.env`. Edit the file and define your credentials inside like so:
    `SSH_USER=yourUSER
    SSH_PASS=yourPASS
    HOST_FILE=path/to/your/file/with/hosts.json`
By default `SSH_USER` and `SSH_PASS` will be used on all sessions unless you specify a different variable in the `hosts.csv` username and password fields.

4. Make sure to create `hosts.csv` and add your sessions following the format found in `example-hosts.csv`.  You can add unique passwords to each session by specifying a .env variable in the `username` and `password` fields.  Just make sure that you define the variable in the .env like you did with `SSH_USER` and `SSH_PASS`.

4. Afterward, you can start the application from that directory with:
   `python3 nframes.py`

5. You can create a shell script/alias if you're on a Unix-like system to easily call the program from anywhere on the system, or if you're on Windows, you can create a batch file or shortcut.







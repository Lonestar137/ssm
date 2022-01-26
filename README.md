
## Simple SSH Manager (SSM)


SSM is a lightweight Python(ncurses) based SSH manager.

### Installation
1. Clone the repo into a directory of your choosing.  
   `git clone https://github.com/Lonestar137/ssm.git`

2. Download the python dependencies: curses(ncurses), python-decouple.   
   `pip3 install windows-curses python-decouple`  
   Install a supported SSH terminal handler for your OS:

   **Ubuntu(Linux)**  
   Make sure you have gnome-terminal, putty, or xterm installed.  
   `sudo apt install putty` or `xterm`
   gnome-terminal should be installed by default on standard Ubuntu/GNOME based distros.

   Defining which terminal to use will be covered in the next step.

   **Windows**  
   Download the [putty](https://www.putty.org/) .exe file and place it in the /ssm folder(The same folder as `nframes.py`).  


3. Then, rename the `env` file to `.env`. Edit the file and define your credentials inside like so:  
    SSH_USER=yourUSER
    SSH_PASS=yourPASS
    HOST_FILE=path/to/your/file/with/hosts.json  

   Note: Environment variables can be defined anywhere your system supports but it's easier to manage from .env file as the file will override any conflicting environment variables on runtime.


By default `SSH_USER` and `SSH_PASS` will be used on all sessions unless you specify a different variable in the `hosts.csv` username and password fields.  
You can define unique username and password for each host if you wish, otherwise `SSH_USER` and `SSH_PASS` will be used on that host.

In the `.env` file, set `PLATFORM` equal to one of the supported SSH terminals.
For example:  `PLATFORM=putty-windows` or `PLATFORM=gnome-terminal`  
Options:
    putty-linux, putty-windows, gnome-terminal, xterm-terminal

4. Make sure to create `hosts.csv` and add your sessions following the format found in `example-hosts.csv`.  You can add unique passwords to each session by specifying a .env variable in the `username` and `password` fields.  Just make sure that you define the variable in the .env like you did with `SSH_USER` and `SSH_PASS`.  
Examples are provided in example hosts and the initial env file.

5. Afterward, you can start the application from that directory by typing in a terminal:
   `python3 nframes.py` or `python3 /path/to/file/nframes.py` if you're in another dir.

6. You can create a shell script/alias if you're on a Unix-like system to easily call the program from anywhere on the system, or if you're on Windows, you can create a batch file or shortcut.







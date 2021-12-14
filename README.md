
## Simple SSH Manager (SSM)


SSM is a lightweight Python(ncurses) based SSH manager.

### Installation
1. Clone the repo into a directory of your choosing.  
   `git clone https://github.com/Lonestar137/ssm.git`

2. Download the python dependencies: curses(ncurses), python-decouple.   
   `pip3 install windows-curses python-decouple`  
   Install putty for your OS:

   **Ubuntu(Linux)**  
   Make sure you have gnome-terminal installed.  

   (Optional)
   Or, optionally you can enable putty terminal:
   `sudo apt install putty`  

   NOTE: To use PuTTy, just uncomment the two lines with `os.system('putty . . .')` and comment the two lines with `os.system('gnome-terminal . . .')` inside the `nframes.py` file.

   **Windows**  
   Download the [putty](https://www.putty.org/) .exe file and place it in the /ssm folder(The same folder as `nframes.py`).  
   Open `nframes.py` and change the line `putty -ssh -l...` to `putty.exe -ssh -l ...`.

   To use PuTTy, just uncomment the two lines with `os.system('putty . . .')` and comment the two lines with `os.system('gnome-terminal . . .')` inside the `nframes.py` file.

3. Then, rename the `env` file to `.env`. Edit the file and define your credentials inside like so:  
    SSH_USER=yourUSER
    SSH_PASS=yourPASS
    HOST_FILE=path/to/your/file/with/hosts.json  

By default `SSH_USER` and `SSH_PASS` will be used on all sessions unless you specify a different variable in the `hosts.csv` username and password fields.  
You can define unique username and password for each host if you wish, otherwise `SSH_USER` and `SSH_PASS` will be used on that host.

4. Make sure to create `hosts.csv` and add your sessions following the format found in `example-hosts.csv`.  You can add unique passwords to each session by specifying a .env variable in the `username` and `password` fields.  Just make sure that you define the variable in the .env like you did with `SSH_USER` and `SSH_PASS`.  

5. Afterward, you can start the application from that directory by typing in a terminal:
   `python3 nframes.py`

6. You can create a shell script/alias if you're on a Unix-like system to easily call the program from anywhere on the system, or if you're on Windows, you can create a batch file or shortcut.







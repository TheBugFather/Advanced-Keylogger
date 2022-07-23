# Advanced Keylogger
![alt text](https://github.com/ngimb64/Advanced-Keylogger/blob/master/Advanced_Keylogger.png?raw=true)
![alt text](https://github.com/ngimb64/Advanced-Keylogger/blob/master/AdvancedKeylogger.png?raw=true)

## Notice
> This tool may be used for legal purposes only.  Users take full responsibility
> for any actions performed using this tool.  The author accepts no liability
> for damage caused by this tool.  If these terms are not acceptable to you, then
> do not use this tool.

## Prereqs
This program runs on Windows, written in Python 3.8

## Purpose
As a Network and Infosec enthusiast the purpose of this project was originally to make a keylogger.
I decided to see what else can be incorporated and the project evolved into more of the realm of spyware.
Tutorial can be found at https://cybr.com/ethical-hacking-archives/how-i-made-a-python-keylogger-that-sends-emails/

## How it works
- Creates a directory to temporarily store information to exfiltrate
- Gets all the essential network information -> stores to log file &nbsp;&nbsp;&nbsp;&nbsp; (takes about a minute in a half)
- Gets the wireless network ssid's and passwords in XML data file
- Retrieves system hardware and running process/service info
- If on Windows and the clipboard is activated and contains anything -> stores to log file
- Browsing history is retrieved as a JSON data file then dumped into a log file
- Then using multiprocessing 4 features work together simultaneously: &nbsp;&nbsp;&nbsp;&nbsp; (set to 5 minutes for demo but timeouts and ranges can be adjusted)
1. Log pressed keys
2. Take screenshots every 5 seconds
3. Record microphone in one minute segments
4. Take webcam picture every 5 seconds
- After all the .txt and .xml files are grouped together and encrypted to protect sensitive data
- Then by individual directory, the files are grouped and sent through email by file type with regex magic
- Finally, the Log directory is deleted and the program loops back to the beginning to repeat the same process

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example:<br>
> python3 setup.py "venv name"

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows in the Scripts directory, for execute the "activate" script to activate the virtual environment.
- For Linux in the bin directory, run the command `source activate` to activate the virtual environment.

## How to use
- In google account, set up multi-factor authentication and generate application password for Gmail
- At line 142 enter your full email( username@gmail.com )
- At line 143 enter the generated app password for that email account
- Open up a command prompt and run the program
- Change to the directory the program is placed and execute it
- Open the graphical file manager and go to the C://Users/Public/Logs directory to watch the program in action
- After files are encrypted and sent to email, download them place them in the directory specified in
  decryptFile.py and run the program in command prompt.

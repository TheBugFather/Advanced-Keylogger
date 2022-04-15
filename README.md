# Advanced Keylogger
![alt text](https://github.com/ngimb64/Advanced-Keylogger/blob/master/AdvancedKeylogger.png?raw=true)

## Prereqs
This program runs on Windows, written in Python 3.8

## Installation
- Run setup.py <env name> to build virtual environment, any packages in packages.txt will be installed in the created venv.
- Once virtual env is built traverse to the Scripts directory in the environment folder just created.
- In the Scripts directory, execute the "activate" script to activate the virtual environment.

- At line 167 enter your full email( username@gmail.com )
- At line 168 enter the password for that email account
- Make sure in the gmail account settings that to allow less secure apps is on (Critical for using Google API)
- Open up a command prompt and run the program
- Change to the directory the program is placed and execute it
- Open the graphical file manager and go to the C://Users/Public/Logs directory to watch the program in action
- After files are encrypted and sent to email, download them place them in the directory specified in
  decryptFile.py and run the program in command prompt.

## Purpose
> As a Network and Infosec enthusiast the purpose of this project was originally to make a keylogger. 
> I decided to see what else can be incorporated and the project evolved into more of the realm of spyware.
> This is a project for learning and experimentation; unethical use is strictly prohibited.
> Only use on this program on personally owned systems or anyone that allows permission of use
> as a demonstration for raising awareness.
> It is intentionally not weaponized making it impossible to use on remote systems and has to manually be installed.
> Tutorial can be found at https://cybr.com/ethical-hacking-archives/how-i-made-a-python-keylogger-that-sends-emails/

## How it works
- Creates a directory to temporarily store information to exfiltrate
- Gets all the essential network information -> stores to log file &nbsp;&nbsp;&nbsp;&nbsp;(takes about a minute in a half)
- Gets the wireless network ssid's and passwords in XML data file
- Retrieves system hardware and running process/service info
- If the clipboard is activated and contains anything -> stores to log file
- Browsing history is retrieved as a JSON data file then dumped into a log file
- Then using multiprocessing 4 features work together simultaneously: &nbsp;&nbsp;&nbsp;&nbsp; (set to 5 minutes for demo but timeouts and ranges can be adjusted)
1. Log pressed keys
2. Take screenshots every 5 seconds
3. Record microphone in one minute segments
4. Take webcam picture every 5 seconds
- After all the .txt and .xml files are grouped together and encrypted to protect sensitive data
- Then by individual directory, the files are grouped and sent through email by file type with regex magic
- Finally, the Log directory is deleted and the program loops back to the beginning to repeat the same process

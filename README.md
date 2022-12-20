# Advanced Keylogger
![alt text](https://github.com/ngimb64/Advanced-Keylogger/blob/master/Advanced_Keylogger.png?raw=true)
![alt text](https://github.com/ngimb64/Advanced-Keylogger/blob/master/AdvancedKeylogger.png?raw=true)

&#9745;&#65039; Bandit verified<br>
&#9745;&#65039; Synk verified<br>
&#9745;&#65039; Pylint verified 9.89/10

## Notice
> This tool may be used for legal purposes only.<br>
> Users take full responsibility for any actions performed using this tool.<br> 
> The author accepts no liability for damage caused by this tool.<br>
> If these terms are not acceptable to you, then do not use this tool.

## Prereqs
This program runs on Windows 10 and Debian-based Linux, written in Python 3.8 and updated to version 3.10.6

## Purpose
As a network and info-sec enthusiast the purpose of this project was originally to make a keylogger.<br>
I decided to see what else can be incorporated and the project evolved into more of the functionality of spyware.<br>
Despite such functionality, the program does not attempt persistence or modify the registry, so it can be run outside of sandboxes.<br>
Tutorial can be found at https://cybr.com/ethical-hacking-archives/how-i-made-a-python-keylogger-that-sends-emails/

## How it works
- Creates a directory to temporarily store information to exfiltrate
- Gets all the essential network information -> stores to log file &ensp; (takes about a minute in a half)
- Gets the wireless network ssid's and passwords in XML data file
- Retrieves system hardware and running process/service info
- If on Windows and the clipboard is activated and contains anything -> stores to log file
- Browsing history is retrieved as a JSON data file then dumped into a log file
- Then using multiprocessing 4 features work together simultaneously for default 5 minute interval:

1. Log pressed keys
2. Take screenshots every 5 seconds
3. Record microphone in one minute segments
4. Take webcam picture every 5 seconds

- After all the .txt and .xml files are grouped together and encrypted to protect sensitive data
- Then by individual directory, the files are grouped and sent through email by file type with regex magic
- Finally, the Log directory is deleted and the program loops back to the beginning to repeat the same process

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Examples:<br> 
>       &emsp;&emsp;- Windows:  `python setup.py venv`<br>
>       &emsp;&emsp;- Linux:  `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows, in the venv\Scripts directory, execute `activate` or `activate.bat` script to activate the virtual environment.
- For Linux, in the venv/bin directory, execute `source activate` to activate the virtual environment.
- If for some reason issues are experienced with the setup script, the alternative is to manually create an environment, activate it, then run pip install -r packages.txt in project root.
- To exit from the virtual environment when finished, execute `deactivate`.

## How to use
- In google account, set up multi-factor authentication and generate application password for Gmail to allow API usage
- At the beginning of send_mail() function enter your full email( username@gmail.com ) and generated app password
- Open up a command prompt and run the program
- Change to the directory the program is placed and execute it
- Open the graphical file manager and go to the directory set at the beginning of main() function to watch the program in action
- After files are encrypted and sent to email, download them place them in the directory specified in
  decryptFile.py and run the program in command prompt.

## Function Layout
-- the_advanced_keylogger.py --
> smtp_handler &nbsp;-&nbsp; Facilitates sending the emails with the encrypted data to be exfiltrated.

> email_attach &nbsp;-&nbsp; Creates email attach object and returns it.

> email_header &nbsp;-&nbsp; Format email header and body.

> send_mail &nbsp;-&nbsp; Facilitates sending emails in a segmented fashion based on regex matches.

> encrypt_data &nbsp;-&nbsp; Encrypts all the file data in the parameter list of files to be 
> exfiltrated.

> RegObject &nbsp;-&nbsp; Regex object that contains numerous compiled expressions grouped together.

> webcam &nbsp;-&nbsp; Captures webcam pictures every five seconds.

> microphone &nbsp;-&nbsp; Actively records microphone in 60 second intervals.

> screenshot &nbsp;-&nbsp; Captured screenshots every five seconds.

> log_keys &nbsp;-&nbsp; Detect and log keys pressed by the user.

> get_browser_history &nbsp;-&nbsp; Get the browser username, path to browser databases, and the 
> entire browser history.

> get_clipboard &nbsp;-&nbsp; Gathers the clipboard contents and writes the output to the clipboard 
> output file.

> get_system_info &nbsp;-&nbsp; Runs an array of commands to gather system and hardware information.
> All the output is redirected to the system info output file.

> linux_wifi_query &nbsp;-&nbsp; Runs nmcli commands to query a list of Wi-Fi SSID's that the system
> has encountered. The SSID list is then iterated over line by line to query for each profile include
> passwords. All the output is redirected to the Wi-Fi info output file.

> get_network_info &nbsp;-&nbsp; Runs an array of commands to query network information, such as 
> network profiles, passwords, ip configuration, arp table, routing table, tcp/udp ports, and 
> attempt to query the ipify.org API for public IP address. All the output is redirected to the 
> network info output file.

> main &nbsp;-&nbsp; Gathers network information, clipboard contents, browser history, initiates 
> multiprocessing, sends encrypted results, cleans up exfiltrated data, and loops back to the beginning.

> print_err &nbsp;-&nbsp; Displays the passed in error message via stderr.

-- decrypt_file.py --
> print_err &nbsp;-&nbsp; Displays the passed in error message via stderr.

> main &nbsp;-&nbsp; Decrypts the encrypted contents in the DecryptDock Folder.

## Exit Codes
-- the_advanced_keylogger.y & decrypt_file.py --
> 0 &nbsp;-&nbsp; Successful operations<br>
> 1 &nbsp;-&nbsp; Unexpected error occurred
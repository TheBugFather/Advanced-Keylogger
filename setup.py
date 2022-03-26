# Script for installing modules not included
# with Python 3 default installation #
import os
import re
from subprocess import Popen, SubprocessError, TimeoutExpired, CalledProcessError


'''
########################################################################################################################
Name:       Install   
Purpose:    Executes system command to install external packages through PIP.
Parameters: Package name to be installed, standard out, standard error, execution timeout.
Returns:    None
########################################################################################################################
'''
def Install(package, stdout, stderr, exec_time):
    command = Popen(['pip', 'install', '--user', package], stdout=stdout, stderr=stderr, shell=False)
    try:
        # Execute Command #
        command.communicate(exec_time)
    # IF command times out or other error occurs #
    except (SubprocessError, TimeoutExpired, CalledProcessError, OSError, ValueError):
        command.kill()
        command.communicate()


'''
########################################################################################################################
Name:       main
Purpose:    Reads package file line by line, calls function to install external packages through PIP if regex matches.
Parameters: None
Returns:    None
########################################################################################################################
'''
def main():
    re_mod = re.compile(r'^[a-zA-Z0-9=\-.]{2,20}')
    filename = 'packages.txt'

    # If package file exists and has read access #
    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        try:
            # Open file #
            with open(filename, 'r') as file:
                # Iterate line by line #
                for line in file:
                    # If regex matches package name .. install #
                    if re.search(re_mod, line):
                        Install(line, None, None, 2)
        # File error handling #
        except (IOError, FileNotFoundError,Exception) as err:
            print(f'\n* Error Occurred: {err} *\n\n')
            input('Hit enter to end ..\n')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

# Copyright 2020 by Tuxedoar <tuxedoar@gmail.com>

# LICENSE

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys
import re
import getpass
from time import sleep
from socket import error
from _version import __version__
import paramiko

def main():
    """ Setup CLI arguments and call rest of the functions """

    args = menu_handler()
    cmd = args.COMMANDS
    pw = getpass.getpass('\n Please, enter your password to access hosts: ')
    target_hosts = read_hosts_file(args.FILE)

    # Start SSH session on each remote host.
    for target_host in target_hosts:
        try:
            remote_shell = setup_ssh_session(args.USER, pw, SSH_PORT, target_host)
            exec_remote_commands(remote_shell, cmd)
        except (KeyboardInterrupt, \
            paramiko.ssh_exception.AuthenticationException, \
            paramiko.SSHException, \
            error) as e:
            print("%s" % (e))

def menu_handler():
    """ Setup CLI arguments """
    parser = argparse.ArgumentParser(
        description='Excecute commands on several remote hosts, with SSH.')
    parser.add_argument('FILE', help='Plain text file with list of hosts')
    parser.add_argument('USER', help='User to login on remote hosts')
    parser.add_argument('COMMANDS', help='Comma separated commands to be \
                         executed on remote hosts')
    parser.add_argument('-p', '--port', nargs='?', type=int,
                        default=22, help='Specify SSH port to connect to hosts')
    parser.add_argument('-v', '--version', action='version',
                        version="%(prog)s {version}".format(version=__version__),
                        help='Show current version')
    args = parser.parse_args()
    return args


def setup_ssh_session(user, pw, port, remote_host):
    """ Setup the SSH session with necessary arguments """
    print("\n [+] Connecting to host %s with the user %s ... \n" % (remote_host, user))
    my_session = paramiko.SSHClient()
    my_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    my_session.connect(remote_host, username=user, password=pw, port=port, \
                      look_for_keys=False, allow_agent=False, timeout=10)
    remote_shell = my_session.invoke_shell()
    return remote_shell


def exec_remote_commands(remote_shell, commands):
    """ Execute provided commands on remote hosts! """
    remote_commands = commands.split(',')

    for command in remote_commands:
        # Remove double quotes!.
        command = command.replace('\"', '')
        remote_shell.send(command+'\n')
        # Wait 1 second before sending commands provided by user!.
        sleep(1)
        # Ouput buffer size in bytes!.
        output = remote_shell.recv(8000)
        # Split each line for output.
        output = output.splitlines()
        for lines in output:
            print(lines.decode())


def validate_ip_addr(ip_addr):
    """ Validate an IP address """
    validate_ip = re.search("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip_addr)
    return bool(validate_ip)


def read_hosts_file(hosts_file):
    """ Read the file and get the IP adresses  """
    remote_hosts = []
    try:
        with open(hosts_file, 'r') as file:
            for line in file.readlines():
                ip = line.strip()
                if line and not line.startswith('#'):
                    print("\n WARNING: The IP %s is NOT valid. Ignored!" % (ip)) \
                    if not validate_ip_addr(ip) else remote_hosts.append(ip)
        return remote_hosts

    except IOError:
        print("Can't read the specified file. Make sure it exist!.")
        sys.exit(2)

if __name__ == "__main__":
    main()

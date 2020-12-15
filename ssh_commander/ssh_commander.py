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
import itertools
import logging
import concurrent.futures
from socket import error
from time import sleep
import coloredlogs
import paramiko
from colorama import init, Fore
from _version import __version__

def main():
    """ Setup CLI arguments and multithreading  """
    try:
        # Setup colorful output
        coloredlogs.install(level='INFO', fmt='[%(hostname)s] %(asctime)s %(message)s')
        init(autoreset=True)
        args = menu_handler()
        target_hosts = read_hosts_file(args.FILE)
        nworkers = len(target_hosts)
        cmd = args.COMMANDS
        ssh_key_file = args.identity_file if args.identity_file else None
        pw = None
        if ssh_key_file is None:
            pw = getpass.getpass('\n Please, enter your password to access hosts: ')
        ssh_session_args = (args.USER, pw, args.port, ssh_key_file)
    except (KeyboardInterrupt, IOError) as err:
        logging.critical("%s\n", err)
        sys.exit()

    # Start multithreaded SSH sessions on remote hosts!.
    with concurrent.futures.ThreadPoolExecutor(max_workers=nworkers) as executor:
        for target_host in target_hosts:
            executor.submit(
                            manage_ssh_session,
                            ssh_session_args,
                            target_host,
                            cmd
                            )


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
    parser.add_argument('-i','--identity_file', help="Public key auth file")
    parser.add_argument('-v', '--version', action='version',
                        version="%(prog)s {version}".format(version=__version__),
                        help='Show current version')
    args = parser.parse_args()
    return args


def start_ssh_session(ssh_session, remote_host, session_args):
    """ Initialize SSH session with remote host """
    user, pw, port, ssh_key_file = session_args[0], \
                                    session_args[1], \
                                    session_args[2], \
                                    session_args[3]
    # Try key based auth first. At failure, try password based auth.
    try:
        logging.info("[+] Connecting to host %s with the user %s", remote_host, user)
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_session.connect(remote_host, username=user, port=port, timeout=10, \
                            key_filename=ssh_key_file)
        #logging.info("Authentication failed for host %s: %s", remote_host)

    except (
            paramiko.ssh_exception.AuthenticationException,
            paramiko.SSHException,
            IOError,
            error
            ) as e:
                logging.critical("Failed to connect to host %s: %s",
                                    remote_host, e)
                ssh_session.connect(remote_host, username=user, password=pw, port=port, \
                                    look_for_keys=False, allow_agent=False, timeout=10)
    return ssh_session


def manage_ssh_session(session_args, remote_host, commands):
    """ Setup the SSH session and exec commands at remote hosts """
    with paramiko.SSHClient() as my_session:
        ssh_session = start_ssh_session(my_session, remote_host, session_args)
        remote_shell = ssh_session.invoke_shell()
        hosts_output = exec_remote_commands(commands, remote_shell)
        show_hosts_output(hosts_output, remote_host)


def exec_remote_commands(commands, remote_shell):
    """ Execute provided commands on remote hosts! """
    hosts_cmds_output = []
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
        # Store each remote host output!
        hosts_cmds_output.append(output)

    # Flatten nested lists in "hosts_cmds_output"!
    flatten_hosts_output = itertools.chain.from_iterable(hosts_cmds_output)

    return flatten_hosts_output


def show_hosts_output(hosts_output, target_host):
    """ Show output results for each target host """
    logging.info(Fore.CYAN + "[*] Showing output for host %s ...\n", target_host)
    for output in hosts_output:
        print(output.decode())


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
                    logging.warning("The IP %s is NOT valid. Ignored!", ip) \
                    if not validate_ip_addr(ip) else remote_hosts.append(ip)
        return remote_hosts
    except IOError:
        logging.critical("Can't read %s file. Make sure it exist!.", hosts_file)
        sys.exit(2)

if __name__ == "__main__":
    main()

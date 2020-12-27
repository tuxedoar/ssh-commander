""" Helper functions for handling SSH sessions  """

from ssh_key_helper import check_ssh_keys_exist
from ssh_key_helper import should_ask_password
from time import sleep
import logging
import getpass
import paramiko
import itertools
from socket import error
from colorama import Fore

def setup_ssh_session_args(args):
    """ Setup needed SSH session arguments """
    check_home_ssh_keys = check_ssh_keys_exist()
    ssh_key_file = args.identity_file if args.identity_file else None
    pw = None
    ask_for_password = should_ask_password(ssh_key_file)
    if ask_for_password:
        logging.info("[+] No SSH key was found nor specified . " \
                         "Won't try key based authentication!")
        pw = getpass.getpass('\n Please, enter your password to access hosts: ')
    else:
        logging.info("[+] Trying key based authentication!")
    ssh_session_args = (
                        args.USER, \
                        pw, \
                        args.port, \
                        ssh_key_file, \
                        check_home_ssh_keys
                        )
    return ssh_session_args


def start_ssh_session(ssh_session, remote_host, session_args):
    """ Initialize SSH session with remote host """
    user, pw, port, ssh_key_file, check_home_ssh_keys = \
                                    session_args[0], \
                                    session_args[1], \
                                    session_args[2], \
                                    session_args[3], \
                                    session_args[4]

    try:
        ssh_session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if ssh_key_file is None and check_home_ssh_keys is not True:
            # Try password based auth!
            logging.info("[+] Trying password based auth for host: %s", remote_host)
            ssh_session.connect(remote_host, username=user, password=pw, port=port, \
                                look_for_keys=False, allow_agent=False, timeout=10)
        else:
            # Try key based auth
            logging.info("[+] Trying key based auth for host: %s", remote_host)
            ssh_session.connect(remote_host, username=user, port=port, timeout=10, \
                                key_filename=ssh_key_file)
    except (
            paramiko.ssh_exception.AuthenticationException,
            paramiko.SSHException,
            IOError,
            error
            ) as e:
                logging.critical("Failed to connect to host %s: %s",
                                    remote_host, e)
                sys.exit(1)
    return ssh_session


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


def manage_ssh_session(session_args, remote_host, commands):
    """ Setup the SSH session and exec commands at remote hosts """
    with paramiko.SSHClient() as my_session:
        ssh_session = start_ssh_session(my_session, remote_host, session_args)
        remote_shell = ssh_session.invoke_shell()
        hosts_output = exec_remote_commands(commands, remote_shell)
        show_hosts_output(hosts_output, remote_host)

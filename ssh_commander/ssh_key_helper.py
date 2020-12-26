""" Functions that help with SSH key handling aspects """

from pathlib import Path
import os

def get_ssh_homedir_content():
    """ Get the content of $HOME/.ssh/ dir"""
    ssh_homedir_content = False
    home_dir = Path.home()
    ssh_config_dir = Path(".ssh/")
    ssh_keys_default_dir = Path(home_dir, ssh_config_dir)
    if ssh_keys_default_dir.exists() and ssh_keys_default_dir.is_dir():
        ssh_homedir_content = os.listdir(ssh_keys_default_dir)
    return ssh_homedir_content


def check_ssh_keys_exist():
    """ Check if a default SSH key exist """
    check = None
    target_ssh_key_files = ("id_dsa", "id_ecdsa", "id_ed25519", "id_rsa")
    ssh_homedir = get_ssh_homedir_content() if get_ssh_homedir_content() is not False else None
    # Is there SSH key file in $HOME/.ssh? Compare both lists.
    check = any(item in target_ssh_key_files for item in ssh_homedir)
    return check


def should_ask_password(ssh_key_file):
    """ Decide whether to ask for password or not  """
    ask_for_password = False
    # Check for SSH keys at default location at $HOME/.ssh/
    check_home_ssh_keys = check_ssh_keys_exist()
    if ssh_key_file is None and check_home_ssh_keys is not True:
         ask_for_password = True
    return ask_for_password

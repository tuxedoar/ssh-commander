# SSH Commander
This *Command Line Interface* (CLI) tool, allows you to execute various commands on several remote hosts,
using the SSH protocol. As a result, you get a per-host generated output of each
command you specified.

You simply specify a plain text file with a list of remote hosts to connect to (domain names
or IP addresses), and a comma-separated list of commands to execute on those. Note that
access credentials (user and password) must be the same for all the target hosts!.

## Highlights and features
* Multithreaded since version `0.2`!.
* Almost no setup required, after installed!.
* Easy to use CLI syntax.
* Colorized output (since `v0.2`)!.

## Requirements
Make sure your system meets the following requirements:
* [Python 3](https://www.python.org/downloads/) (>= 3.6)
* [paramiko](https://github.com/paramiko/paramiko) (tested with v2.7.1)
* [colorama](https://github.com/tartley/colorama) (tested with v0.4.3)
* [coloredlogs](https://pypi.org/project/coloredlogs/) (tested with v14.0)

## Installation
The recommended method for installing this tool, is using `pip`:
```
pip install ssh-commander
```

## Usage
When using `ssh-commander`, respect the following syntax:
```
usage: ssh-commander [-h] [-p [PORT]] [-v] FILE USER COMMANDS

Excecute commands on several remote hosts, with SSH.

positional arguments:
  FILE                  Plain text file with list of hosts
  USER                  User to login on remote hosts
  COMMANDS              Comma separated commands to be executed on remote
                        hosts

optional arguments:
  -h, --help            show this help message and exit
  -p [PORT], --port [PORT]
                        Specify SSH port to connect to hosts
  -v, --version         Show current version
```
First, remember to create a text file (name it whatever you like), where you
list the target hosts. Its content, may look like this:
```
# This is a comment. It'll be ignored!.
192.168.0.10
192.168.0.11
192.168.0.12
```
Also, note that the password for the user provided, is gonna be asked only
once. Therefore, those credentials, should be valid on all target hosts!.

### Examples
Let's say you have some managed switches (or routers): 
```
ssh-commander hosts.txt root "terminal length 0, sh port-security"
```
They could rather be some GNU/Linux servers, as well:
```
ssh-commander hosts.txt foones "hostname, whoami"
```

## License
This program is licensed under the GPLv3.

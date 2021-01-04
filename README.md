# SSH Commander
This *Command Line Interface* (CLI) tool, allows you to execute various commands on several remote hosts, using the SSH 
protocol. As a result, you get a per-host generated output of each command you specified.

You simply specify a plain text file with a list of remote hosts to connect to (domain names or IP addresses), and a 
comma-separated list of commands to execute on those. Note that access credentials (user and password) must be the same for all 
the target hosts!.

## Highlights and features
* Key-based authentication support (`>=v0.3`)
* Multithreaded sessions (`>=v0.2`).
* Almost no setup required, after installed!.
* Easy to use CLI syntax.
* Colorized output (`>=v0.2`)!.

## Requirements
Make sure your system meets the following requirements:
* [Python 3](https://www.python.org/downloads/) (>= 3.7)
* [paramiko](https://github.com/paramiko/paramiko) (tested with v2.7.2)
* [colorama](https://github.com/tartley/colorama) (tested with v0.4.4)
* [coloredlogs](https://pypi.org/project/coloredlogs/) (tested with v15.0)

## Installation
The recommended method for installing this tool, is using `pip`:
```
pip install ssh-commander
```

## Usage
When using `ssh-commander`, respect the following syntax:
```
usage: ssh-commander [-h] [-p [PORT]] [-i IDENTITY_FILE] [-T] [-v]
                     FILE USER COMMANDS

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
  -i IDENTITY_FILE, --identity_file IDENTITY_FILE
                        Public key auth file
  -T, --trust_unknown   Trust hosts with no entries at known_hosts file 
  -v, --version         Show current version
```

### Setup your targeted hosts

First, remember to create a text file (name it whatever you like), where you list the target hosts. Its content, may look like 
this:
```
# This is a comment. It'll be ignored!.
192.168.0.10
192.168.0.11
192.168.0.12
```

### Authentication
Since `v0.3`, `ssh-commander` supports the following *authentication methods*:
* Password-based authentication.
* SSH key-based authentication.

In this regard, `ssh-commander` tries to mimmick the [OpenSSH](https://www.openssh.com/)
client default behaviour. In practical terms, this means that:
* If any valid *key file* is found at `~/.ssh/`, it'll attempt a *key-based
authentication* on all the targeted hosts!.
* If no valid *key file* is found nor provided, you'll be asked for a
* *password*, to be used as the *authentication method* for all remote hosts.
In any case, both the *SSH key* or the provided *password*, should be valid on ALL
the targeted hosts, for doing the authentication!.

#### Password-based authentication
A *password* is prompted ONLY if no previous valid *key file* was found, at default location (`~/.ssh/`). When using 
*password-based authentication*, note that the latter, is gonna be asked only once. Therefore, remember that those credentials, 
should be valid on all targeted hosts!.

#### SSH key-based authentication
As explained previously, firstly, `ssh-commander` is gonna try a *key-based authentication*, by looking for valid *keys* at the 
`~/.ssh/` directory.

The following types of keys are looked for:
* `id_dsa`
* `id_ecdsa`
* `id_ed25519`
* `id_rsa`

An alternative key file location, can be specified by using the `-i` CLI
option!.

### Known hosts validation
By default, `ssh-commander` will take a look at the `~/.ssh/known_hosts` file and check that each targeted host, has a matching 
entry in it. If it doesn't, it'll warn you and ask for an explicit confirmation, about whether you trust each of those hosts 
anyway or not!.

Note that if you answer negatively to the trust confirmation, nothing is done and the program exits with a notification.

If you don't want this validation to be performed, you can use the `-T` option, to blindly trust the remote hosts!.

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

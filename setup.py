from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ssh-commander',
    version='0.1',
    description='Excecute remote commands on several hosts, with SSH',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tuxedoar/ssh-commander',
    author='tuxedoar',
    author_email='tuxedoar@gmail.com',
    packages=['ssh-commander'],
    entry_points={
        "console_scripts": [
        "ssh-commander = ssh-commander.ssh-commander:main",
        ],
    },
    install_requires=[
    'paramiko>=2.4.3'
    ],

    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        ],
)

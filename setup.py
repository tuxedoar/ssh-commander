from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ssh-commander',
    version='0.2',
    description='Excecute commands on several remote hosts, with SSH',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tuxedoar/ssh-commander',
    author='tuxedoar',
    author_email='tuxedoar@gmail.com',
    packages=['ssh_commander'],
    python_requires='>=3.6',
    scripts=["ssh_commander/_version.py"],
    entry_points={
        "console_scripts": [
        "ssh-commander = ssh_commander.ssh_commander:main",
        ],
    },
    install_requires=[
    'paramiko',
    'colorama',
    'coloredlogs'
    ],

    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: System Administrators",
        "Environment :: Console",
        ],
)

